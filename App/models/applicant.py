from App.database import db


class Applicant(db.Model):
    id: int = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name: str = db.Column(db.String(50), nullable=False)
    last_name: str = db.Column(db.String(50), nullable=False)
    education: str = db.Column(db.String(50), nullable=False)
    skills: str = db.Column(db.String(50), nullable=False)
    jobs_applied = db.relationship("Application", backref="applicant")

    def __init__(self, first_name: str, last_name: str, education: str, skills: str) -> None:
        self.first_name = first_name
        self.last_name = last_name
        self.education = education
        self.skills = skills

    def __repr__(self) -> str:
        return "{} {} {} {} {}".format(
            self.id, self.first_name, self.last_name, self.education, self.skills
        )
