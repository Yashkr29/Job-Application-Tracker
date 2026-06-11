export function Skeleton({ className = "" }: { className?: string }): JSX.Element {
  return <div className={`animate-pulse rounded-app bg-muted ${className}`} />;
}

