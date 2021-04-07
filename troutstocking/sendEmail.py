import smtplib, ssl
import emailInfo
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import stockingScrape

port = 465

def create_html(stocking_info_dict):
    c_html = """\
    <head>
        <style type="text/css">
            div.county-div {{
                border: 1px solid red;
                padding: 10px;
                border-radius: 15px;
            }}
            h3.header {{
                color: black;
                font-weight: bold;
                font-variant: small-caps;
            }}
            p.list-key {{
                font-weight: bold;
            }}
        </style>
    </head>
    <html>
        <body>
            <h3 class='header'>North Carolina Trout Stocking Notification</h3>
            <p>The following counties have been stocked: </p>
            <br>
    """
    for keys, values in stocking_info_dict.items():
        c_html += """<div class='county-div'>
                    <p class='list-key'>"""+ keys + """</p>"""
    
        for val in values:
            for i in range(0, len(val), 2):
                c_html += """<p class='list-value'>""" + val[i] + " " + val[i+1] + """</p>"""
                    
    c_html += """</div>
            <br>"""

    c_html += """<a href="https://www.ncpaws.org/PAWS/Fish/Stocking/Schedule/OnlineSchedule.aspx">Daily Trout Stocking Updates</a> 
        </body>
    </html>
    """
    return c_html

def create_text(stocking_info_dict)
    c_text = """\
    
        Stocking Notification!\n
        
      """
    for keys, values in stocking_info_dict.items():
        c_text += "\n" + keys + ":\n"
        for val in values:
            for i in range(0, len(val), 2):
                c_text += val[i] + " - " + val[i+1]
        c_text += "\n"

def send_email(email_info_dict):
  context = ssl.create_default_context()
  with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
      server.login(emailInfo.sender_email, emailInfo.sender_pass)
      
      for person in emailInfo.testList:
        
        message = MIMEMultipart("alternative")
        message["Subject"] = "testing multipart"
        message["From"] = emailInfo.sender_email
        message["To"] = person['Email']
        
        mime_plain = MIMEText(text, "plain")
        mime_html = MIMEText(html.format(name = person['Name']), "html")
        
        message.attach(mime_plain)
        message.attach(mime_html)
        
        server.sendmail(emailInfo.sender_email, person['Email'], message.as_string())
        
  print('Email sent')