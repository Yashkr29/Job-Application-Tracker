import { Outlet } from "react-router-dom";

import { Sidebar } from "./Sidebar";

export function AppShell(): JSX.Element {
  return (
    <div className="flex min-h-screen bg-background">
      <Sidebar />
      <Outlet />
    </div>
  );
}

