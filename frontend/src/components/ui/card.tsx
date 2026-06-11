import type { HTMLAttributes } from "react";

import { cn } from "../../utils/cn";

export function Card({ className, ...props }: HTMLAttributes<HTMLDivElement>): JSX.Element {
  return <div className={cn("rounded-app border border-border bg-surface p-4 shadow-soft", className)} {...props} />;
}

