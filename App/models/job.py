from App.database import db
from App.models.application import Application


class Job(db.Model):
    id: int = db.Column(db.Integer, primary_key=True)
    company_id: int = db.Column(db.Integer, db.ForeignKey("company.id"))
    company_name: str = db.Column(db.String(100), nullable=False)
    title: str = db.Column(db.String(100), nullable=False)
    description: str = db.Column(db.String(100), nullable=False)
    applicants: list[Application] = db.relationship("Application", backref="job")

    def __init__(
        self, company_id: int, company_name: str, title: str, description: str
    ) -> None:
        self.company_id = company_id
        self.company_name = company_name
        self.title = title
        self.description = description

    def __repr__(self) -> str:
        return (
            f"<Job: {self.title} at {self.company_name} (ID: {self.id}), "
            f"Company ID: {self.company_id}, "
            f"Description: {self.description}>"
        )
