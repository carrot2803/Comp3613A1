from App.database import db


class Application(db.Model):
    id: int = db.Column(db.Integer, primary_key=True)
    job_id: int = db.Column(db.Integer, db.ForeignKey("job.id"))
    applicant_id: int = db.Column(db.Integer, db.ForeignKey("applicant.id"))

    def __init__(self, job_id: int, applicant_id: int) -> None:
        self.job_id = job_id
        self.applicant_id = applicant_id

    def __repr__(self) -> str:
        return f"Application(id={self.id}, job_id={self.job_id}, applicant_id={self.applicant_id})"
