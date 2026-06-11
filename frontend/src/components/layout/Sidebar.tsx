import { BarChart3, Briefcase, FileText, Home, Settings, Users } from "lucide-react";
import { NavLink } from "react-router-dom";

const navItems = [
  { to: "/", label: "Dashboard", icon: Home },
  { to: "/applications", label: "Applications", icon: Briefcase },
  { to: "/stats", label: "Stats", icon: BarChart3 },
  { to: "/contacts", label: "Contacts", icon: Users },
  { to: "/resumes", label: "Resumes", icon: FileText },
  { to: "/settings", label: "Settings", icon: Settings },
];

export function Sidebar(): JSX.Element {
  return (
    <aside className="sticky top-0 hidden h-screen w-64 border-r border-border bg-surface p-4 md:block">
      <div className="mb-6 text-lg font-semibold text-text">Job Tracker</div>
      <nav className="space-y-1">
        {navItems.map((item) => (
          <NavLink
            key={item.to}
            to={item.to}
            className={({ isActive }) =>
              `flex items-center gap-3 rounded-app px-3 py-2 text-sm ${isActive ? "bg-primary text-background" : "text-subdued hover:bg-muted hover:text-text"}`
            }
          >
            <item.icon className="h-4 w-4" />
            {item.label}
          </NavLink>
        ))}
      </nav>
    </aside>
  );
}

