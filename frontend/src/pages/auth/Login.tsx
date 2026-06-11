import { zodResolver } from "@hookform/resolvers/zod";
import { useMutation } from "@tanstack/react-query";
import { useForm } from "react-hook-form";
import toast from "react-hot-toast";
import { Link, useNavigate } from "react-router-dom";
import { z } from "zod";

import { login } from "../../api/auth";
import { Button } from "../../components/ui/button";
import { Card } from "../../components/ui/card";
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
    <div className="flex min-h-screen items-center justify-center bg-background p-4">
      <Card className="w-full max-w-sm">
        <h1 className="mb-1 text-xl font-semibold text-text">Welcome back</h1>
        <p className="mb-6 text-sm text-subdued">Track every role from saved to offer.</p>
        <form className="space-y-3" onSubmit={handleSubmit((values) => mutation.mutate(values))}>
          <Input placeholder="Email" type="email" {...register("email")} />
          <Input placeholder="Password" type="password" {...register("password")} />
          <Button className="w-full" disabled={mutation.isPending}>
            Sign in
          </Button>
        </form>
        <Link className="mt-4 block text-sm text-primary" to="/register">
          Create an account
        </Link>
      </Card>
    </div>
  );
}

