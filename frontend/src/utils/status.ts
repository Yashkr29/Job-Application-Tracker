import type { ApplicationStatus } from "../types/api";

export const statuses: ApplicationStatus[] = [
  "SAVED",
  "APPLIED",
  "PHONE_SCREEN",
  "INTERVIEW",
  "TECHNICAL",
  "FINAL_ROUND",
  "OFFER",
  "REJECTED",
  "WITHDRAWN",
  "GHOSTED",
];

export function statusLabel(status: ApplicationStatus): string {
  return status
    .split("_")
    .map((part) => part[0] + part.slice(1).toLowerCase())
    .join(" ");
}

