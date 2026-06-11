import { useQuery } from "@tanstack/react-query";
import { Bar, BarChart, CartesianGrid, Pie, PieChart, ResponsiveContainer, Tooltip, XAxis, YAxis } from "recharts";

import { funnelStats, sourceStats, timelineStats } from "../api/stats";
import { PageWrapper } from "../components/layout/PageWrapper";
import { Card } from "../components/ui/card";

export function Stats(): JSX.Element {
  const funnel = useQuery({ queryKey: ["stats", "funnel"], queryFn: funnelStats });
  const sources = useQuery({ queryKey: ["stats", "sources"], queryFn: sourceStats });
  const timeline = useQuery({ queryKey: ["stats", "timeline"], queryFn: timelineStats });

  return (
    <PageWrapper title="Stats">
      <div className="grid gap-4 xl:grid-cols-2">
        <Card className="h-80">
          <h2 className="mb-3 font-semibold text-text">Pipeline funnel</h2>
          <ResponsiveContainer width="100%" height="85%">
            <BarChart data={funnel.data ?? []}>
              <CartesianGrid stroke="var(--color-border)" />
              <XAxis dataKey="status" stroke="var(--color-subdued)" />
              <YAxis stroke="var(--color-subdued)" />
              <Tooltip />
              <Bar dataKey="count" fill="var(--color-primary)" radius={[4, 4, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </Card>
        <Card className="h-80">
          <h2 className="mb-3 font-semibold text-text">Sources</h2>
          <ResponsiveContainer width="100%" height="85%">
            <PieChart>
              <Pie data={sources.data ?? []} dataKey="count" nameKey="source" fill="var(--color-accent)" label />
              <Tooltip />
            </PieChart>
          </ResponsiveContainer>
        </Card>
        <Card className="h-80 xl:col-span-2">
          <h2 className="mb-3 font-semibold text-text">Timeline</h2>
          <ResponsiveContainer width="100%" height="85%">
            <BarChart data={timeline.data ?? []}>
              <CartesianGrid stroke="var(--color-border)" />
              <XAxis dataKey="date" stroke="var(--color-subdued)" />
              <YAxis stroke="var(--color-subdued)" />
              <Tooltip />
              <Bar dataKey="count" fill="var(--color-success)" radius={[4, 4, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </Card>
      </div>
    </PageWrapper>
  );
}

