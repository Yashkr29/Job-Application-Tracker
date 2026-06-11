import { api } from "./client";
import type { ApiResponse, ApplicationList, ApplicationStatus, JobApplication } from "../types/api";

export type ApplicationPayload = {
  title: string;
  company: string;
  location?: string;
  source?: string;
  status?: ApplicationStatus;
  priority?: "low" | "medium" | "high" | "dream";
};

export async function listApplications(search = ""): Promise<ApplicationList> {
  const response = await api.get<ApiResponse<ApplicationList>>("/applications/", { params: { search } });
  return response.data.data;
}

export async function createApplication(payload: ApplicationPayload): Promise<JobApplication> {
  const response = await api.post<ApiResponse<JobApplication>>("/applications/", payload);
  return response.data.data;
}

export async function updateApplicationStatus(id: string, status: ApplicationStatus): Promise<JobApplication> {
  const response = await api.patch<ApiResponse<JobApplication>>(`/applications/${id}/status`, { status });
  return response.data.data;
}

export async function upcomingApplications(): Promise<JobApplication[]> {
  const response = await api.get<ApiResponse<JobApplication[]>>("/applications/upcoming");
  return response.data.data;
}

