import { formatDistanceToNow } from "date-fns";

import { Badge } from "../ui/badge";
import { Card } from "../ui/card";
import type { JobApplication } from "../../types/api";
import { statusLabel } from "../../utils/status";

export function ApplicationCard({ application }: { application: JobApplication }): JSX.Element {
  return (
    <Card className="space-y-3">
      <div className="flex items-start justify-between gap-3">
        <div>
          <h3 className="font-medium text-text">{application.title}</h3>
          <p className="text-sm text-subdued">{application.company}</p>
        </div>
        <Badge>{statusLabel(application.status)}</Badge>
      </div>
      <div className="flex flex-wrap gap-2 text-xs text-subdued">
        {application.location && <span>{application.location}</span>}
        {application.source && <span>{application.source}</span>}
        <span>{formatDistanceToNow(new Date(application.created_at), { addSuffix: true })}</span>
      </div>
    </Card>
  );
}

