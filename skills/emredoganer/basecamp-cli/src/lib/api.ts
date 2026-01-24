import got, { Got, Options, HTTPError } from 'got';
import chalk from 'chalk';
import { getValidAccessToken } from './auth.js';
import { getCurrentAccountId } from './config.js';
import type {
  BasecampProject,
  BasecampTodoList,
  BasecampTodo,
  BasecampMessage,
  BasecampCampfire,
  BasecampCampfireLine,
  BasecampPerson,
  BasecampDock
} from '../types/index.js';

const USER_AGENT = 'Basecamp CLI (emredoganer@github.com)';

async function createClient(): Promise<Got> {
  const accessToken = await getValidAccessToken();
  const accountId = getCurrentAccountId();

  if (!accountId) {
    throw new Error('No account selected. Please run: basecamp account set <id>');
  }

  return got.extend({
    prefixUrl: `https://3.basecampapi.com/${accountId}/`,
    headers: {
      'Authorization': `Bearer ${accessToken}`,
      'User-Agent': USER_AGENT,
      'Content-Type': 'application/json'
    },
    responseType: 'json',
    hooks: {
      beforeError: [
        (error) => {
          if (error instanceof HTTPError) {
            const { response } = error;
            if (response.statusCode === 429) {
              console.error(chalk.yellow('Rate limited. Please wait and try again.'));
            } else if (response.statusCode === 401) {
              console.error(chalk.red('Authentication failed. Please run: basecamp auth login'));
            } else if (response.statusCode === 404) {
              console.error(chalk.red('Resource not found.'));
            }
          }
          return error;
        }
      ]
    }
  });
}

// Projects
export async function listProjects(): Promise<BasecampProject[]> {
  const client = await createClient();
  const response = await client.get('projects.json').json<BasecampProject[]>();
  return response;
}

export async function getProject(projectId: number): Promise<BasecampProject> {
  const client = await createClient();
  const response = await client.get(`projects/${projectId}.json`).json<BasecampProject>();
  return response;
}

export async function createProject(name: string, description?: string): Promise<BasecampProject> {
  const client = await createClient();
  const response = await client.post('projects.json', {
    json: { name, description }
  }).json<BasecampProject>();
  return response;
}

export async function archiveProject(projectId: number): Promise<void> {
  const client = await createClient();
  await client.put(`projects/${projectId}.json`, {
    json: { status: 'archived' }
  });
}

// Todo Lists
export async function listTodoLists(projectId: number): Promise<BasecampTodoList[]> {
  const client = await createClient();
  const project = await getProject(projectId);
  const todosetDock = project.dock.find((d: BasecampDock) => d.name === 'todoset');

  if (!todosetDock) {
    throw new Error('To-do lists not enabled for this project');
  }

  const todosetId = todosetDock.id;
  const response = await client.get(`buckets/${projectId}/todosets/${todosetId}/todolists.json`).json<BasecampTodoList[]>();
  return response;
}

export async function getTodoList(projectId: number, todolistId: number): Promise<BasecampTodoList> {
  const client = await createClient();
  const response = await client.get(`buckets/${projectId}/todolists/${todolistId}.json`).json<BasecampTodoList>();
  return response;
}

export async function createTodoList(projectId: number, name: string, description?: string): Promise<BasecampTodoList> {
  const client = await createClient();
  const project = await getProject(projectId);
  const todosetDock = project.dock.find((d: BasecampDock) => d.name === 'todoset');

  if (!todosetDock) {
    throw new Error('To-do lists not enabled for this project');
  }

  const todosetId = todosetDock.id;
  const response = await client.post(`buckets/${projectId}/todosets/${todosetId}/todolists.json`, {
    json: { name, description }
  }).json<BasecampTodoList>();
  return response;
}

// Todos
export async function listTodos(projectId: number, todolistId: number, completed?: boolean): Promise<BasecampTodo[]> {
  const client = await createClient();
  const params = completed !== undefined ? `?completed=${completed}` : '';
  const response = await client.get(`buckets/${projectId}/todolists/${todolistId}/todos.json${params}`).json<BasecampTodo[]>();
  return response;
}

export async function getTodo(projectId: number, todoId: number): Promise<BasecampTodo> {
  const client = await createClient();
  const response = await client.get(`buckets/${projectId}/todos/${todoId}.json`).json<BasecampTodo>();
  return response;
}

export async function createTodo(
  projectId: number,
  todolistId: number,
  content: string,
  options?: {
    description?: string;
    assignee_ids?: number[];
    due_on?: string;
    starts_on?: string;
  }
): Promise<BasecampTodo> {
  const client = await createClient();
  const response = await client.post(`buckets/${projectId}/todolists/${todolistId}/todos.json`, {
    json: { content, ...options }
  }).json<BasecampTodo>();
  return response;
}

export async function updateTodo(
  projectId: number,
  todoId: number,
  updates: {
    content?: string;
    description?: string;
    assignee_ids?: number[];
    due_on?: string | null;
    starts_on?: string | null;
  }
): Promise<BasecampTodo> {
  const client = await createClient();
  const response = await client.put(`buckets/${projectId}/todos/${todoId}.json`, {
    json: updates
  }).json<BasecampTodo>();
  return response;
}

export async function completeTodo(projectId: number, todoId: number): Promise<void> {
  const client = await createClient();
  await client.post(`buckets/${projectId}/todos/${todoId}/completion.json`);
}

export async function uncompleteTodo(projectId: number, todoId: number): Promise<void> {
  const client = await createClient();
  await client.delete(`buckets/${projectId}/todos/${todoId}/completion.json`);
}

// Messages
export async function listMessages(projectId: number): Promise<BasecampMessage[]> {
  const client = await createClient();
  const project = await getProject(projectId);
  const messageboardDock = project.dock.find((d: BasecampDock) => d.name === 'message_board');

  if (!messageboardDock) {
    throw new Error('Message board not enabled for this project');
  }

  const messageboardId = messageboardDock.id;
  const response = await client.get(`buckets/${projectId}/message_boards/${messageboardId}/messages.json`).json<BasecampMessage[]>();
  return response;
}

export async function getMessage(projectId: number, messageId: number): Promise<BasecampMessage> {
  const client = await createClient();
  const response = await client.get(`buckets/${projectId}/messages/${messageId}.json`).json<BasecampMessage>();
  return response;
}

export async function createMessage(
  projectId: number,
  subject: string,
  content?: string
): Promise<BasecampMessage> {
  const client = await createClient();
  const project = await getProject(projectId);
  const messageboardDock = project.dock.find((d: BasecampDock) => d.name === 'message_board');

  if (!messageboardDock) {
    throw new Error('Message board not enabled for this project');
  }

  const messageboardId = messageboardDock.id;
  const response = await client.post(`buckets/${projectId}/message_boards/${messageboardId}/messages.json`, {
    json: { subject, content }
  }).json<BasecampMessage>();
  return response;
}

// Campfires
export async function listCampfires(projectId: number): Promise<BasecampCampfire[]> {
  const client = await createClient();
  const project = await getProject(projectId);
  const campfireDock = project.dock.find((d: BasecampDock) => d.name === 'chat');

  if (!campfireDock) {
    throw new Error('Campfire not enabled for this project');
  }

  // Return the campfire as an array
  const response = await client.get(`buckets/${projectId}/chats/${campfireDock.id}.json`).json<BasecampCampfire>();
  return [response];
}

export async function getCampfireLines(projectId: number, campfireId: number): Promise<BasecampCampfireLine[]> {
  const client = await createClient();
  const response = await client.get(`buckets/${projectId}/chats/${campfireId}/lines.json`).json<BasecampCampfireLine[]>();
  return response;
}

export async function sendCampfireLine(projectId: number, campfireId: number, content: string): Promise<BasecampCampfireLine> {
  const client = await createClient();
  const response = await client.post(`buckets/${projectId}/chats/${campfireId}/lines.json`, {
    json: { content }
  }).json<BasecampCampfireLine>();
  return response;
}

// People
export async function listPeople(projectId?: number): Promise<BasecampPerson[]> {
  const client = await createClient();
  const url = projectId ? `projects/${projectId}/people.json` : 'people.json';
  const response = await client.get(url).json<BasecampPerson[]>();
  return response;
}

export async function getPerson(personId: number): Promise<BasecampPerson> {
  const client = await createClient();
  const response = await client.get(`people/${personId}.json`).json<BasecampPerson>();
  return response;
}

export async function getMe(): Promise<BasecampPerson> {
  const client = await createClient();
  const response = await client.get('my/profile.json').json<BasecampPerson>();
  return response;
}
