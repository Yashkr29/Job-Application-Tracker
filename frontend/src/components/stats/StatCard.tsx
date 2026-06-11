import { Card } from "../ui/card";

export function StatCard({ label, value }: { label: string; value: string | number }): JSX.Element {
  return (
    <Card>
      <p className="text-sm text-subdued">{label}</p>
      <p className="mt-2 text-2xl font-semibold text-text">{value}</p>
    </Card>
  );
}

