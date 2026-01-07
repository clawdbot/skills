import { getValidToken } from "./auth";

const API_BASE = "https://api.ticktick.com/open/v1";

export interface Project {
  id: string;
  name: string;
  color?: string;
  sortOrder?: number;
  closed?: boolean;
  groupId?: string;
  viewMode?: string;
  permission?: string;
  kind?: string;
}

export interface Task {
  id: string;
  projectId: string;
  title: string;
  content?: string;
  desc?: string;
  priority: number;
  status: number;
  dueDate?: string;
  startDate?: string;
  isAllDay?: boolean;
  timeZone?: string;
  reminders?: string[];
  tags?: string[];
  items?: ChecklistItem[];
  sortOrder?: number;
  completedTime?: string;
}

export interface ChecklistItem {
  id: string;
  title: string;
  status: number;
  sortOrder: number;
}

export interface ProjectData {
  project: Project;
  tasks: Task[];
}

export interface CreateTaskInput {
  title: string;
  projectId: string;
  content?: string;
  priority?: number;
  dueDate?: string;
  startDate?: string;
  isAllDay?: boolean;
  tags?: string[];
}

export interface UpdateTaskInput {
  id: string;
  projectId: string;
  title?: string;
  content?: string;
  priority?: number;
  status?: number;
  dueDate?: string;
  startDate?: string;
  isAllDay?: boolean;
  tags?: string[];
}

export interface BatchDeleteItem {
  taskId: string;
  projectId: string;
}

export interface BatchRequest {
  add?: CreateTaskInput[];
  update?: UpdateTaskInput[];
  delete?: BatchDeleteItem[];
}

export interface BatchResponse {
  id2etag?: Record<string, string>;
  id2error?: Record<string, string>;
}

export interface CreateProjectInput {
  name: string;
  color?: string;
}

export interface UpdateProjectInput {
  id: string;
  name?: string;
  color?: string;
}

// Priority mapping
export const PRIORITY_MAP: Record<string, number> = {
  none: 0,
  low: 1,
  medium: 3,
  high: 5,
};

export const PRIORITY_REVERSE: Record<number, string> = {
  0: "none",
  1: "low",
  3: "medium",
  5: "high",
};

class TickTickAPI {
  private static readonly RETRY_DELAYS = [5000, 15000, 30000, 60000];
  private static readonly MAX_RETRIES = 4;

  private async request<T>(
    endpoint: string,
    options: RequestInit = {},
    retryCount = 0
  ): Promise<T> {
    const token = await getValidToken();

    const response = await fetch(`${API_BASE}${endpoint}`, {
      ...options,
      headers: {
        Authorization: `Bearer ${token}`,
        "Content-Type": "application/json",
        ...options.headers,
      },
    });

    if (!response.ok) {
      const errorText = await response.text();

      // Handle rate limit errors (returned as 500 with exceed_query_limit)
      if (response.status === 500 && errorText.includes("exceed_query_limit")) {
        if (retryCount < TickTickAPI.MAX_RETRIES) {
          const waitMs = TickTickAPI.RETRY_DELAYS[retryCount];
          console.error(
            `Rate limited, waiting ${waitMs / 1000}s before retry ${retryCount + 1}/${TickTickAPI.MAX_RETRIES}...`
          );
          await new Promise((r) => setTimeout(r, waitMs));
          return this.request(endpoint, options, retryCount + 1);
        }
        throw new Error(
          "Rate limit exceeded. Maximum retries reached. Please wait a few minutes and try again."
        );
      }

      if (response.status === 401) {
        throw new Error(
          "Authentication expired. Please run 'ticktick auth' to re-authenticate."
        );
      }
      if (response.status === 404) {
        throw new Error(`Not found: ${endpoint}`);
      }
      if (response.status === 429) {
        // Also handle standard 429 rate limit with retry
        if (retryCount < TickTickAPI.MAX_RETRIES) {
          const waitMs = TickTickAPI.RETRY_DELAYS[retryCount];
          console.error(
            `Rate limited (429), waiting ${waitMs / 1000}s before retry ${retryCount + 1}/${TickTickAPI.MAX_RETRIES}...`
          );
          await new Promise((r) => setTimeout(r, waitMs));
          return this.request(endpoint, options, retryCount + 1);
        }
        throw new Error(
          "Rate limit exceeded. Maximum retries reached. Please wait a few minutes and try again."
        );
      }
      throw new Error(
        `API error ${response.status}: ${errorText || response.statusText}`
      );
    }

    // Handle empty responses
    const text = await response.text();
    if (!text) {
      return {} as T;
    }

    return JSON.parse(text);
  }

  // Projects
  async listProjects(): Promise<Project[]> {
    return this.request<Project[]>("/project");
  }

  async createProject(input: CreateProjectInput): Promise<Project> {
    return this.request<Project>("/project", {
      method: "POST",
      body: JSON.stringify(input),
    });
  }

  async updateProject(input: UpdateProjectInput): Promise<Project> {
    return this.request<Project>(`/project/${input.id}`, {
      method: "POST",
      body: JSON.stringify(input),
    });
  }

  async getProjectData(projectId: string): Promise<ProjectData> {
    return this.request<ProjectData>(`/project/${projectId}/data`);
  }

  async getInboxData(): Promise<ProjectData> {
    // Inbox is a special project
    const projects = await this.listProjects();
    const inbox = projects.find(
      (p) => p.name.toLowerCase() === "inbox" || p.kind === "INBOX"
    );
    if (!inbox) {
      // Fallback - try the inbox endpoint
      return this.request<ProjectData>("/project/inbox/data");
    }
    return this.getProjectData(inbox.id);
  }

  // Tasks
  async createTask(input: CreateTaskInput): Promise<Task> {
    return this.request<Task>("/task", {
      method: "POST",
      body: JSON.stringify(input),
    });
  }

  async updateTask(input: UpdateTaskInput): Promise<Task> {
    return this.request<Task>(`/task/${input.id}`, {
      method: "POST",
      body: JSON.stringify(input),
    });
  }

  async completeTask(projectId: string, taskId: string): Promise<void> {
    await this.request<void>(`/project/${projectId}/task/${taskId}/complete`, {
      method: "POST",
    });
  }

  async deleteTask(projectId: string, taskId: string): Promise<void> {
    await this.request<void>(`/project/${projectId}/task/${taskId}`, {
      method: "DELETE",
    });
  }

  async batchTasks(batch: BatchRequest): Promise<BatchResponse> {
    return this.request<BatchResponse>("/batch/task", {
      method: "POST",
      body: JSON.stringify(batch),
    });
  }

  // Utility functions
  async findProjectByName(name: string): Promise<Project | undefined> {
    const projects = await this.listProjects();
    const lowerName = name.toLowerCase();
    return projects.find(
      (p) => p.name.toLowerCase() === lowerName || p.id === name
    );
  }

  async findTaskById(taskId: string): Promise<{ task: Task; projectId: string } | undefined> {
    const projects = await this.listProjects();

    for (const project of projects) {
      try {
        const data = await this.getProjectData(project.id);
        const task = data.tasks?.find((t) => t.id === taskId);
        if (task) {
          return { task, projectId: project.id };
        }
      } catch {
        // Project might not have tasks accessible
        continue;
      }
    }
    return undefined;
  }

  async findTaskByTitle(
    title: string,
    projectId?: string
  ): Promise<{ task: Task; projectId: string } | undefined> {
    const projects = await this.listProjects();
    const searchProjects = projectId
      ? projects.filter((p) => p.id === projectId || p.name.toLowerCase() === projectId.toLowerCase())
      : projects;

    // Check if searching by ID (24-char hex string)
    const isIdSearch = /^[a-f0-9]{24}$/i.test(title);

    const matches: Array<{ task: Task; projectId: string; projectName: string }> = [];

    for (const project of searchProjects) {
      try {
        const data = await this.getProjectData(project.id);
        const matchingTasks = data.tasks?.filter(
          (t) => t.title.toLowerCase() === title.toLowerCase() || t.id === title
        ) || [];

        for (const task of matchingTasks) {
          matches.push({ task, projectId: project.id, projectName: project.name });
        }
      } catch {
        // Project might not have tasks accessible
        continue;
      }
    }

    if (matches.length === 0) {
      return undefined;
    }

    // If searching by ID or only one match, return it
    if (isIdSearch || matches.length === 1) {
      return { task: matches[0].task, projectId: matches[0].projectId };
    }

    // Multiple matches found - throw error with details
    const matchList = matches
      .map((m) => `  [${m.task.id.slice(0, 8)}] "${m.task.title}" in project "${m.projectName}"`)
      .join("\n");
    throw new Error(
      `Multiple tasks found with name "${title}":\n${matchList}\n\nPlease use the task ID instead of the name to specify which task.`
    );
  }

  async getAllTasks(projectId?: string): Promise<Task[]> {
    const projects = await this.listProjects();
    const searchProjects = projectId
      ? projects.filter((p) => p.id === projectId || p.name.toLowerCase() === projectId.toLowerCase())
      : projects;

    const allTasks: Task[] = [];

    for (const project of searchProjects) {
      try {
        const data = await this.getProjectData(project.id);
        if (data.tasks) {
          allTasks.push(...data.tasks);
        }
      } catch {
        // Project might not have tasks accessible
        continue;
      }
    }

    return allTasks;
  }
}

export const api = new TickTickAPI();
