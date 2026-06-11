import { Bell, BriefcaseBusiness, Search, UserRound } from "lucide-react";
import { NavLink } from "react-router-dom";

import { useAuthStore } from "../../store/auth";

const navItems = [
  { to: "/", label: "Find Jobs" },
  { to: "/applications", label: "Applications" },
  { to: "/stats", label: "Stats" },
  { to: "/contacts", label: "Contacts" },
];

export function TopNav(): JSX.Element {
  const user = useAuthStore((state) => state.user);

  return (
    <header className="sticky top-0 z-20 border-b border-border bg-hero/95 backdrop-blur">
      <div className="mx-auto flex max-w-7xl items-center justify-between gap-4 px-4 py-4 md:px-6">
        <div className="flex items-center gap-8">
          <NavLink to="/" className="flex items-center gap-2 text-xl font-black text-primary">
            <span className="flex h-8 w-8 items-center justify-center rounded-full bg-primary text-sm text-background">
              <BriefcaseBusiness className="h-4 w-4" />
            </span>
            Voo
          </NavLink>
          <nav className="hidden items-center gap-6 text-sm md:flex">
            {navItems.map((item) => (
              <NavLink
                key={item.to}
                to={item.to}
                className={({ isActive }) => (isActive ? "font-semibold text-text" : "text-subdued hover:text-text")}
              >
                {item.label}
              </NavLink>
            ))}
          </nav>
        </div>
        <div className="flex items-center gap-3">
          <button className="hidden h-9 w-9 items-center justify-center rounded-full bg-surface text-subdued md:flex" title="Search">
            <Search className="h-4 w-4" />
          </button>
          <button className="h-9 w-9 rounded-full bg-surface text-subdued" title="Notifications">
            <Bell className="mx-auto h-4 w-4" />
          </button>
          <div className="flex items-center gap-2">
            <div className="hidden text-right text-xs md:block">
              <p className="font-semibold text-text">{user?.name ?? "Emma R."}</p>
              <p className="text-subdued">Quality Assurance</p>
            </div>
            <div className="flex h-10 w-10 items-center justify-center rounded-full bg-primary text-background">
              <UserRound className="h-5 w-5" />
            </div>
          </div>
        </div>
      </div>
    </header>
  );
}
