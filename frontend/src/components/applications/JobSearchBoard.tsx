import { Bookmark, MapPin, Plus, Search, SlidersHorizontal } from "lucide-react";
import { useMemo, useState } from "react";

import type { ApplicationStatus, JobApplication, Priority } from "../../types/api";
import { statuses, statusLabel } from "../../utils/status";
import { Badge } from "../ui/badge";
import { Button } from "../ui/button";
import { Input } from "../ui/input";

const priorityOptions: Priority[] = ["low", "medium", "high", "dream"];

function relativeTime(iso: string): string {
  const hours = Math.max(1, Math.round((Date.now() - new Date(iso).getTime()) / 3_600_000));
  if (hours < 24) {
    return `${hours} hour${hours === 1 ? "" : "s"} ago`;
  }
  const days = Math.round(hours / 24);
  return `${days} day${days === 1 ? "" : "s"} ago`;
}

function logoColor(index: number): string {
  const colors = ["bg-primary", "bg-text", "bg-accent", "bg-success", "bg-danger", "bg-subdued"];
  return colors[index % colors.length];
}

export function JobSearchBoard({ applications, onAddApplication }: { applications: JobApplication[]; onAddApplication?: () => void }): JSX.Element {
  const [search, setSearch] = useState("");
  const [location, setLocation] = useState("");
  const [statusFilter, setStatusFilter] = useState<ApplicationStatus | "ALL">("ALL");
  const [priorityFilter, setPriorityFilter] = useState<Priority | "ALL">("ALL");
  const filteredJobs = useMemo(() => {
    const term = search.trim().toLowerCase();
    const locationTerm = location.trim().toLowerCase();
    return applications.filter((job) => {
      const matchesSearch = !term || `${job.title} ${job.company} ${job.source ?? ""} ${job.description ?? ""}`.toLowerCase().includes(term);
      const matchesLocation = !locationTerm || (job.location ?? "").toLowerCase().includes(locationTerm);
      const matchesStatus = statusFilter === "ALL" || job.status === statusFilter;
      const matchesPriority = priorityFilter === "ALL" || job.priority === priorityFilter;
      return matchesSearch && matchesLocation && matchesStatus && matchesPriority;
    });
  }, [applications, location, priorityFilter, search, statusFilter]);

  return (
    <div className="overflow-hidden rounded-app bg-surface shadow-soft">
      <section className="relative overflow-hidden bg-hero px-6 pb-6 pt-5 md:px-10 md:pb-8">
        <div className="mb-8 flex items-center justify-between gap-4">
          <nav className="hidden items-center gap-6 text-sm md:flex">
            <span className="border-t-2 border-text pt-3 font-semibold text-text">Pipeline</span>
            <span className="text-subdued">Upcoming interviews</span>
            <span className="text-subdued">Follow-ups</span>
            <span className="text-subdued">Resume links</span>
          </nav>
          <div className="ml-auto hidden gap-4 md:flex">
            <div className="portrait-tile h-20 w-14 rounded-app bg-surface shadow-soft" style={{ "--tilt": "-15deg" } as React.CSSProperties} />
            <div className="portrait-tile h-20 w-14 rounded-app bg-muted shadow-soft" style={{ "--tilt": "8deg" } as React.CSSProperties} />
            <div className="portrait-tile h-20 w-20 rounded-app bg-border shadow-soft" style={{ "--tilt": "18deg" } as React.CSSProperties} />
          </div>
        </div>
        <h1 className="mb-5 max-w-md text-2xl font-bold text-text md:text-3xl">Track Every Job Application Here</h1>
        <div className="relative z-10 grid gap-3 rounded-[28px] bg-surface p-2 shadow-soft md:grid-cols-[1fr_1fr_auto]">
          <label className="flex items-center gap-3 border-border px-3 md:border-r">
            <Search className="h-5 w-5 text-subdued" />
            <Input
              className="border-0 bg-transparent shadow-none focus:border-0"
              placeholder="Role, company, tag, or note"
              value={search}
              onChange={(event) => setSearch(event.target.value)}
            />
          </label>
          <label className="flex items-center gap-3 px-3">
            <MapPin className="h-5 w-5 text-subdued" />
            <Input
              className="border-0 bg-transparent shadow-none focus:border-0"
              placeholder="Location or work mode"
              value={location}
              onChange={(event) => setLocation(event.target.value)}
            />
          </label>
          <Button className="h-12 rounded-[24px] px-10" type="button">
            Search apps
          </Button>
        </div>
      </section>

      <div className="flex gap-2 overflow-x-auto border-b border-border bg-surface px-4 py-3">
        <button
          className={`shrink-0 rounded-app border px-3 py-1 text-xs ${statusFilter === "ALL" ? "border-primary bg-primary text-background" : "border-border text-text hover:bg-muted"}`}
          onClick={() => setStatusFilter("ALL")}
          type="button"
        >
          All
        </button>
        {statuses.map((status) => (
          <button
            key={status}
            className={`shrink-0 rounded-app border px-3 py-1 text-xs ${statusFilter === status ? "border-primary bg-primary text-background" : "border-border text-text hover:bg-muted"}`}
            onClick={() => setStatusFilter(status)}
            type="button"
          >
            {statusLabel(status)}
          </button>
        ))}
      </div>

      <section className="grid gap-5 bg-surface p-4 md:grid-cols-[230px_1fr]">
        <aside className="space-y-6 text-sm">
          <div className="flex items-center justify-between">
            <h2 className="font-semibold text-text">Filter</h2>
            <SlidersHorizontal className="h-4 w-4 text-subdued" />
          </div>
          <Input placeholder="Company, source, note..." value={search} onChange={(event) => setSearch(event.target.value)} />
          <div>
            <h3 className="mb-3 font-semibold text-text">Pipeline stage</h3>
            <div className="space-y-2">
              {(["APPLIED", "INTERVIEW", "OFFER"] as ApplicationStatus[]).map((status) => (
                <button
                  key={status}
                  className={`block w-full rounded-app px-3 py-2 text-left text-sm ${statusFilter === status ? "bg-primary text-background" : "text-subdued hover:bg-muted hover:text-text"}`}
                  onClick={() => setStatusFilter(statusFilter === status ? "ALL" : status)}
                  type="button"
                >
                  {statusLabel(status)}
                </button>
              ))}
            </div>
          </div>
          <div>
            <h3 className="mb-3 font-semibold text-text">Priority</h3>
            <div className="space-y-2">
              <button
                className={`block w-full rounded-app px-3 py-2 text-left text-sm ${priorityFilter === "ALL" ? "bg-muted text-text" : "text-subdued hover:bg-muted hover:text-text"}`}
                onClick={() => setPriorityFilter("ALL")}
                type="button"
              >
                All priorities
              </button>
              {priorityOptions.map((priority) => (
                <button
                  key={priority}
                  className={`block w-full rounded-app px-3 py-2 text-left text-sm capitalize ${priorityFilter === priority ? "bg-primary text-background" : "text-subdued hover:bg-muted hover:text-text"}`}
                  onClick={() => setPriorityFilter(priority)}
                  type="button"
                >
                  {priority}
                </button>
              ))}
            </div>
          </div>
        </aside>

        <div className="space-y-2">
          {filteredJobs.length === 0 && (
            <div className="flex min-h-72 flex-col items-center justify-center rounded-app border border-dashed border-border bg-muted p-8 text-center">
              <p className="text-base font-semibold text-text">No applications found</p>
              <p className="mt-2 max-w-sm text-sm text-subdued">
                Add your first application or clear the filters to see tracked roles from the backend.
              </p>
              {onAddApplication && (
                <Button className="mt-5" onClick={onAddApplication} type="button">
                  <Plus className="mr-2 h-4 w-4" />
                  Add application
                </Button>
              )}
            </div>
          )}
          {filteredJobs.map((job, index) => (
            <article key={job.id} className="grid items-center gap-3 rounded-app px-3 py-3 transition hover:bg-muted md:grid-cols-[1fr_auto_auto_auto]">
              <div className="flex items-center gap-4">
                <div className={`flex h-10 w-10 items-center justify-center rounded-app text-sm font-bold text-background ${logoColor(index)}`}>
                  {job.company.slice(0, 1)}
                </div>
                <div>
                  <h3 className="font-semibold text-text">{job.title}</h3>
                  <p className="text-xs text-subdued">{job.company}</p>
                </div>
              </div>
              <div className="flex flex-wrap gap-2">
                <Badge>{job.priority}</Badge>
                <Badge>{statusLabel(job.status)}</Badge>
                <Badge>{job.source ?? "Manual"}</Badge>
              </div>
              <p className="text-sm font-medium text-text">{job.location ?? "Remote"}</p>
              <div className="flex items-center justify-between gap-5">
                <span className="text-xs text-subdued">{relativeTime(job.created_at)}</span>
                <Bookmark className="h-5 w-5 text-text" />
              </div>
            </article>
          ))}
        </div>
      </section>
    </div>
  );
}
