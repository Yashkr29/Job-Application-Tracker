import { Rocket } from "lucide-react";
import type { ReactNode } from "react";

export function AuthFrame({ children, subtitle, title }: { children: ReactNode; subtitle?: string; title: string }): JSX.Element {
  return (
    <div className="flex min-h-screen items-center justify-center bg-soft-blue p-4">
      <section className="grid w-full max-w-5xl overflow-hidden rounded-[18px] bg-surface shadow-soft md:grid-cols-[0.95fr_1.05fr]">
        <div className="auth-wave relative hidden min-h-[560px] flex-col justify-between px-12 py-12 text-background md:flex">
          <div className="relative z-10">
            <p className="mb-10 text-sm font-medium text-background/85">Welcome to</p>
            <div className="mb-5 flex h-20 w-20 items-center justify-center rounded-full bg-surface text-auth shadow-soft">
              <Rocket className="h-10 w-10" />
            </div>
            <h2 className="text-3xl font-bold">JobTrackr</h2>
            <p className="mt-5 max-w-xs text-sm leading-6 text-background/85">
              Track applications, interviews, resumes, contacts, reminders, and offers from one focused workspace.
            </p>
          </div>
          <div className="relative z-10 flex gap-5 text-[10px] font-semibold uppercase tracking-wide text-background/80">
            <span>Pipeline</span>
            <span>Analytics</span>
            <span>Reminders</span>
          </div>
        </div>
        <div className="flex min-h-[560px] items-center justify-center px-6 py-10 md:px-14">
          <div className="w-full max-w-sm">
            <h1 className="mb-2 text-2xl font-bold text-text">{title}</h1>
            {subtitle && <p className="mb-8 text-sm leading-6 text-subdued">{subtitle}</p>}
            {children}
          </div>
        </div>
      </section>
    </div>
  );
}
