import { forwardRef, type ButtonHTMLAttributes } from "react";

import { cn } from "../../utils/cn";

type ButtonProps = ButtonHTMLAttributes<HTMLButtonElement> & {
  variant?: "primary" | "secondary" | "ghost" | "danger";
};

export const Button = forwardRef<HTMLButtonElement, ButtonProps>(({ className, variant = "primary", ...props }, ref) => {
  const variants = {
    primary: "bg-primary text-background hover:opacity-90",
    secondary: "bg-muted text-text hover:bg-border",
    ghost: "bg-transparent text-text hover:bg-muted",
    danger: "bg-danger text-background hover:opacity-90",
  };
  return (
    <button
      ref={ref}
      className={cn("inline-flex h-10 items-center justify-center rounded-app px-4 text-sm font-medium transition disabled:opacity-50", variants[variant], className)}
      {...props}
    />
  );
});

Button.displayName = "Button";

