import { Button } from "../../components/ui/button";
import { Card } from "../../components/ui/card";
import { Input } from "../../components/ui/input";

export function ResetPassword(): JSX.Element {
  return (
    <div className="flex min-h-screen items-center justify-center bg-background p-4">
      <Card className="w-full max-w-sm space-y-3">
        <h1 className="text-xl font-semibold text-text">Set new password</h1>
        <Input placeholder="Email" type="email" />
        <Input placeholder="6-digit OTP" />
        <Input placeholder="New password" type="password" />
        <Button className="w-full">Update password</Button>
      </Card>
    </div>
  );
}

