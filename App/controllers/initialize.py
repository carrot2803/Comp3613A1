import csv
from pathlib import Path
import random
from .application import apply_to_job
from .job import create_job
from .applicant import create_applicant, get_applicant
from .company import create_company
from App.database import db
from rich.console import Console

console = Console()


def initialize() -> None:
    db.drop_all()
    db.create_all()
    init_db()
    console.print("[green]Database initialized[/green]")


CSV_PATHS: dict[str, Path] = {
    "companies": Path(__file__).parent.parent / "data" / "companies.csv",
    "jobs": Path(__file__).parent.parent / "data" / "jobs.csv",
    "applicants": Path(__file__).parent.parent / "data" / "applicants.csv",
}


def load_data(file: str) -> list[dict]:
    with open(CSV_PATHS[file], newline="") as f:
        return list(csv.DictReader(f))


def init_db() -> None:
    for company in load_data("companies"):
        create_company(company["name"], company["industry"])

    for applicant in load_data("applicants"):
        create_applicant(
            applicant["first_name"],
            applicant["last_name"],
            applicant["education"],
            applicant["skills"],
        )

    jobs: list[dict] = load_data("jobs")
    for job in jobs:
        create_job(int(job["company_id"]), job["title"], job["description"])

    applicants = [get_applicant(i + 1) for i in range(len(load_data("applicants")))]

    for job_id in range(1, len(jobs) + 1):
        num_applications: int = random.randint(2, 4)
        assigned_applicants = random.sample(applicants, num_applications)

        for applicant in assigned_applicants:
            apply_to_job(applicant, job_id)
