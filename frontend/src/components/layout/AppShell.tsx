import { Outlet } from "react-router-dom";

import { TopNav } from "./TopNav";

export function AppShell(): JSX.Element {
  return (
    <div className="min-h-screen bg-background">
      <TopNav />
      <Outlet />
    </div>
  );
}
