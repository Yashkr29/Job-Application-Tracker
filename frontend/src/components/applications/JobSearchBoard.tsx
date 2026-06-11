import { Bookmark, Check, MapPin, Search, SlidersHorizontal } from "lucide-react";
import { useMemo, useState } from "react";

import type { JobApplication } from "../../types/api";
import { statusLabel } from "../../utils/status";
import { Badge } from "../ui/badge";
import { Button } from "../ui/button";
import { Input } from "../ui/input";

const chips = [
  "Sales",
  "Fulltime",
  "Remote",
  "Product designer",
  "Senior level",
  "Illustrator",
  "Co-Founder",
  "Senior Dev",
  "Researcher",
  "Project manager",
  "Designer",
];

const sampleApplications: JobApplication[] = [
  {
    id: "sample-1",
    title: "UX Researcher",
    company: "Webflow",
    location: "California, CA",
    source: "LinkedIn",
    job_url: null,
    description: null,
    status: "PHONE_SCREEN",
    priority: "high",
    salary_min: null,
    salary_max: null,
    currency: "INR",
    applied_at: null,
    follow_up_date: null,
    interview_at: null,
    offer_deadline: null,
    created_at: new Date(Date.now() - 60 * 60 * 1000).toISOString(),
    updated_at: new Date().toISOString(),
  },
  {
    id: "sample-2",
    title: "Quality Assurance",
    company: "Notion",
    location: "Idaho, ID",
    source: "Referral",
    job_url: null,
    description: null,
    status: "APPLIED",
    priority: "dream",
    salary_min: null,
    salary_max: null,
    currency: "INR",
    applied_at: null,
    follow_up_date: null,
    interview_at: null,
    offer_deadline: null,
    created_at: new Date(Date.now() - 2 * 60 * 60 * 1000).toISOString(),
    updated_at: new Date().toISOString(),
  },
  {
    id: "sample-3",
    title: "Senior Dev",
    company: "Zapier",
    location: "Oklahoma, OK",
    source: "Company site",
    job_url: null,
    description: null,
    status: "TECHNICAL",
    priority: "medium",
    salary_min: null,
    salary_max: null,
    currency: "INR",
    applied_at: null,
    follow_up_date: null,
    interview_at: null,
    offer_deadline: null,
    created_at: new Date(Date.now() - 7 * 60 * 60 * 1000).toISOString(),
    updated_at: new Date().toISOString(),
  },
  {
    id: "sample-4",
    title: "Product Designer",
    company: "Mailchimp",
    location: "Tennessee, TN",
    source: "AngelList",
    job_url: null,
    description: null,
    status: "INTERVIEW",
    priority: "high",
    salary_min: null,
    salary_max: null,
    currency: "INR",
    applied_at: null,
    follow_up_date: null,
    interview_at: null,
    offer_deadline: null,
    created_at: new Date(Date.now() - 24 * 60 * 60 * 1000).toISOString(),
    updated_at: new Date().toISOString(),
  },
  {
    id: "sample-5",
    title: "Sales",
    company: "Outreach",
    location: "New York, NY",
    source: "Naukri",
    job_url: null,
    description: null,
    status: "SAVED",
    priority: "low",
    salary_min: null,
    salary_max: null,
    currency: "INR",
    applied_at: null,
    follow_up_date: null,
    interview_at: null,
    offer_deadline: null,
    created_at: new Date(Date.now() - 2 * 24 * 60 * 60 * 1000).toISOString(),
    updated_at: new Date().toISOString(),
  },
  {
    id: "sample-6",
    title: "Project manager",
    company: "Squarespace",
    location: "Florida, FL",
    source: "LinkedIn",
    job_url: null,
    description: null,
    status: "FINAL_ROUND",
    priority: "medium",
    salary_min: null,
    salary_max: null,
    currency: "INR",
    applied_at: null,
    follow_up_date: null,
    interview_at: null,
    offer_deadline: null,
    created_at: new Date(Date.now() - 3 * 24 * 60 * 60 * 1000).toISOString(),
    updated_at: new Date().toISOString(),
  },
];

function relativeTime(iso: string): string {
  const hours = Math.max(1, Math.round((Date.now() - new Date(iso).getTime()) / 3_600_000));
  if (hours < 24) {
    return `${hours} hour${hours === 1 ? "" : "s"} ago`;
  }
  const days = Math.round(hours / 24);
  return `${days} day${days === 1 ? "" : "s"} ago`;
}

function logoColor(index: number): string {
  const colors = ["bg-primary", "bg-text", "bg-accent", "bg-success", "bg-danger", "bg-subdued"];
  return colors[index % colors.length];
}

export function JobSearchBoard({ applications }: { applications: JobApplication[] }): JSX.Element {
  const [search, setSearch] = useState("");
  const jobs = applications.length > 0 ? applications : sampleApplications;
  const filteredJobs = useMemo(() => {
    const term = search.trim().toLowerCase();
    if (!term) {
      return jobs;
    }
    return jobs.filter((job) => `${job.title} ${job.company} ${job.location ?? ""}`.toLowerCase().includes(term));
  }, [jobs, search]);

  return (
    <div className="overflow-hidden rounded-app bg-surface shadow-soft">
      <section className="relative overflow-hidden bg-hero px-6 pb-6 pt-5 md:px-10 md:pb-8">
        <div className="mb-8 flex items-center justify-between gap-4">
          <nav className="hidden items-center gap-6 text-sm md:flex">
            <span className="border-t-2 border-text pt-3 font-semibold text-text">Find Jobs</span>
            <span className="text-subdued">Employers</span>
            <span className="text-subdued">Upload Job</span>
            <span className="text-subdued">About Us</span>
          </nav>
          <div className="ml-auto hidden gap-4 md:flex">
            <div className="portrait-tile h-20 w-14 rounded-app bg-surface shadow-soft" style={{ "--tilt": "-15deg" } as React.CSSProperties} />
            <div className="portrait-tile h-20 w-14 rounded-app bg-muted shadow-soft" style={{ "--tilt": "8deg" } as React.CSSProperties} />
            <div className="portrait-tile h-20 w-20 rounded-app bg-border shadow-soft" style={{ "--tilt": "18deg" } as React.CSSProperties} />
          </div>
        </div>
        <h1 className="mb-5 max-w-md text-2xl font-bold text-text md:text-3xl">Find Your Dream Job Here</h1>
        <div className="relative z-10 grid gap-3 rounded-[28px] bg-surface p-2 shadow-soft md:grid-cols-[1fr_1fr_auto]">
          <label className="flex items-center gap-3 border-border px-3 md:border-r">
            <Search className="h-5 w-5 text-subdued" />
            <Input className="border-0 bg-transparent shadow-none focus:border-0" placeholder="Job title or keyword" value={search} onChange={(event) => setSearch(event.target.value)} />
          </label>
          <label className="flex items-center gap-3 px-3">
            <MapPin className="h-5 w-5 text-subdued" />
            <Input className="border-0 bg-transparent shadow-none focus:border-0" placeholder="Add country or city" />
          </label>
          <Button className="h-12 rounded-[24px] px-10">Search</Button>
        </div>
      </section>

      <div className="flex gap-2 overflow-x-auto border-b border-border bg-surface px-4 py-3">
        {chips.map((chip) => (
          <button key={chip} className="shrink-0 rounded-app border border-border px-3 py-1 text-xs text-text hover:bg-muted">
            {chip}
          </button>
        ))}
      </div>

      <section className="grid gap-5 bg-surface p-4 md:grid-cols-[230px_1fr]">
        <aside className="space-y-6 text-sm">
          <div className="flex items-center justify-between">
            <h2 className="font-semibold text-text">Filter</h2>
            <SlidersHorizontal className="h-4 w-4 text-subdued" />
          </div>
          <Input placeholder="Company, skill, tag..." />
          <div>
            <h3 className="mb-3 font-semibold text-text">Specialty</h3>
            <div className="space-y-2 text-subdued">
              {["Product", "Engineering", "Research"].map((item) => (
                <label key={item} className="flex items-center gap-2">
                  <input className="accent-primary" type="checkbox" />
                  {item}
                </label>
              ))}
            </div>
          </div>
          <div>
            <h3 className="mb-3 font-semibold text-text">Employment</h3>
            <div className="space-y-2 text-subdued">
              {["Fulltime", "Senior level", "Remote"].map((item) => (
                <label key={item} className="flex items-center gap-2">
                  <span className="flex h-4 w-4 items-center justify-center rounded bg-primary text-background">
                    <Check className="h-3 w-3" />
                  </span>
                  {item}
                </label>
              ))}
              <label className="flex items-center gap-2">
                <span className="h-4 w-4 rounded border border-border" />
                Contract
              </label>
            </div>
          </div>
          <div>
            <h3 className="font-semibold text-text">Salary Type</h3>
          </div>
        </aside>

        <div className="space-y-2">
          {filteredJobs.map((job, index) => (
            <article key={job.id} className="grid items-center gap-3 rounded-app px-3 py-3 transition hover:bg-muted md:grid-cols-[1fr_auto_auto_auto]">
              <div className="flex items-center gap-4">
                <div className={`flex h-10 w-10 items-center justify-center rounded-app text-sm font-bold text-background ${logoColor(index)}`}>
                  {job.company.slice(0, 1)}
                </div>
                <div>
                  <h3 className="font-semibold text-text">{job.title}</h3>
                  <p className="text-xs text-subdued">{job.company}</p>
                </div>
              </div>
              <div className="flex flex-wrap gap-2">
                <Badge>Fulltime</Badge>
                <Badge>{statusLabel(job.status)}</Badge>
                <Badge>Remote</Badge>
              </div>
              <p className="text-sm font-medium text-text">{job.location ?? "Remote"}</p>
              <div className="flex items-center justify-between gap-5">
                <span className="text-xs text-subdued">{relativeTime(job.created_at)}</span>
                <Bookmark className="h-5 w-5 text-text" />
              </div>
            </article>
          ))}
        </div>
      </section>
    </div>
  );
}
