import { PageWrapper } from "../components/layout/PageWrapper";
import { Card } from "../components/ui/card";

export function ApplicationDetail(): JSX.Element {
  return (
    <PageWrapper title="Application detail">
      <Card>
        <p className="text-sm text-subdued">Select an application from the list to view timeline, notes, contacts, and resume links.</p>
      </Card>
    </PageWrapper>
  );
}

