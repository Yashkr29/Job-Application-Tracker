import { api } from "./client";
import type { ApiResponse, ChartDatum, OverviewStats } from "../types/api";

export async function overviewStats(): Promise<OverviewStats> {
  const response = await api.get<ApiResponse<OverviewStats>>("/stats/overview");
  return response.data.data;
}

export async function funnelStats(): Promise<ChartDatum[]> {
  const response = await api.get<ApiResponse<ChartDatum[]>>("/stats/funnel");
  return response.data.data;
}

export async function sourceStats(): Promise<ChartDatum[]> {
  const response = await api.get<ApiResponse<ChartDatum[]>>("/stats/sources");
  return response.data.data;
}

export async function timelineStats(): Promise<ChartDatum[]> {
  const response = await api.get<ApiResponse<ChartDatum[]>>("/stats/timeline");
  return response.data.data;
}

