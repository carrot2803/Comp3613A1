from App.models import Applicant
from App.database import db
from sqlalchemy.exc import SQLAlchemyError
from rich.table import Table


def create_applicant(first_name: str, last_name: str, education: str,  skills: str) -> str:
    try:
        applicant = Applicant(first_name, last_name, education, skills)
        db.session.add(applicant)
        db.session.commit()
        return f"[green]New applicant created: {applicant.first_name} {applicant.last_name}[/green]"
    except SQLAlchemyError as e:
        db.session.rollback()
        print(f"Error creating applicant: {e}")
        return "[red]Failed to create applicant[/red]"


def get_applicant(id: int) -> Applicant | None:
    return Applicant.query.get(id)


def get_all_applicants() -> list[Applicant]:
    return Applicant.query.all()


def get_all_applicants_table() -> Table | str:
    all_applicants: list[Applicant] = get_all_applicants()

    if not all_applicants:
        return "[red]No applicants found. Please create an applicant first.[/red]"

    table = Table(title="Applicants List")
    table.add_column("ID", justify="center", style="cyan", no_wrap=True)
    table.add_column("First Name", style="magenta")
    table.add_column("Last Name", style="magenta")
    table.add_column("Education", style="blue")
    table.add_column("Skills", style="blue")
    table.add_column("Applications", style="yellow")

    for applicant in all_applicants:
        table.add_row(
            str(applicant.id),
            applicant.first_name,
            applicant.last_name,
            applicant.education,
            applicant.skills,
            str(len(applicant.jobs_applied)),
        )
    return table
