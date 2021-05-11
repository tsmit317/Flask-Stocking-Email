from troutstocking import db
from troutstocking.models import Email, Counties

def create():
    db.create_all()

def delete_everthing():
    db.session.query(Counties).delete()
    db.session.query(Email).delete()
    db.session.commit()
