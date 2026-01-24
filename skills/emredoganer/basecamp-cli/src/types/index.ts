export interface BasecampTokens {
  access_token: string;
  refresh_token: string;
  expires_at: number;
}

export interface BasecampAccount {
  id: number;
  name: string;
  product: string;
  href: string;
  app_href: string;
}

export interface BasecampIdentity {
  id: number;
  first_name: string;
  last_name: string;
  email_address: string;
}

export interface BasecampAuthorization {
  expires_at: string;
  identity: BasecampIdentity;
  accounts: BasecampAccount[];
}

export interface BasecampProject {
  id: number;
  status: string;
  created_at: string;
  updated_at: string;
  name: string;
  description: string;
  purpose: string;
  clients_enabled: boolean;
  bookmark_url: string;
  url: string;
  app_url: string;
  dock: BasecampDock[];
  bookmarked: boolean;
}

export interface BasecampDock {
  id: number;
  title: string;
  name: string;
  enabled: boolean;
  position: number;
  url: string;
  app_url: string;
}

export interface BasecampTodoList {
  id: number;
  status: string;
  visible_to_clients: boolean;
  created_at: string;
  updated_at: string;
  title: string;
  inherits_status: boolean;
  type: string;
  url: string;
  app_url: string;
  bookmark_url: string;
  subscription_url: string;
  comments_count: number;
  comments_url: string;
  parent: BasecampParent;
  bucket: BasecampBucket;
  creator: BasecampPerson;
  description: string;
  completed: boolean;
  completed_ratio: string;
  name: string;
  todos_url: string;
  groups_url: string;
  app_todos_url: string;
}

export interface BasecampTodo {
  id: number;
  status: string;
  visible_to_clients: boolean;
  created_at: string;
  updated_at: string;
  title: string;
  inherits_status: boolean;
  type: string;
  url: string;
  app_url: string;
  bookmark_url: string;
  subscription_url: string;
  comments_count: number;
  comments_url: string;
  parent: BasecampParent;
  bucket: BasecampBucket;
  creator: BasecampPerson;
  description: string;
  completed: boolean;
  content: string;
  starts_on: string | null;
  due_on: string | null;
  assignees: BasecampPerson[];
  completion_subscribers: BasecampPerson[];
  completion_url: string;
  completion?: {
    created_at: string;
    creator: BasecampPerson;
  };
}

export interface BasecampParent {
  id: number;
  title: string;
  type: string;
  url: string;
  app_url: string;
}

export interface BasecampBucket {
  id: number;
  name: string;
  type: string;
}

export interface BasecampPerson {
  id: number;
  attachable_sgid: string;
  name: string;
  email_address: string;
  personable_type: string;
  title: string;
  bio: string | null;
  location: string | null;
  created_at: string;
  updated_at: string;
  admin: boolean;
  owner: boolean;
  client: boolean;
  employee: boolean;
  time_zone: string;
  avatar_url: string;
  company?: BasecampCompany;
  can_manage_projects: boolean;
  can_manage_people: boolean;
}

export interface BasecampCompany {
  id: number;
  name: string;
}

export interface BasecampMessage {
  id: number;
  status: string;
  visible_to_clients: boolean;
  created_at: string;
  updated_at: string;
  title: string;
  inherits_status: boolean;
  type: string;
  url: string;
  app_url: string;
  bookmark_url: string;
  subscription_url: string;
  comments_count: number;
  comments_url: string;
  parent: BasecampParent;
  bucket: BasecampBucket;
  creator: BasecampPerson;
  content: string;
  subject: string;
}

export interface BasecampCampfire {
  id: number;
  status: string;
  visible_to_clients: boolean;
  created_at: string;
  updated_at: string;
  title: string;
  inherits_status: boolean;
  type: string;
  url: string;
  app_url: string;
  bookmark_url: string;
  subscription_url: string;
  lines_url: string;
  bucket: BasecampBucket;
  topic: string;
}

export interface BasecampCampfireLine {
  id: number;
  status: string;
  visible_to_clients: boolean;
  created_at: string;
  updated_at: string;
  title: string;
  inherits_status: boolean;
  type: string;
  url: string;
  app_url: string;
  parent: BasecampParent;
  bucket: BasecampBucket;
  creator: BasecampPerson;
  content: string;
}

export interface BasecampConfig {
  tokens?: BasecampTokens;
  currentAccountId?: number;
  clientId?: string;
  redirectUri?: string;
  // Note: clientSecret is intentionally NOT stored in config for security.
  // It must be provided via BASECAMP_CLIENT_SECRET environment variable.
}

export interface PaginatedResponse<T> {
  data: T[];
  nextPage?: string;
  totalCount?: number;
}
