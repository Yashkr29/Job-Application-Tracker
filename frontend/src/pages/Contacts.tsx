import { PageWrapper } from "../components/layout/PageWrapper";
import { EmptyState } from "../components/shared/EmptyState";
import { Button } from "../components/ui/button";

export function Contacts(): JSX.Element {
  return (
    <PageWrapper title="Contacts" actions={<Button>Add contact</Button>}>
      <EmptyState title="No recruiters or interviewers saved yet." />
    </PageWrapper>
  );
}

