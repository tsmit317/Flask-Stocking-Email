from datetime import datetime
import sys
import time

from flask import Flask, render_template, url_for, request, flash, redirect
from apscheduler.schedulers.background import BackgroundScheduler

from troutstocking import app, db
from troutstocking.models import Email, Counties
from troutstocking.countylist import nc_counties_list as counties_list
from troutstocking.troutScrape import StockingScrape
from troutstocking import testEmail, sendEmail

scheduler = BackgroundScheduler()
stocking = StockingScrape()


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

def delete_everthing(modelToDelete):
    db.session.query(modelToDelete).delete()
    db.session.commit()
    
def delete_and_commit(query_to_delete):
    db.session.delete(query_to_delete)
    db.session.commit()


def find_emails_for_WScounty(county_to_find):
    return [temp.email for temp in Email.query.join(Counties).filter(Counties.county_name == county_to_find).all()]
    
def create_email_dict_for_sending():
    stocking_dict = stocking.update_and_get_stocking_dict()
    
    to_send_dict = {}
    for stocked_county, stream_info in stocking_dict.items():

        for mail in find_emails_for_WScounty(stocked_county):

            if mail in to_send_dict:
                to_send_dict[mail][stocked_county] = stream_info

            else:
                to_send_dict[mail] = {stocked_county: stream_info}

    return to_send_dict


@scheduler.scheduled_job('interval', id='sched_job', hours=24 ,max_instances=1, misfire_grace_time=900, next_run_time='2021-05-03 16:30:00')
def sched_job():
    sendEmail.send_email_to_users(create_email_dict_for_sending())
    time.sleep(20)

scheduler.start()

sendEmail.send_email_to_users(create_email_dict_for_sending())

@app.route('/', methods=['GET','POST'])
def home():
    return render_template('home.html', counties= counties_list)


@app.route('/process-data', methods=['GET', 'POST'])
def process_data():
    if request.method == 'POST':
        
        counties_selected = request.form.getlist('counties')
        request_email = request.form['email'] 
        
        if not counties_selected:
            flash('You must select at least one county', 'danger')
            return redirect(url_for('home'))

        else:
            queryEmail = Email.query.filter_by(email=request_email).first() 
            if queryEmail is None:
                add_to_db(request_email, counties_selected)
                return render_template('submitsuccess.html', message=" has been successfully added to the mailing list.", 
                                        counties_confirmed = query_user_counties(request_email), email_query = Email.query.filter_by(email=request_email).first())

            else:
                delete_and_commit(queryEmail)
                add_to_db(request_email, counties_selected)
                return render_template('submitsuccess.html', message=" has been successfully updated.", 
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
            flash('You are currently unsubscribed.', 'warning')
            return render_template('unsubscribe.html')

        else:
            delete_and_commit(queryEmail)
            flash("You have been successfully unsubscribed!",'success')
            return render_template('unsubscribe.html')
    
    else:
        return render_template('unsubscribe.html')

@app.route('/about')
def about():
    return render_template('about.html')