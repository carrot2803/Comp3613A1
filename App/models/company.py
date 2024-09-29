from App.database import db
from App.models.job import Job


class Company(db.Model):
    id: int = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name: str = db.Column(db.String(50), nullable=False)
    industry: str = db.Column(db.String(50), nullable=False)
    jobs = db.relationship("Job", backref="company")

    def __init__(self, name: str, industry: str) -> None:
        self.name = name
        self.industry = industry

    def __repr__(self) -> str:
        return "{} {} {}".format(self.id, self.name, self.industry)

    def to_json(self) -> dict:
        return {**self.__dict__, "jobs": [job.id for job in self.jobs]}
