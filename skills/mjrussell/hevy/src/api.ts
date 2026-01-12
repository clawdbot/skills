/**
 * Hevy API Client
 * 
 * REST client for the Hevy workout tracking API.
 * Docs: https://api.hevyapp.com/docs/
 */

import type {
  HevyConfig,
} from "./config.js";
import type {
  Workout,
  WorkoutsResponse,
  WorkoutCountResponse,
  WorkoutEventsResponse,
  Routine,
  RoutinesResponse,
  RoutineFolder,
  RoutineFoldersResponse,
  ExerciseTemplate,
  ExerciseTemplatesResponse,
  ExerciseHistoryResponse,
  CreateWorkoutRequest,
  CreateRoutineRequest,
  UpdateRoutineRequest,
  CreateRoutineFolderRequest,
  CreateExerciseTemplateRequest,
} from "./types.js";

const BASE_URL = "https://api.hevyapp.com";

export class HevyClient {
  private apiKey: string;

  constructor(config: HevyConfig) {
    this.apiKey = config.apiKey;
  }

  /**
   * Make an authenticated request to the Hevy API
   */
  private async request<T>(
    endpoint: string,
    options: RequestInit = {}
  ): Promise<T> {
    const url = `${BASE_URL}${endpoint}`;
    const headers: Record<string, string> = {
      "api-key": this.apiKey,
      "Content-Type": "application/json",
      ...(options.headers as Record<string, string>),
    };

    const response = await fetch(url, {
      ...options,
      headers,
    });

    if (!response.ok) {
      const text = await response.text();
      throw new Error(`Hevy API error ${response.status}: ${text}`);
    }

    // Handle empty responses (e.g., 204 No Content)
    const contentLength = response.headers.get("content-length");
    if (contentLength === "0" || response.status === 204) {
      return {} as T;
    }

    return response.json() as Promise<T>;
  }

  // ============================================
  // Workouts
  // ============================================

  /**
   * Get paginated list of workouts
   * @param page Page number (1-indexed)
   * @param pageSize Items per page (max 10)
   */
  async getWorkouts(page = 1, pageSize = 10): Promise<WorkoutsResponse> {
    const params = new URLSearchParams({
      page: String(page),
      pageSize: String(Math.min(pageSize, 10)),
    });
    return this.request<WorkoutsResponse>(`/v1/workouts?${params}`);
  }

  /**
   * Get all workouts (auto-paginate)
   */
  async getAllWorkouts(): Promise<Workout[]> {
    const allWorkouts: Workout[] = [];
    let page = 1;
    let pageCount = 1;

    do {
      const response = await this.getWorkouts(page, 10);
      allWorkouts.push(...response.workouts);
      pageCount = response.page_count;
      page++;
    } while (page <= pageCount);

    return allWorkouts;
  }

  /**
   * Get a single workout by ID
   */
  async getWorkout(workoutId: string): Promise<Workout> {
    // API may return { workout: {...} } wrapper
    const response = await this.request<Workout | { workout: Workout }>(`/v1/workouts/${workoutId}`);
    return 'workout' in response ? response.workout : response;
  }

  /**
   * Get total workout count
   */
  async getWorkoutCount(): Promise<number> {
    const response = await this.request<WorkoutCountResponse>("/v1/workouts/count");
    return response.workout_count;
  }

  /**
   * Get workout events since a date (for syncing)
   * @param since ISO 8601 date string
   */
  async getWorkoutEvents(since: string, page = 1, pageSize = 10): Promise<WorkoutEventsResponse> {
    const params = new URLSearchParams({
      page: String(page),
      pageSize: String(Math.min(pageSize, 10)),
      since,
    });
    return this.request<WorkoutEventsResponse>(`/v1/workouts/events?${params}`);
  }

  /**
   * Create a new workout
   */
  async createWorkout(workout: CreateWorkoutRequest): Promise<Workout> {
    return this.request<Workout>("/v1/workouts", {
      method: "POST",
      body: JSON.stringify(workout),
    });
  }

  /**
   * Update an existing workout
   */
  async updateWorkout(workoutId: string, workout: CreateWorkoutRequest): Promise<Workout> {
    return this.request<Workout>(`/v1/workouts/${workoutId}`, {
      method: "PUT",
      body: JSON.stringify(workout),
    });
  }

  // ============================================
  // Routines
  // ============================================

  /**
   * Get paginated list of routines
   */
  async getRoutines(page = 1, pageSize = 10): Promise<RoutinesResponse> {
    const params = new URLSearchParams({
      page: String(page),
      pageSize: String(Math.min(pageSize, 10)),
    });
    return this.request<RoutinesResponse>(`/v1/routines?${params}`);
  }

  /**
   * Get all routines (auto-paginate)
   */
  async getAllRoutines(): Promise<Routine[]> {
    const allRoutines: Routine[] = [];
    let page = 1;
    let pageCount = 1;

    do {
      const response = await this.getRoutines(page, 10);
      allRoutines.push(...response.routines);
      pageCount = response.page_count;
      page++;
    } while (page <= pageCount);

    return allRoutines;
  }

  /**
   * Get a single routine by ID
   */
  async getRoutine(routineId: string): Promise<Routine> {
    const response = await this.request<{ routine: Routine }>(`/v1/routines/${routineId}`);
    return response.routine;
  }

  /**
   * Create a new routine
   */
  async createRoutine(routine: CreateRoutineRequest): Promise<Routine> {
    const response = await this.request<{ routine: Routine[] }>("/v1/routines", {
      method: "POST",
      body: JSON.stringify(routine),
    });
    // API returns { routine: [Routine] }
    return response.routine[0];
  }

  /**
   * Update an existing routine
   */
  async updateRoutine(routineId: string, routine: UpdateRoutineRequest): Promise<Routine> {
    return this.request<Routine>(`/v1/routines/${routineId}`, {
      method: "PUT",
      body: JSON.stringify(routine),
    });
  }

  // ============================================
  // Routine Folders
  // ============================================

  /**
   * Get paginated list of routine folders
   */
  async getRoutineFolders(page = 1, pageSize = 10): Promise<RoutineFoldersResponse> {
    const params = new URLSearchParams({
      page: String(page),
      pageSize: String(Math.min(pageSize, 10)),
    });
    return this.request<RoutineFoldersResponse>(`/v1/routine_folders?${params}`);
  }

  /**
   * Get all routine folders (auto-paginate)
   */
  async getAllRoutineFolders(): Promise<RoutineFolder[]> {
    const allFolders: RoutineFolder[] = [];
    let page = 1;
    let pageCount = 1;

    do {
      const response = await this.getRoutineFolders(page, 10);
      // API returns routine_folders or routines depending on if empty
      const folders = response.routine_folders ?? response.routines ?? [];
      allFolders.push(...folders);
      pageCount = response.page_count;
      page++;
    } while (page <= pageCount);

    return allFolders;
  }

  /**
   * Get a single routine folder by ID
   */
  async getRoutineFolder(folderId: number): Promise<RoutineFolder> {
    return this.request<RoutineFolder>(`/v1/routine_folders/${folderId}`);
  }

  /**
   * Create a new routine folder
   */
  async createRoutineFolder(folder: CreateRoutineFolderRequest): Promise<RoutineFolder> {
    return this.request<RoutineFolder>("/v1/routine_folders", {
      method: "POST",
      body: JSON.stringify(folder),
    });
  }

  // ============================================
  // Exercise Templates
  // ============================================

  /**
   * Get paginated list of exercise templates
   */
  async getExerciseTemplates(page = 1, pageSize = 10): Promise<ExerciseTemplatesResponse> {
    const params = new URLSearchParams({
      page: String(page),
      pageSize: String(Math.min(pageSize, 10)),
    });
    return this.request<ExerciseTemplatesResponse>(`/v1/exercise_templates?${params}`);
  }

  /**
   * Get all exercise templates (auto-paginate)
   * Note: This can be a lot of data - Hevy has hundreds of built-in exercises
   */
  async getAllExerciseTemplates(): Promise<ExerciseTemplate[]> {
    const allTemplates: ExerciseTemplate[] = [];
    let page = 1;
    let pageCount = 1;

    do {
      const response = await this.getExerciseTemplates(page, 10);
      allTemplates.push(...response.exercise_templates);
      pageCount = response.page_count;
      page++;
    } while (page <= pageCount);

    return allTemplates;
  }

  /**
   * Get a single exercise template by ID
   */
  async getExerciseTemplate(templateId: string): Promise<ExerciseTemplate> {
    return this.request<ExerciseTemplate>(`/v1/exercise_templates/${templateId}`);
  }

  /**
   * Create a custom exercise template
   */
  async createExerciseTemplate(template: CreateExerciseTemplateRequest): Promise<ExerciseTemplate> {
    return this.request<ExerciseTemplate>("/v1/exercise_templates", {
      method: "POST",
      body: JSON.stringify(template),
    });
  }

  // ============================================
  // Exercise History
  // ============================================

  /**
   * Get exercise history for a specific exercise template
   * Returns all sets ever performed for this exercise
   */
  async getExerciseHistory(templateId: string, page = 1, pageSize = 10): Promise<ExerciseHistoryResponse> {
    const params = new URLSearchParams({
      page: String(page),
      pageSize: String(Math.min(pageSize, 10)),
    });
    return this.request<ExerciseHistoryResponse>(`/v1/exercise_history/${templateId}?${params}`);
  }

  /**
   * Get all exercise history for a template (auto-paginate)
   */
  async getAllExerciseHistory(templateId: string): Promise<ExerciseHistoryResponse["exercise_history"]> {
    const allHistory: ExerciseHistoryResponse["exercise_history"] = [];
    let page = 1;
    let pageCount = 1;

    do {
      const response = await this.getExerciseHistory(templateId, page, 10);
      allHistory.push(...response.exercise_history);
      pageCount = response.page_count;
      page++;
    } while (page <= pageCount);

    return allHistory;
  }

  // ============================================
  // Utility Methods
  // ============================================

  /**
   * Search exercise templates by name
   */
  async searchExerciseTemplates(query: string): Promise<ExerciseTemplate[]> {
    const templates = await this.getAllExerciseTemplates();
    const lowerQuery = query.toLowerCase();
    return templates.filter(t => 
      t.title.toLowerCase().includes(lowerQuery)
    );
  }

  /**
   * Get recent workouts (shorthand for first page)
   */
  async getRecentWorkouts(limit = 5): Promise<Workout[]> {
    const response = await this.getWorkouts(1, Math.min(limit, 10));
    return response.workouts.slice(0, limit);
  }

  /**
   * Find exercise template by exact or partial name match
   */
  async findExerciseTemplate(name: string): Promise<ExerciseTemplate | null> {
    const templates = await this.searchExerciseTemplates(name);
    if (templates.length === 0) return null;
    
    // Prefer exact match
    const lowerName = name.toLowerCase();
    const exact = templates.find(t => t.title.toLowerCase() === lowerName);
    return exact ?? templates[0];
  }
}
