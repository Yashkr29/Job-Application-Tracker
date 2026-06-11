import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { LayoutGrid, List, Plus } from "lucide-react";
import { useState } from "react";
import toast from "react-hot-toast";

import { createApplication, listApplications, type ApplicationPayload } from "../api/applications";
import { ApplicationFormModal } from "../components/applications/ApplicationFormModal";
import { JobSearchBoard } from "../components/applications/JobSearchBoard";
import { KanbanBoard } from "../components/applications/KanbanBoard";
import { PageWrapper } from "../components/layout/PageWrapper";
import { EmptyState } from "../components/shared/EmptyState";
import { Button } from "../components/ui/button";
import { Input } from "../components/ui/input";

export function Applications(): JSX.Element {
  const [search, setSearch] = useState("");
  const [view, setView] = useState<"list" | "kanban">("list");
  const [isFormOpen, setIsFormOpen] = useState(false);
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

  async function submitApplication(payload: ApplicationPayload): Promise<void> {
    await createMutation.mutateAsync(payload);
    setIsFormOpen(false);
  }

  return (
    <PageWrapper
      title="Applications"
      actions={
        <Button onClick={() => setIsFormOpen(true)}>
          <Plus className="mr-2 h-4 w-4" />
          Add application
        </Button>
      }
    >
      <div className="mb-4 flex flex-wrap gap-2">
        <Input className="max-w-md" placeholder="Search tracked applications" value={search} onChange={(event) => setSearch(event.target.value)} />
        <Button variant={view === "list" ? "primary" : "secondary"} onClick={() => setView("list")} title="List view">
          <List className="h-4 w-4" />
        </Button>
        <Button variant={view === "kanban" ? "primary" : "secondary"} onClick={() => setView("kanban")} title="Kanban view">
          <LayoutGrid className="h-4 w-4" />
        </Button>
      </div>
      {view === "list" ? (
        <JobSearchBoard applications={items} onAddApplication={() => setIsFormOpen(true)} />
      ) : items.length === 0 ? (
        <EmptyState title="No applications match your filters." />
      ) : (
        <KanbanBoard applications={items} />
      )}
      <ApplicationFormModal isOpen={isFormOpen} isSaving={createMutation.isPending} onClose={() => setIsFormOpen(false)} onSubmit={submitApplication} />
    </PageWrapper>
  );
}
