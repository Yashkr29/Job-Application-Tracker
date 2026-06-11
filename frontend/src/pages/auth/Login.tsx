import { zodResolver } from "@hookform/resolvers/zod";
import { useMutation } from "@tanstack/react-query";
import { useForm } from "react-hook-form";
import toast from "react-hot-toast";
import { Link, useNavigate } from "react-router-dom";
import { z } from "zod";

import { login } from "../../api/auth";
import { AuthFrame } from "../../components/layout/AuthFrame";
import { Button } from "../../components/ui/button";
import { Input } from "../../components/ui/input";

const schema = z.object({
  email: z.string().email(),
  password: z.string().min(1),
});

type FormValues = z.infer<typeof schema>;

export function Login(): JSX.Element {
  const navigate = useNavigate();
  const { register, handleSubmit } = useForm<FormValues>({ resolver: zodResolver(schema) });
  const mutation = useMutation({
    mutationFn: login,
    onSuccess: () => navigate("/"),
    onError: () => toast.error("Login failed"),
  });

  return (
    <AuthFrame title="Welcome back" subtitle="Sign in to continue tracking your job search.">
      <form className="space-y-4" onSubmit={handleSubmit((values) => mutation.mutate(values))}>
        <label className="block text-sm font-medium text-text">
          Email
          <Input className="mt-2 h-12 bg-muted/70" placeholder="Enter email" type="email" {...register("email")} />
        </label>
        <label className="block text-sm font-medium text-text">
          <span className="flex items-center justify-between">
            Password
            <Link className="text-xs font-semibold text-primary" to="/forgot-password">
              Forgot?
            </Link>
          </span>
          <Input className="mt-2 h-12 bg-muted/70" placeholder="Enter password" type="password" {...register("password")} />
        </label>
        <Button className="h-12 w-full bg-auth text-background hover:bg-auth-dark" disabled={mutation.isPending}>
          Sign in
        </Button>
      </form>
      <p className="mt-6 text-center text-sm text-subdued">
        New here?{" "}
        <Link className="font-semibold text-primary" to="/register">
          Create account
        </Link>
      </p>
    </AuthFrame>
  );
}
