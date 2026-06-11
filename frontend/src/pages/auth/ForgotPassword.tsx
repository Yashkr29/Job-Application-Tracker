import { AuthFrame } from "../../components/layout/AuthFrame";
import { Button } from "../../components/ui/button";
import { Input } from "../../components/ui/input";

export function ForgotPassword(): JSX.Element {
  return (
    <AuthFrame title="Reset password" subtitle="Recover access to your application tracker.">
      <div className="space-y-4">
        <Input className="h-12 bg-muted/70" placeholder="Enter email" type="email" />
        <Button className="h-12 w-full bg-auth text-background hover:bg-auth-dark">Send OTP</Button>
      </div>
    </AuthFrame>
  );
}
