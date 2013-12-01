from splitit.models.shared import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    def __init__(self):
        pass
