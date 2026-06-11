import type { ReactNode } from "react";

export function PageWrapper({ title, children, actions }: { title: string; children: ReactNode; actions?: ReactNode }): JSX.Element {
  return (
    <main className="mx-auto min-h-screen max-w-7xl overflow-auto p-4 md:p-6">
      <div className="mb-5 flex flex-wrap items-center justify-between gap-3">
        <h1 className="text-2xl font-semibold tracking-normal text-text">{title}</h1>
        {actions}
      </div>
      {children}
    </main>
  );
}
