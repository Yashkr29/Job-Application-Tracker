import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { LayoutGrid, List, Plus } from "lucide-react";
import { useState } from "react";
import toast from "react-hot-toast";

import { createApplication, listApplications } from "../api/applications";
import { ApplicationCard } from "../components/applications/ApplicationCard";
import { KanbanBoard } from "../components/applications/KanbanBoard";
import { PageWrapper } from "../components/layout/PageWrapper";
import { EmptyState } from "../components/shared/EmptyState";
import { Button } from "../components/ui/button";
import { Input } from "../components/ui/input";

export function Applications(): JSX.Element {
  const [search, setSearch] = useState("");
  const [view, setView] = useState<"list" | "kanban">("list");
  const queryClient = useQueryClient();
  const applications = useQuery({ queryKey: ["applications", search], queryFn: () => listApplications(search) });
  const createMutation = useMutation({
    mutationFn: createApplication,
    onSuccess: async () => {
      toast.success("Application added");
      await queryClient.invalidateQueries({ queryKey: ["applications"] });
    },
  });

  const items = applications.data?.items ?? [];

  return (
    <PageWrapper
      title="Applications"
      actions={
        <Button
          onClick={() =>
            createMutation.mutate({
              title: "Frontend Engineer",
              company: "Sample Company",
              source: "LinkedIn",
              status: "SAVED",
              priority: "medium",
            })
          }
        >
          <Plus className="mr-2 h-4 w-4" />
          Quick add
        </Button>
      }
    >
      <div className="mb-4 flex flex-wrap gap-2">
        <Input className="max-w-md" placeholder="Search company or role" value={search} onChange={(event) => setSearch(event.target.value)} />
        <Button variant={view === "list" ? "primary" : "secondary"} onClick={() => setView("list")} title="List view">
          <List className="h-4 w-4" />
        </Button>
        <Button variant={view === "kanban" ? "primary" : "secondary"} onClick={() => setView("kanban")} title="Kanban view">
          <LayoutGrid className="h-4 w-4" />
        </Button>
      </div>
      {items.length === 0 ? (
        <EmptyState title="No applications match your filters." />
      ) : view === "kanban" ? (
        <KanbanBoard applications={items} />
      ) : (
        <div className="grid gap-3 lg:grid-cols-2">
          {items.map((item) => (
            <ApplicationCard key={item.id} application={item} />
          ))}
        </div>
      )}
    </PageWrapper>
  );
}

