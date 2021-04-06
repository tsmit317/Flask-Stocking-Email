from troutstocking import db


class Email(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String(50), nullable=False)
    counties = db.relationship('Counties', backref='email', lazy=True, cascade="all, delete, delete-orphan")
    
    def __repr__(self):
        return '<Email {}>'.format(self.email)
    

class Counties(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    county_name = db.Column(db.String(120), nullable=False)
    email_id = db.Column(db.Integer, db.ForeignKey('email.id'), nullable=False)

    def __repr__(self):
        return '<Counties {} : {}>'.format(self.county_name, self.email_id)

