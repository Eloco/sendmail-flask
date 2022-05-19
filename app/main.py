#!/usr/bin/env python
# coding=utf-8

#Import the flask module
from wrapt_timeout_decorator import *
from flask import Flask, request, jsonify
import base64
import os,sys
import datetime,time,random
import requests
import traceback

import email, smtplib, ssl
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

app = Flask(__name__)

@app.route('/')
def hello_world():
    return "Hello World!"

default_mail_user        =os.environ.get('MAIL_USER'  ) or "None"
default_mail_pass        =os.environ.get('MAIL_PASS'  ) or "None"
default_mail_server      =os.environ.get('MAIL_SERVER') or "smtp.gmail.com"
default_mail_port        =os.environ.get('MAIL_PORT'  ) or 465

@timeout(60*5) # 5 minutes
@app.route('/send', methods=['POST'])
def send_mail():

    status_code    = 200
    result         = "success"
    mail_user      = request.form.get('mail'        , default = default_mail_user       ).strip()
    mail_pass      = request.form.get('pass'        , default = default_mail_pass       ).strip()
    mail_server    = request.form.get('server'      , default = default_mail_server     ).strip()
    mail_port      = request.form.get('port'        , default = default_mail_port       )
    receiver_email = request.form.get('receiver'    , default = "None"                  ).strip()
    subject        = request.form.get('subject'     , default = "default subject"       ).strip()
    body           = request.form.get('message'     , default = "hello world [Default]" ).strip()
    attach_link    = request.form.get('attach_link' , default = "None"                  ).strip()
    Bcc            = request.form.get('Bcc'         , default = "None"                  ).strip()



    # init mesage and body
    if receiver_email == "None":
        status_code = 400
        return jsonify({
                        'code': status_code,
                        'result': "sender email is not defined"
                      })

    message            = MIMEMultipart()
    message["From"]    = mail_user
    message["To"]      = receiver_email
    message["Subject"] = subject

    if Bcc != "None": message["Bcc"]= Bcc  # Recommended for mass emails

    try:
        body=base64.b64decode(body).decode('utf-8')
    except:pass

    message.attach(MIMEText(body, "plain"))

    # insert attachment
    try:
        if attach_link != "None":
            attach_name    = attach_link.split('/')[-1]
            attach_name    = request.form.get('attach_name', default = attach_name).strip()
            r = requests.get(attach_link)
            r.raise_for_status()
            part = MIMEBase("application", "octet-stream")
            part.set_payload(r.content)
            encoders.encode_base64(part)
            part.add_header(
            "Content-Disposition",
           f"attachment; filename= {attach_name}",
            )
            message.attach(part)
    except Exception as e:
        result = "attach file error : " + str(e)

    # send mail
    context = ssl.create_default_context()
    try:
        mail_port = int(mail_port)
        with smtplib.SMTP_SSL(mail_server, mail_port, context=context) as server:
            server.login(mail_user, mail_pass)
            server.sendmail(mail_user, receiver_email, message.as_string())
    except Exception as e:
        status_code = 500
        return jsonify({
                        'code'   : status_code,
                        'result' : "send mail error : " + str(e),
                      })

    return jsonify({
                    'code': status_code,
                    'result': result,
                  })

if __name__ == "__main__":
    # Create the main driver function
    app.run(host    = os.getenv('IP', '0.0.0.0'), 
            port    = int(os.getenv('PORT', 9000)),
            debug   = True,
           )
