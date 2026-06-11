import { useQuery } from "@tanstack/react-query";

import { listApplications, upcomingApplications } from "../api/applications";
import { overviewStats } from "../api/stats";
import { JobSearchBoard } from "../components/applications/JobSearchBoard";
import { PageWrapper } from "../components/layout/PageWrapper";
import { Skeleton } from "../components/shared/Skeleton";
import { StatCard } from "../components/stats/StatCard";

export function Dashboard(): JSX.Element {
  const stats = useQuery({ queryKey: ["stats", "overview"], queryFn: overviewStats });
  const recent = useQuery({ queryKey: ["applications", "recent"], queryFn: () => listApplications("") });
  const upcoming = useQuery({ queryKey: ["applications", "upcoming"], queryFn: upcomingApplications });

  return (
    <PageWrapper title="Find Jobs">
      <div className="grid gap-3 md:grid-cols-4">
        {stats.data ? (
          <>
            <StatCard label="Total apps" value={stats.data.total} />
            <StatCard label="This week" value={stats.data.this_week} />
            <StatCard label="Interviews" value={stats.data.interviews_next_7_days} />
            <StatCard label="Response rate" value={`${Math.round(stats.data.response_rate * 100)}%`} />
          </>
        ) : (
          Array.from({ length: 4 }).map((_, index) => <Skeleton key={index} className="h-28" />)
        )}
      </div>
      <div className="mt-5">
        <JobSearchBoard applications={recent.data?.items.length ? recent.data.items : upcoming.data ?? []} />
      </div>
    </PageWrapper>
  );
}
