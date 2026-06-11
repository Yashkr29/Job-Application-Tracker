import type { HTMLAttributes } from "react";

import { cn } from "../../utils/cn";

export function Badge({ className, ...props }: HTMLAttributes<HTMLSpanElement>): JSX.Element {
  return <span className={cn("inline-flex rounded-app bg-muted px-2 py-1 text-xs font-medium text-subdued", className)} {...props} />;
}

