import { Briefcase } from "lucide-react";

export function EmptyState({ title, action }: { title: string; action?: JSX.Element }): JSX.Element {
  return (
    <div className="flex min-h-64 flex-col items-center justify-center rounded-app border border-dashed border-border bg-surface p-8 text-center">
      <Briefcase className="mb-3 h-8 w-8 text-subdued" />
      <p className="mb-4 text-sm text-subdued">{title}</p>
      {action}
    </div>
  );
}

