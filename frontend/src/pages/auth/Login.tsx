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
    <AuthFrame title="Sign in to your account">
      <form className="space-y-4" onSubmit={handleSubmit((values) => mutation.mutate(values))}>
        <label className="block text-xs font-medium text-text">
          Email
          <Input placeholder="Email" type="email" {...register("email")} />
        </label>
        <label className="block text-xs font-medium text-text">
          Password
          <Input placeholder="Password" type="password" {...register("password")} />
        </label>
        <Button className="w-full bg-auth text-background hover:bg-auth-dark" disabled={mutation.isPending}>
          Sign in
        </Button>
      </form>
      <div className="my-6 flex items-center gap-3 text-xs text-subdued">
        <span className="h-px flex-1 bg-border" />
        Sign in with
        <span className="h-px flex-1 bg-border" />
      </div>
      <div className="flex justify-center gap-6 text-lg font-semibold">
        <span className="text-auth">f</span>
        <span>X</span>
        <span className="text-accent">G</span>
        <span>Apple</span>
      </div>
      <p className="mt-5 text-center text-xs text-subdued">
        New here?{" "}
        <Link className="font-semibold text-primary" to="/register">
          Create account
        </Link>
      </p>
    </AuthFrame>
  );
}
