import { zodResolver } from "@hookform/resolvers/zod";
import { X } from "lucide-react";
import { useForm } from "react-hook-form";
import { z } from "zod";

import type { ApplicationPayload } from "../../api/applications";
import type { ApplicationStatus, Priority } from "../../types/api";
import { statuses, statusLabel } from "../../utils/status";
import { Button } from "../ui/button";
import { Input } from "../ui/input";

const schema = z.object({
  title: z.string().min(1, "Role is required"),
  company: z.string().min(1, "Company is required"),
  location: z.string().optional(),
  source: z.string().optional(),
  job_url: z.string().url("Enter a valid URL").or(z.literal("")).optional(),
  status: z.enum(["SAVED", "APPLIED", "PHONE_SCREEN", "INTERVIEW", "TECHNICAL", "FINAL_ROUND", "OFFER", "REJECTED", "WITHDRAWN", "GHOSTED"]),
  priority: z.enum(["low", "medium", "high", "dream"]),
  salary_min: z.string().optional(),
  salary_max: z.string().optional(),
  currency: z.string().min(3).max(3),
  applied_at: z.string().optional(),
  follow_up_date: z.string().optional(),
  description: z.string().optional(),
});

type FormValues = z.infer<typeof schema>;

function optionalText(value: string | undefined): string | undefined {
  const trimmed = value?.trim();
  return trimmed ? trimmed : undefined;
}

function optionalNumber(value: string | undefined): number | undefined {
  if (!value) {
    return undefined;
  }
  const parsed = Number(value);
  return Number.isFinite(parsed) ? parsed : undefined;
}

export function ApplicationFormModal({
  isOpen,
  isSaving,
  onClose,
  onSubmit,
}: {
  isOpen: boolean;
  isSaving: boolean;
  onClose: () => void;
  onSubmit: (payload: ApplicationPayload) => Promise<void>;
}): JSX.Element | null {
  const {
    formState: { errors },
    handleSubmit,
    register,
    reset,
  } = useForm<FormValues>({
    resolver: zodResolver(schema),
    defaultValues: {
      title: "",
      company: "",
      location: "",
      source: "LinkedIn",
      job_url: "",
      status: "SAVED",
      priority: "medium",
      salary_min: "",
      salary_max: "",
      currency: "INR",
      applied_at: "",
      follow_up_date: "",
      description: "",
    },
  });

  if (!isOpen) {
    return null;
  }

  async function submit(values: FormValues): Promise<void> {
    await onSubmit({
      title: values.title,
      company: values.company,
      location: optionalText(values.location),
      source: optionalText(values.source),
      job_url: optionalText(values.job_url),
      status: values.status as ApplicationStatus,
      priority: values.priority as Priority,
      salary_min: optionalNumber(values.salary_min),
      salary_max: optionalNumber(values.salary_max),
      currency: values.currency.toUpperCase(),
      applied_at: optionalText(values.applied_at),
      follow_up_date: optionalText(values.follow_up_date),
      description: optionalText(values.description),
    });
    reset();
  }

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-text/35 p-4">
      <section className="max-h-[92vh] w-full max-w-3xl overflow-auto rounded-[14px] bg-surface shadow-soft">
        <div className="sticky top-0 z-10 flex items-center justify-between border-b border-border bg-surface px-5 py-4">
          <div>
            <h2 className="text-lg font-semibold text-text">Add application details</h2>
            <p className="text-sm text-subdued">Capture the role properly before it enters your pipeline.</p>
          </div>
          <button className="rounded-app p-2 text-subdued hover:bg-muted" onClick={onClose} title="Close" type="button">
            <X className="h-5 w-5" />
          </button>
        </div>

        <form className="grid gap-4 p-5 md:grid-cols-2" onSubmit={handleSubmit(submit)}>
          <label className="text-sm font-medium text-text">
            Role / position *
            <Input className="mt-2" placeholder="Frontend Engineer" {...register("title")} />
            {errors.title && <span className="mt-1 block text-xs text-danger">{errors.title.message}</span>}
          </label>
          <label className="text-sm font-medium text-text">
            Company *
            <Input className="mt-2" placeholder="Acme Labs" {...register("company")} />
            {errors.company && <span className="mt-1 block text-xs text-danger">{errors.company.message}</span>}
          </label>
          <label className="text-sm font-medium text-text">
            Location / work mode
            <Input className="mt-2" placeholder="Remote, Bengaluru, Hybrid" {...register("location")} />
          </label>
          <label className="text-sm font-medium text-text">
            Source
            <Input className="mt-2" placeholder="LinkedIn, referral, company site" {...register("source")} />
          </label>
          <label className="text-sm font-medium text-text">
            Job URL
            <Input className="mt-2" placeholder="https://..." {...register("job_url")} />
            {errors.job_url && <span className="mt-1 block text-xs text-danger">{errors.job_url.message}</span>}
          </label>
          <label className="text-sm font-medium text-text">
            Status
            <select className="mt-2 h-10 w-full rounded-app border border-border bg-surface px-3 text-sm outline-none focus:border-primary" {...register("status")}>
              {statuses.map((status) => (
                <option key={status} value={status}>
                  {statusLabel(status)}
                </option>
              ))}
            </select>
          </label>
          <label className="text-sm font-medium text-text">
            Priority
            <select className="mt-2 h-10 w-full rounded-app border border-border bg-surface px-3 text-sm outline-none focus:border-primary" {...register("priority")}>
              <option value="low">Low</option>
              <option value="medium">Medium</option>
              <option value="high">High</option>
              <option value="dream">Dream</option>
            </select>
          </label>
          <label className="text-sm font-medium text-text">
            Currency
            <Input className="mt-2" maxLength={3} placeholder="INR" {...register("currency")} />
          </label>
          <label className="text-sm font-medium text-text">
            Salary min
            <Input className="mt-2" min="0" placeholder="600000" type="number" {...register("salary_min")} />
          </label>
          <label className="text-sm font-medium text-text">
            Salary max
            <Input className="mt-2" min="0" placeholder="1200000" type="number" {...register("salary_max")} />
          </label>
          <label className="text-sm font-medium text-text">
            Applied date
            <Input className="mt-2" type="date" {...register("applied_at")} />
          </label>
          <label className="text-sm font-medium text-text">
            Follow-up date
            <Input className="mt-2" type="date" {...register("follow_up_date")} />
          </label>
          <label className="text-sm font-medium text-text md:col-span-2">
            Notes / job description
            <textarea
              className="mt-2 min-h-28 w-full rounded-app border border-border bg-surface px-3 py-2 text-sm text-text outline-none focus:border-primary"
              placeholder="Recruiter name, interview details, role notes, next action..."
              {...register("description")}
            />
          </label>
          <div className="flex justify-end gap-3 border-t border-border pt-4 md:col-span-2">
            <Button onClick={onClose} type="button" variant="secondary">
              Cancel
            </Button>
            <Button disabled={isSaving} type="submit">
              {isSaving ? "Saving..." : "Save application"}
            </Button>
          </div>
        </form>
      </section>
    </div>
  );
}
