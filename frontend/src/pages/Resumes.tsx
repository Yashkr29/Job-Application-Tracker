import { PageWrapper } from "../components/layout/PageWrapper";
import { EmptyState } from "../components/shared/EmptyState";
import { Button } from "../components/ui/button";

export function Resumes(): JSX.Element {
  return (
    <PageWrapper title="Resumes" actions={<Button>Upload PDF</Button>}>
      <EmptyState title="Upload resume versions and link them to applications." />
    </PageWrapper>
  );
}

