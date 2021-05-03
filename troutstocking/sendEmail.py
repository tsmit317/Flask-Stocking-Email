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
    <meta name="color-scheme" content="only">
    <body style='background-color: #999999; margin: 0px; padding: 0px; padding-bottom: 10px;'>
        <div class="topnav" style='background-color: #000000; overflow: hidden;  margin: 0px; padding: 10px; text-align: center;' id="myTopnav">
          <a style='width: 100%;'><img src="https://lh3.googleusercontent.com/bItVytwX0hQTsVO1DAa-2Mxaj6YbENCIpOanM_Uxdt5fKWOHbW5MgbZIbAyzvQFyVk-HZkxVxGol940d75ccqSIOkpWxvtVL4AHGCqihMlvhvlOKlZSjGT7IjD-kdm0z5SnNC1am=w2400"></a>
        </div>
          <div class = 'card' style=' width: 400px; margin: 0 auto; text-align: center; background: #FFFFFF;  border-radius: 8px; box-shadow: 0 19px 38px rgba(0,0,0,0.30), 0 15px 12px rgba(0,0,0,0.22);'>     
            <div class= 'image-wrap' style='background: url("https://lh3.googleusercontent.com/8_rZ3mYTAK0Z4XlPUoR3pAOraXuyFHh8hdJFNnsA2CBfKdF3mHpW5OjpN_9AAi-tzAaaxllIFY9C11Behj-W5BuHa2mb4Ppzxz_UF3TLB1VYxCeU0go9J36FyPv3bdP2PoOiC7zt=w2400"); 
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat; 
            width:100%;
            height: 200px;
            color:#FFFFFF;
            border-radius: 8px 8px 0px 0px;
            line-height: 1pt;
            '>
              <p style = 'font-family: "Roboto", sans-serif; 
              font-weight: 900;
              padding-top: 100px;
              font-size: 24px;
              color: #FFFFFF;
              font-size: 1.2em;'>"""+ t + """</p>
            </div>
           
            <table style='margin: auto; padding-bottom:10px;'>
              <tbody>
  """
  for index, (county_key, stream_list) in enumerate(stocking_info_dict.items()):
    if index == 0:
      c_html += """<tr>
                <th colspan='2' style='font-family: "Roboto", sans-serif; font-weight:bold; padding-top:12px; padding-bottom: 10px; font-size: 14px;'>"""+ county_key + """</th></tr>"""
    
    else:
      c_html +="""<tr>
                <th colspan='2' style='font-family: "Roboto", sans-serif; border-top: 1px solid black; font-weight:bold; padding-top:12px; padding-bottom: 10px; font-size: 14px;'>"""+ county_key + """</th></tr>"""
    
    for stream in stream_list:
      for i in range(0, len(stream), 2):
        c_html += """<tr><td class='stream' style=' padding-bottom: 5px; padding-left:5px; text-align: left;'>""" + stream[i] + "</td><td class ='hatcherytype' style=' padding-bottom: 5px; padding-right: 5px; text-align: right;'>" + stream[i+1] + """</td></tr>"""
                    
    
  c_html += """
          <tr>
            <th colspan='2' style = 'border-top: 1px solid black;'</th>
          </tr>
          </tbody>
        </table>
        <div style='position: relative; text-align: center; border-radius: 0px 0px 8px 8px; padding-top: 10px;'>
          <div style = ''>
            <a href="https://www.ncpaws.org/PAWS/Fish/Stocking/Schedule/OnlineSchedule.aspx" style='font-family: "Roboto", sans-serif;'> Daily Trout Stocking Updates</a>
          </div>
          <div style = 'padding-top: 20px; padding-bottom: 20px;'>
            <a href="">Unsubscribe</a>
          </div>
        </div>
      </div>
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
