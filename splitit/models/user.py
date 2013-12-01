from splitit.models.shared import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255))
    oauth_access_token = db.Column(db.String(255))

    def __init__(self):
        pass
