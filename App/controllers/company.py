from App.models import Company
from App.database import db
from sqlalchemy.exc import SQLAlchemyError
from rich.table import Table


def create_company(name: str, industry: str) -> str:
    try:
        company = Company(name, industry)
        db.session.add(company)
        db.session.commit()
        return f"[green]New {company.industry} company created: ID: {company.id}, Name: {company.name}[/green]"
    except SQLAlchemyError as e:
        db.session.rollback()
        print(f"Error creating company: {e}")
        return "[red]Failed to create company[/red]"


def get_company(id: int) -> Company | None:
    return Company.query.get(id)


def get_all_companies() -> list[Company]:
    return Company.query.all()


def get_all_companies_table() -> Table | str:
    all_companies: list[Company] = get_all_companies()

    if not all_companies:
        return "[red]No Company found. Please create a Company first.[/red]"

    table = Table(title="Company List")
    table.add_column("Company ID", justify="center", style="cyan", no_wrap=True)
    table.add_column("Name", style="yellow")
    table.add_column("Industry", style="magenta")
    table.add_column("Num Jobs", style="blue")

    for company in all_companies:
        table.add_row(
            str(company.id), company.name, company.industry, str(len(company.jobs))
        )
    return table
