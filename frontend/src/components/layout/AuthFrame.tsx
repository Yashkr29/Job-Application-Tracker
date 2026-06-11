import { Rocket } from "lucide-react";
import type { ReactNode } from "react";

export function AuthFrame({ children, subtitle, title }: { children: ReactNode; subtitle?: string; title: string }): JSX.Element {
  return (
    <div className="flex min-h-screen items-center justify-center bg-soft-blue p-4">
      <section className="grid w-full max-w-5xl overflow-hidden rounded-app bg-surface shadow-soft md:grid-cols-[1.05fr_1fr]">
        <div className="auth-wave relative hidden min-h-[520px] flex-col items-center justify-center px-12 text-center text-background md:flex">
          <p className="mb-12 text-lg font-medium">Welcome to</p>
          <div className="relative z-10 mb-5 flex h-24 w-24 items-center justify-center rounded-full bg-surface text-auth shadow-soft">
            <Rocket className="h-12 w-12" />
          </div>
          <h2 className="relative z-10 text-lg font-semibold">JobTrackr</h2>
          <p className="relative z-10 mt-10 max-w-xs text-sm leading-6 text-background/85">
            Track applications, interviews, resumes, contacts, reminders, and offers from one focused workspace.
          </p>
          <div className="relative z-10 mt-24 flex gap-5 text-[10px] uppercase tracking-wide text-background/80">
            <span>Pipeline</span>
            <span>Analytics</span>
            <span>Reminders</span>
          </div>
        </div>
        <div className="flex min-h-[520px] items-center justify-center p-8 md:p-12">
          <div className="w-full max-w-sm">
            <h1 className="mb-2 text-center text-xl font-bold text-text">{title}</h1>
            {subtitle && <p className="mb-7 text-center text-sm text-subdued">{subtitle}</p>}
            {children}
          </div>
        </div>
      </section>
    </div>
  );
}
