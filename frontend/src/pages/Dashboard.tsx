import { useQuery } from "@tanstack/react-query";

import { listApplications, upcomingApplications } from "../api/applications";
import { overviewStats } from "../api/stats";
import { ApplicationCard } from "../components/applications/ApplicationCard";
import { PageWrapper } from "../components/layout/PageWrapper";
import { EmptyState } from "../components/shared/EmptyState";
import { Skeleton } from "../components/shared/Skeleton";
import { StatCard } from "../components/stats/StatCard";

export function Dashboard(): JSX.Element {
  const stats = useQuery({ queryKey: ["stats", "overview"], queryFn: overviewStats });
  const recent = useQuery({ queryKey: ["applications", "recent"], queryFn: () => listApplications("") });
  const upcoming = useQuery({ queryKey: ["applications", "upcoming"], queryFn: upcomingApplications });

  return (
    <PageWrapper title="Dashboard">
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
      <div className="mt-5 grid gap-4 xl:grid-cols-[1.5fr_1fr]">
        <section>
          <h2 className="mb-3 font-semibold text-text">Recent applications</h2>
          <div className="space-y-3">
            {recent.data?.items.length ? recent.data.items.slice(0, 5).map((item) => <ApplicationCard key={item.id} application={item} />) : <EmptyState title="No applications yet." />}
          </div>
        </section>
        <section>
          <h2 className="mb-3 font-semibold text-text">Upcoming interviews</h2>
          <div className="space-y-3">
            {upcoming.data?.length ? upcoming.data.map((item) => <ApplicationCard key={item.id} application={item} />) : <EmptyState title="No interviews scheduled." />}
          </div>
        </section>
      </div>
    </PageWrapper>
  );
}

