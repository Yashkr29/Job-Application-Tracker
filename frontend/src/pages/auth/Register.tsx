import { zodResolver } from "@hookform/resolvers/zod";
import { useMutation } from "@tanstack/react-query";
import { useForm } from "react-hook-form";
import toast from "react-hot-toast";
import { Link, useNavigate } from "react-router-dom";
import { z } from "zod";

import { register as registerUser } from "../../api/auth";
import { AuthFrame } from "../../components/layout/AuthFrame";
import { Button } from "../../components/ui/button";
import { Input } from "../../components/ui/input";

const schema = z.object({
  name: z.string().min(2),
  email: z.string().email(),
  password: z.string().min(8),
});

type FormValues = z.infer<typeof schema>;

export function Register(): JSX.Element {
  const navigate = useNavigate();
  const { register, handleSubmit } = useForm<FormValues>({ resolver: zodResolver(schema) });
  const mutation = useMutation({
    mutationFn: registerUser,
    onSuccess: () => {
      toast.success("Account created. Please sign in.");
      navigate("/login");
    },
  });

  return (
    <AuthFrame title="Create your account" subtitle="Start organizing applications, follow-ups, interviews, and resumes.">
      <form className="space-y-4" onSubmit={handleSubmit((values) => mutation.mutate(values))}>
        <label className="block text-xs font-medium text-text">
          Full name
          <Input placeholder="Name" {...register("name")} />
        </label>
        <label className="block text-xs font-medium text-text">
          Email
          <Input placeholder="Email" type="email" {...register("email")} />
        </label>
        <label className="block text-xs font-medium text-text">
          Password
          <Input placeholder="Password" type="password" {...register("password")} />
        </label>
        <label className="flex items-center gap-2 text-xs text-subdued">
          <input className="h-4 w-4 rounded border-border accent-auth" type="checkbox" defaultChecked />
          I agree to the terms and conditions.
        </label>
        <Button className="w-full bg-auth text-background hover:bg-auth-dark" disabled={mutation.isPending}>
          Sign up
        </Button>
      </form>
      <p className="mt-5 text-center text-xs text-subdued">
        Already have an account?{" "}
        <Link className="font-semibold text-primary" to="/login">
          Sign in
        </Link>
      </p>
    </AuthFrame>
  );
}
