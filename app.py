from flask import Flask, render_template, url_for, request
from flask_sqlalchemy import SQLAlchemy

from countylist import nc_counties_list as counties_list

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///selectedcounties.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


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


def add_to_db(request_email, counties_selected):
    emDB = Email(email= request_email)
    try:
        db.session.add(emDB)
        db.session.commit()
    except Exception as e:
        error = str(e.__dict__['orig'])
        print(error)

    for county in counties_selected:
        county_to_DB = Counties(county_name = county, email_id = emDB.id)
        try:
            db.session.add(county_to_DB)
            db.session.commit()
        except:
            print("Problem adding county")

@app.route('/', methods=['GET','POST'])
def home():
    if request.method == 'POST':
        
        counties_selected = request.form.getlist('counties')
        request_email = request.form['email']   

       
        queryEmail = Email.query.filter_by(email=request_email).first() 
        if queryEmail is None:
            add_to_db(request_email, counties_selected)
            return render_template('submitsuccess.html', message="You have been added")
        else:
            
            db.session.delete(queryEmail)
            add_to_db(request_email, counties_selected)
            return render_template('submitsuccess.html', message="You have been updated")   
    else:
        return render_template('home.html', counties= counties_list)


@app.route('/submitsuccess/')
def submitsuccess():
    return render_template('submitsuccess.html')

if __name__ == "__main__":
    db.create_all()

    app.run(debug=True)