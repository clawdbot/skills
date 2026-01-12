// Hevy API Types - Generated from OpenAPI spec

// Enums
export type SetType = "warmup" | "normal" | "failure" | "dropset";

export type ExerciseType =
  | "weight_reps"
  | "reps_only"
  | "bodyweight_reps"
  | "bodyweight_assisted_reps"
  | "duration"
  | "weight_duration"
  | "distance_duration"
  | "short_distance_weight";

export type MuscleGroup =
  | "abdominals"
  | "shoulders"
  | "biceps"
  | "triceps"
  | "forearms"
  | "quadriceps"
  | "hamstrings"
  | "calves"
  | "glutes"
  | "abductors"
  | "adductors"
  | "lats"
  | "upper_back"
  | "traps"
  | "lower_back"
  | "chest"
  | "cardio"
  | "neck"
  | "full_body"
  | "other";

export type EquipmentCategory =
  | "none"
  | "barbell"
  | "dumbbell"
  | "kettlebell"
  | "machine"
  | "plate"
  | "resistance_band"
  | "suspension"
  | "other";

// Core types
export interface Set {
  index: number;
  type: SetType;
  weight_kg: number | null;
  reps: number | null;
  distance_meters: number | null;
  duration_seconds: number | null;
  rpe: number | null;
  custom_metric: number | null;
}

export interface RepRange {
  start: number | null;
  end: number | null;
}

export interface RoutineSet extends Set {
  rep_range?: RepRange | null;
}

export interface Exercise {
  index: number;
  title: string;
  notes: string;
  exercise_template_id: string;
  supersets_id: number | null;
  sets: Set[];
}

export interface RoutineExercise {
  index: number;
  title: string;
  rest_seconds: number | null;
  notes: string;
  exercise_template_id: string;
  supersets_id: number | null;
  sets: RoutineSet[];
}

export interface Workout {
  id: string;
  title: string;
  routine_id?: string;
  description: string;
  start_time: string;
  end_time: string;
  updated_at: string;
  created_at: string;
  exercises: Exercise[];
}

export interface Routine {
  id: string;
  title: string;
  folder_id: number | null;
  updated_at: string;
  created_at: string;
  notes?: string;
  exercises: RoutineExercise[];
}

export interface RoutineFolder {
  id: number;
  index: number;
  title: string;
  updated_at: string;
  created_at: string;
}

export interface ExerciseTemplate {
  id: string;
  title: string;
  type: ExerciseType;
  primary_muscle_group: MuscleGroup;
  secondary_muscle_groups: MuscleGroup[];
  is_custom: boolean;
}

export interface ExerciseHistoryEntry {
  workout_id: string;
  workout_title: string;
  workout_start_time: string;
  workout_end_time: string;
  exercise_template_id: string;
  weight_kg: number | null;
  reps: number | null;
  distance_meters: number | null;
  duration_seconds: number | null;
  rpe: number | null;
  custom_metric: number | null;
  set_type: SetType;
}

// Paginated responses
export interface PaginatedResponse<T> {
  page: number;
  page_count: number;
}

export interface WorkoutsResponse extends PaginatedResponse<Workout> {
  workouts: Workout[];
}

export interface RoutinesResponse extends PaginatedResponse<Routine> {
  routines: Routine[];
}

export interface ExerciseTemplatesResponse extends PaginatedResponse<ExerciseTemplate> {
  exercise_templates: ExerciseTemplate[];
}

export interface RoutineFoldersResponse extends PaginatedResponse<RoutineFolder> {
  routine_folders?: RoutineFolder[];
  // API sometimes returns 'routines' key for empty results
  routines?: RoutineFolder[];
}

export interface ExerciseHistoryResponse extends PaginatedResponse<ExerciseHistoryEntry> {
  exercise_history: ExerciseHistoryEntry[];
}

export interface WorkoutCountResponse {
  workout_count: number;
}

// Workout events (for sync)
export interface UpdatedWorkoutEvent {
  type: "updated";
  workout: Workout;
}

export interface DeletedWorkoutEvent {
  type: "deleted";
  id: string;
  deleted_at: string;
}

export type WorkoutEvent = UpdatedWorkoutEvent | DeletedWorkoutEvent;

export interface WorkoutEventsResponse extends PaginatedResponse<WorkoutEvent> {
  events: WorkoutEvent[];
}

// Request types for creating/updating
export interface CreateSetRequest {
  type: SetType;
  weight_kg?: number | null;
  reps?: number | null;
  distance_meters?: number | null;
  duration_seconds?: number | null;
  custom_metric?: number | null;
  rpe?: number | null;
  rep_range?: RepRange | null;
}

export interface CreateExerciseRequest {
  exercise_template_id: string;
  superset_id?: number | null;
  notes?: string | null;
  rest_seconds?: number | null;
  sets: CreateSetRequest[];
}

export interface CreateWorkoutRequest {
  workout: {
    title: string;
    description?: string | null;
    start_time: string;
    end_time: string;
    is_private?: boolean;
    exercises: CreateExerciseRequest[];
  };
}

export interface CreateRoutineRequest {
  routine: {
    title: string;
    folder_id?: number | null;
    notes?: string;
    exercises: CreateExerciseRequest[];
  };
}

export interface UpdateRoutineRequest {
  routine: {
    title: string;
    notes?: string | null;
    exercises: CreateExerciseRequest[];
  };
}

export interface CreateRoutineFolderRequest {
  routine_folder: {
    title: string;
  };
}

export interface CreateExerciseTemplateRequest {
  exercise: {
    title: string;
    exercise_type: ExerciseType;
    equipment_category: EquipmentCategory;
    muscle_group: MuscleGroup;
    other_muscles?: MuscleGroup[];
  };
}
