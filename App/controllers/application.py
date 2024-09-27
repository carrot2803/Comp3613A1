from App.models import Applicant, Job
from App.database import db
from sqlalchemy.exc import SQLAlchemyError
from App.models.application import Application
from rich.table import Table
from App.controllers.job import get_job
from App.controllers.applicant import get_applicant


def apply_to_job(applicant: Applicant, job_id: int) -> str:
    job: Job | None = get_job(job_id)
    if not job:
        return f"[red]No job found with ID: {job_id}[/red]"

    has_applied: Application | None = Application.query.filter_by(
        applicant_id=applicant.id, job_id=job.id
    ).first()
    if has_applied:
        return f"[red]Applicant {applicant.first_name} {applicant.last_name} has already applied to job '{job.title}'.[/red]"

    try:
        application = Application(job.id, applicant.id)
        db.session.add(application)
        applicant.jobs_applied.append(application)
        db.session.commit()
        return f"[green]Application created for applicant {applicant.first_name} {applicant.last_name} for the job '{job.title}'![/green]"
    except SQLAlchemyError:
        db.session.rollback()
        return "[red]Failed to apply[/red]"


def get_all_job_applicants_table(job_id: int) -> Table | str:
    job: Job | None = get_job(job_id)

    if not job:
        return f"[red]No job found with ID: {job_id}[/red]"

    applications: list[Application] = job.applicants
    if not applications:
        return f"[red]No applicants found for job '{job.title}'.[/red]"

    applicant_table = Table(title=f"Applicants for Job '{job.title}'")
    applicant_table.add_column("ID", justify="center", style="cyan", no_wrap=True)
    applicant_table.add_column("First Name", style="magenta")
    applicant_table.add_column("Last Name", style="magenta")
    applicant_table.add_column("Education", style="blue")
    applicant_table.add_column("Skills", style="blue")

    for application in applications:
        applicant: Applicant | None = get_applicant(application.applicant_id)
        if applicant:
            applicant_table.add_row(
                str(applicant.id),
                applicant.first_name,
                applicant.last_name,
                applicant.education,
                applicant.skills,
            )
        else:
            return f"[red]Applicant with ID {application.applicant_id} not found.[/red]"

    return applicant_table
