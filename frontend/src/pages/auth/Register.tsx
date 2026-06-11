import { zodResolver } from "@hookform/resolvers/zod";
import { useMutation } from "@tanstack/react-query";
import { useForm } from "react-hook-form";
import toast from "react-hot-toast";
import { Link, useNavigate } from "react-router-dom";
import { z } from "zod";

import { register as registerUser } from "../../api/auth";
import { Button } from "../../components/ui/button";
import { Card } from "../../components/ui/card";
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
    <div className="flex min-h-screen items-center justify-center bg-background p-4">
      <Card className="w-full max-w-sm">
        <h1 className="mb-6 text-xl font-semibold text-text">Create account</h1>
        <form className="space-y-3" onSubmit={handleSubmit((values) => mutation.mutate(values))}>
          <Input placeholder="Name" {...register("name")} />
          <Input placeholder="Email" type="email" {...register("email")} />
          <Input placeholder="Password" type="password" {...register("password")} />
          <Button className="w-full" disabled={mutation.isPending}>
            Register
          </Button>
        </form>
        <Link className="mt-4 block text-sm text-primary" to="/login">
          Already have an account?
        </Link>
      </Card>
    </div>
  );
}

