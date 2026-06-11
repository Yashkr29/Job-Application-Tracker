import { PageWrapper } from "../components/layout/PageWrapper";
import { Card } from "../components/ui/card";
import { Button } from "../components/ui/button";
import { Input } from "../components/ui/input";

export function Settings(): JSX.Element {
  return (
    <PageWrapper title="Settings">
      <div className="grid gap-4 xl:grid-cols-2">
        <Card className="space-y-3">
          <h2 className="font-semibold text-text">Profile</h2>
          <Input placeholder="Name" />
          <Input placeholder="Email" />
          <Button>Save profile</Button>
        </Card>
        <Card className="space-y-3">
          <h2 className="font-semibold text-text">Change password</h2>
          <Input placeholder="Current password" type="password" />
          <Input placeholder="New password" type="password" />
          <Button>Update password</Button>
        </Card>
        <Card className="space-y-3 xl:col-span-2">
          <h2 className="font-semibold text-danger">Danger zone</h2>
          <Button variant="danger">Delete account</Button>
        </Card>
      </div>
    </PageWrapper>
  );
}

