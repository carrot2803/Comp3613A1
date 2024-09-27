from App.models import Job, Company
from App.database import db
from sqlalchemy.exc import SQLAlchemyError
from rich.table import Table
from .company import get_company


def create_job(company_id: int, title: str, description: str) -> str:
    company: Company | None = get_company(company_id)
    if company is None:
        return f"[red]Company with ID {company_id} does not exist[/red]"

    try:
        job = Job(company.id, company.name, title, description)
        db.session.add(job)
        db.session.commit()
        return f"[green]Job (ID: {job.id}) '{title}' created by {company.name} (ID: {company.id})[/green]"
    except SQLAlchemyError as e:
        db.session.rollback()
        return f"Error creating job: {e}"


def get_job(id: int) -> Job | None:
    return Job.query.get(id)


def get_all_jobs() -> list[Job]:
    return Job.query.all()


def is_job_in_company(company_id: int, job_id: int) -> bool:
    job: Job | None = get_job(job_id)
    if job is None:
        return False
    return job.company_id == company_id


def get_jobs_table(company_id: int) -> Table | str:
    if get_company(company_id) is None:
        return f"[red]Company with ID {company_id} does not exist[/red]"
    all_jobs: list[Job] = Job.query.filter_by(company_id=company_id).all()
    return format_jobs_table(all_jobs)


def get_all_jobs_table() -> Table | str:
    all_jobs: list[Job] = get_all_jobs()
    return format_jobs_table(all_jobs)


def format_jobs_table(all_jobs: list[Job]) -> Table | str:
    if not all_jobs:
        return "[red]No jobs found. Please create a job first.[/red]"

    job_table = Table(title="[blue]Jobs List[/blue]")
    job_table.add_column("Job ID", justify="center", style="cyan", no_wrap=True)
    job_table.add_column("Company Name", style="green")
    job_table.add_column("Company ID", style="green")
    job_table.add_column("Title", style="yellow")
    job_table.add_column("Description", style="magenta")
    job_table.add_column("Num Applicants", style="purple")

    for job in all_jobs:
        job_table.add_row(
            str(job.id),
            job.company_name,
            str(job.company_id),
            job.title,
            job.description,
            str(len(job.applicants)),
        )

    return job_table
