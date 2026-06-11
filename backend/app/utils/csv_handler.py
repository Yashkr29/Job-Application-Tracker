import csv
from io import StringIO

from app.models.application import JobApplication


CSV_FIELDS = ["title", "company", "location", "source", "status", "priority", "salary_min", "salary_max", "currency"]


def applications_to_csv(applications: list[JobApplication]) -> str:
    """Serialize applications to CSV."""
    buffer = StringIO()
    writer = csv.DictWriter(buffer, fieldnames=CSV_FIELDS)
    writer.writeheader()
    for app in applications:
        writer.writerow({field: getattr(app, field) for field in CSV_FIELDS})
    return buffer.getvalue()


def parse_applications_csv(content: str) -> list[dict[str, str]]:
    """Parse application rows from CSV content."""
    reader = csv.DictReader(StringIO(content))
    return [row for row in reader if row.get("title") and row.get("company")]

