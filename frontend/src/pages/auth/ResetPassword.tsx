import { AuthFrame } from "../../components/layout/AuthFrame";
import { Button } from "../../components/ui/button";
import { Input } from "../../components/ui/input";

export function ResetPassword(): JSX.Element {
  return (
    <AuthFrame title="Set new password" subtitle="Enter your OTP and choose a fresh password.">
      <div className="space-y-4">
        <Input placeholder="Email" type="email" />
        <Input placeholder="6-digit OTP" />
        <Input placeholder="New password" type="password" />
        <Button className="w-full bg-auth text-background hover:bg-auth-dark">Update password</Button>
      </div>
    </AuthFrame>
  );
}
