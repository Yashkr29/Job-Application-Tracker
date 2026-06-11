export type ApiResponse<T> = {
  success: boolean;
  data: T;
  message: string;
};

export type User = {
  id: string;
  email: string;
  name: string;
  is_verified: boolean;
  created_at: string;
};

export type AuthTokens = {
  access_token: string;
  refresh_token: string;
  token_type: "bearer";
  expires_in: number;
  user: User;
};

export type ApplicationStatus =
  | "SAVED"
  | "APPLIED"
  | "PHONE_SCREEN"
  | "INTERVIEW"
  | "TECHNICAL"
  | "FINAL_ROUND"
  | "OFFER"
  | "REJECTED"
  | "WITHDRAWN"
  | "GHOSTED";

export type Priority = "low" | "medium" | "high" | "dream";

export type JobApplication = {
  id: string;
  title: string;
  company: string;
  location: string | null;
  source: string | null;
  job_url: string | null;
  description: string | null;
  status: ApplicationStatus;
  priority: Priority;
  salary_min: number | null;
  salary_max: number | null;
  currency: string;
  applied_at: string | null;
  follow_up_date: string | null;
  interview_at: string | null;
  offer_deadline: string | null;
  created_at: string;
  updated_at: string;
};

export type ApplicationList = {
  items: JobApplication[];
  total: number;
  page: number;
  limit: number;
};

export type OverviewStats = {
  total: number;
  this_week: number;
  this_month: number;
  by_status: Record<string, number>;
  acceptance_rate: number;
  response_rate: number;
  avg_response_days: number;
  streak: number;
  interviews_next_7_days: number;
};

export type ChartDatum = {
  status?: string;
  source?: string;
  date?: string;
  count: number;
};

