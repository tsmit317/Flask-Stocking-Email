from troutstocking import db
from troutstocking.models import Email, Counties


db.session.query(Counties).delete()
db.session.query(Email).delete()
db.session.commit()
