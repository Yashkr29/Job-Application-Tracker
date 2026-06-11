import { Card } from "../../components/ui/card";
import { Input } from "../../components/ui/input";
import { Button } from "../../components/ui/button";

export function ForgotPassword(): JSX.Element {
  return (
    <div className="flex min-h-screen items-center justify-center bg-background p-4">
      <Card className="w-full max-w-sm space-y-3">
        <h1 className="text-xl font-semibold text-text">Reset password</h1>
        <Input placeholder="Email" type="email" />
        <Button className="w-full">Send OTP</Button>
      </Card>
    </div>
  );
}

