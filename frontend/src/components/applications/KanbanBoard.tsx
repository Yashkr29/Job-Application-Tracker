import type { JobApplication } from "../../types/api";
import { statusLabel, statuses } from "../../utils/status";
import { ApplicationCard } from "./ApplicationCard";

export function KanbanBoard({ applications }: { applications: JobApplication[] }): JSX.Element {
  return (
    <div className="grid gap-3 overflow-x-auto pb-3 md:grid-cols-3 xl:grid-cols-5">
      {statuses.slice(0, 10).map((status) => {
        const items = applications.filter((item) => item.status === status);
        return (
          <section key={status} className="min-w-64 rounded-app border border-border bg-muted p-3">
            <div className="mb-3 flex items-center justify-between">
              <h2 className="text-sm font-semibold text-text">{statusLabel(status)}</h2>
              <span className="text-xs text-subdued">{items.length}</span>
            </div>
            <div className="space-y-3">
              {items.map((item) => (
                <ApplicationCard key={item.id} application={item} />
              ))}
            </div>
          </section>
        );
      })}
    </div>
  );
}

