import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import date
import os

sender_email = os.environ.get('TROUT_STOCKING_EMAIL')
sender_email_password = os.environ.get('TROUT_STOCKING_EMAIL_PASSWORD')

today =  date.today()
t = today.strftime("%A - %B %d, %Y")

def create_html(stocking_info_dict):
  c_html = """\
  <html>
    <body>
      <h3 class='header' style='color:black;font-weight:bold;font-variant:small-caps;'>North Carolina Trout Stocking Notification</h3>
      <p>The following counties have been stocked: </p>
      <br>
      <table class='stable' style='border-width:1px;border-style:solid;border-color:black;padding-top:10px;padding-bottom:10px;padding-right:10px;padding-left:10px;border-radius:12px;'>
        <tbody>
          <tr><th colspan='2' style='color:black;font-weight:bold;' >"""+ t + """</th></tr>
  """
  for county_key, stream_list in stocking_info_dict.items():
    c_html += """<tr>
            <th class='list-key' colspan='2' style='border-top: 1px solid black; font-weight:bold; padding-top:12px;'>"""+ county_key + """</th></tr>"""
  
    for stream in stream_list:
        for i in range(0, len(stream), 2):
          c_html += """<tr><td class='stream' style='padding-right:5px;'>""" + stream[i] + "</td><td class ='hatcherytype'>" + stream[i+1] + """</td></tr>"""
                  
  c_html += """
        </tbody>
      </table>
      <br>
      <a href="https://www.ncpaws.org/PAWS/Fish/Stocking/Schedule/OnlineSchedule.aspx">Daily Trout Stocking Updates</a> 
    </body>
  </html>
  """
  return c_html


def create_text(stocking_info_dict):
  c_text = """\
    
        Stocking Notification!\n
        
      """
  for county_key, stream_list in stocking_info_dict.items():
    c_text += "\n" + county_key + ":\n"
    for stream in stream_list:
      for i in range(0, len(stream), 2):
        c_text += stream[i] + " - " + stream[i+1]
  return c_text


def send_email(email_info_dict):
  context = ssl.create_default_context()
  with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
      server.login(sender_email, sender_email_password)
      
      for receiver, stocking_info_dict in email_info_dict.items():
        
        message = MIMEMultipart("alternative")
        message["Subject"] = "testing multipart"
        message["From"] = sender_email
        message["To"] = receiver
        
        text = create_text(stocking_info_dict)
        html = create_html(stocking_info_dict)

        mime_plain = MIMEText(text, "plain")
        mime_html = MIMEText(html, "html")
        
        message.attach(mime_plain)
        message.attach(mime_html)
        
        server.sendmail(sender_email, receiver, message.as_string())
        print('Email sent')
