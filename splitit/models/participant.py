from splitit.models.shared import db


class Participant(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', backref=db.backref('participants', lazy='dynamic'))

    auction_id = db.Column(db.Integer, db.ForeignKey('auction.id'))
    auction = db.relationship('Auction', backref=db.backref('participants', lazy='dynamic'))

    def __init__(self, user_id, auction_id):
        self.user_id = int(user_id)
        self.auction_id = int(auction_id)

    def has_completed_bidding(self):
        return self.bids.count() > 0
