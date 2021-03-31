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
        except Exception as e:
            error = str(e.__dict__['orig'])
            print(error)


def query_user_counties(emailStr):
    userEm = Email.query.filter_by(email=emailStr).first()
    return Counties.query.filter_by(email_id=userEm.id).all()


def delete_and_commit(query_to_delete):
    db.session.delete(query_to_delete)
    db.session.commit()


def find_emails_for_WScounty(county_to_find):
    return [temp.email for temp in Email.query.join(Counties).filter(Counties.county_name == county_to_find).all()]
    

def make_dict_for_emails(c_list):
    email_with_counties_dict = {}
    for c in c_list: 
        for i in find_emails_for_WScounty(c):
            if i in email_with_counties_dict.keys():
                email_with_counties_dict[i].append(c)
            else:
                email_with_counties_dict[i] = [c]
    return email_with_counties_dict            


@app.route('/', methods=['GET','POST'])
def home():
    return render_template('home.html', counties= counties_list)


@app.route('/process-data', methods=['GET', 'POST'])
def process_data():
    if request.method == 'POST':
        counties_selected = request.form.getlist('counties')
        request_email = request.form['email']   

        queryEmail = Email.query.filter_by(email=request_email).first() 
        if queryEmail is None:
            add_to_db(request_email, counties_selected)
            return render_template('submitsuccess.html', message=" has been successfully added", 
                                    counties_confirmed = query_user_counties(request_email), email_query = Email.query.filter_by(email=request_email).first())
        
        else:
            delete_and_commit(queryEmail)
            add_to_db(request_email, counties_selected)
            return render_template('submitsuccess.html', message=" has been successfully updated", 
                                    counties_confirmed = query_user_counties(request_email), email_query= Email.query.filter_by(email=request_email).first())   
    

@app.route('/submitsuccess')
def submitsuccess():
    return render_template('submitsuccess.html')


@app.route('/unsubscribe', methods=['GET','POST'])
def unsubscribe():
    if request.method == 'POST':
        request_email = request.form['email']
        queryEmail = Email.query.filter_by(email=request_email).first()
        if queryEmail is None:
            return render_template('unsubscribe.html', message = "You are currently unsubscribed.")
        else:
            delete_and_commit(queryEmail)
            return render_template('unsubscribe.html', message = "You have been successfully unsubscribed!")
    
    else:
        return render_template('unsubscribe.html', message= "Enter your email to unsubscribe.")


if __name__ == "__main__":
    db.create_all()

    app.run(debug=True)