import { AuthFrame } from "../../components/layout/AuthFrame";
import { Button } from "../../components/ui/button";
import { Input } from "../../components/ui/input";

export function ForgotPassword(): JSX.Element {
  return (
    <AuthFrame title="Reset password">
      <div className="space-y-4">
        <p className="text-center text-sm text-subdued">Enter your email and we will send a six digit OTP.</p>
        <Input placeholder="Email" type="email" />
        <Button className="w-full bg-auth text-background hover:bg-auth-dark">Send OTP</Button>
      </div>
    </AuthFrame>
  );
}
