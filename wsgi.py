import click
from flask import Flask
from flask.cli import AppGroup
from rich.console import Console
from rich.table import Table
from App.database import get_migrate, Migrate
from App.models import Applicant
from App.main import create_app
from App.controllers import (
    initialize,
    create_company,
    create_applicant,
    create_job,
    apply_to_job,
    is_job_in_company,
    get_applicant,
    get_all_companies_table,
    get_all_applicants_table,
    get_all_job_applicants_table,
    get_all_jobs_table,
    get_jobs_table,
)

app: Flask = create_app()
migrate: Migrate = get_migrate(app)
console = Console()

job = AppGroup("job", help="job commands for viewing and creating jobs")
applicant = AppGroup("applicant", help="applicant commands for CRUD applicants")
company = AppGroup("company", help="company commands for CRUD applicants")


@app.cli.command("init", help="Creates and initializes the database")
def init() -> None:
    initialize()


@company.command("create", help="Creates a new company entry in the database.")
@click.argument("name", default="Jobs TT")
@click.argument("industry", default="Tech")
def create_company_command(name, industry) -> None:
    console.print(create_company(name, industry))


@applicant.command("create", help="Creates a new applicant.")
@click.argument("first_name", default="Default")
@click.argument("last_name", default="Applicant")
@click.argument("Education", default="Bachelor's")
@click.argument("Skills", default="Productivity")
def create_applicant_command(first_name: str, last_name: str, education: str, skills: str) -> None:
    console.print(create_applicant(first_name, last_name, education, skills))


@job.command("create", help="Adds a new job listing to the database.")
@click.argument("title", default="New Job")
@click.argument("description", default="An entry-level job")
def create_job_command(title, description) -> None:
    console.print(get_all_companies_table())
    company_id: int = click.prompt("Select your CompanyID", type=int)
    console.print(create_job(company_id, title, description))


@job.command("apply", help="Allows an applicant to apply for a job.")
def apply_job_command() -> None:
    console.print(get_all_applicants_table())
    applicant_id: int = click.prompt("Enter your applicant ID", type=int)
    applicant: Applicant | None = get_applicant(applicant_id)
    if not applicant:
        console.print(f"[red]No applicant found with ID: {applicant_id}[/red]")
        return
    console.print(get_all_jobs_table())
    job_id: int = click.prompt("Enter the job ID for your interested job", type=int)
    console.print(apply_to_job(applicant, job_id))


@job.command("view-all", help="Displays a table of all available job listings.")
def view_jobs_command() -> None:
    console.print(get_all_jobs_table())


@job.command("view-applicants", help="Shows all applicants for a company's jobs.")
def view_job_applicants_command() -> None:
    console.print(get_all_companies_table())
    company_id: int = click.prompt("Enter your company's ID", type=int)
    console.print(get_jobs_table(company_id))
    job_id: int = click.prompt("Enter the job ID to view its applicants", type=int)
    if is_job_in_company(company_id, job_id):
        console.print(get_all_job_applicants_table(job_id))
    else:
        console.print(f"[red]Company does not offer job with ID: {job_id}[/red]")


@job.command("view-all-applicants", help="Shows all applicants for a specific job.")
def view_all_job_applicants_command() -> None:
    console.print(
        "[bold yellow]Administrator access required. Please input your password.[/bold yellow]\n[bold]Hint: password is 'password'[/bold]"
    )
    password: str = click.prompt("Enter password", hide_input=True)
    if password != "password":
        console.print("[bold red]Access denied: Incorrect password[/bold red]")
    else:
        console.print(get_all_jobs_table())
        job_id: int = click.prompt("Enter job ID to view applicants", type=int)
        console.print(get_all_job_applicants_table(job_id))


@applicant.command("view-all", help="Displays a list of all applicants.")
def view_all_applicants_command() -> None:
    console.print(
        "[bold yellow]Administrator access required. Please input your password.[/bold yellow]\n[bold]Hint: password is 'password'[/bold]"
    )
    password: str = click.prompt("Enter password", hide_input=True)
    if password == "password":
        console.print(get_all_applicants_table())
    else:
        console.print("[bold red]Access denied: Incorrect password[/bold red]")


@app.cli.command("help", help="Displays all available commands and their descriptions.")
def help_command() -> None:
    ctx = click.Context(app.cli)
    groups: dict[str, AppGroup] = {"applicant": applicant, "company": company, "job": job}
    table = Table(title="Available Commands")
    table.add_column("Command", justify="left", style="cyan", no_wrap=True)
    table.add_column("Description", justify="left", style="magenta")

    for cmd in app.cli.list_commands(ctx) + [
        f"{g} {c}" for g, group in groups.items() for c in group.list_commands(ctx)
    ]:
        group, command = cmd.split() if " " in cmd else (None, cmd)
        command = (
            groups[group].get_command(ctx, command) if group else app.cli.get_command(ctx, command)
        )
        table.add_row(cmd, command.help if command else "No description available")

    console.print(table)


app.cli.add_command(applicant)
app.cli.add_command(company)
app.cli.add_command(job)
