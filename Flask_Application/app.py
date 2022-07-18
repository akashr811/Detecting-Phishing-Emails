from flask import Flask,jsonify, render_template
import imaplib, email
import sqlite3
from second import second
from flask_cors import CORS
# connection=sqlite3.connect("Project.db",check_same_thread=False)

global UN,PW,host,getsender,getsub,getdate,cleantext,phishing,text_pred,url_pred
# UN='1ep18cs017.cse@eastpoint.ac.in'
# PW='charlie_X95'
# host='imap.gmail.com' 
app = Flask(__name__)
app.register_blueprint(second, url_prefix='/main')
cors = CORS(app)
@app.route('/res')
def output():
    global UN,PW,host
    UN = 'sandeep.18bec@cmr.edu.in'
    PW = 'Sandeep#29112000'
    host='imap.gmail.com' 
    mail = imaplib.IMAP4_SSL(host)
    mail.login(UN, PW)
    mail.select("inbox")
    _, search_data = mail.search(None, 'UNSEEN')
    my_message = []
    for num in search_data[0].split():
        email_data = {}
        _, data = mail.fetch(num, '(RFC822)')
        # print(data[0])
        _, b = data[0]
        email_message = email.message_from_bytes(b)
        for header in ['subject', 'to', 'from', 'date']:
            print("{}: {}".format(header, email_message[header]))
            email_data[header] = email_message[header]
        for part in email_message.walk():
            if part.get_content_type() == "text/plain":
                body = part.get_payload(decode=True)
                email_data['body'] = body.decode()
            elif part.get_content_type() == "text/html":
                html_body = part.get_payload(decode=True)
                email_data['html_body'] = html_body.decode()
        my_message.append(email_data)
        #print(my_message)
    return jsonify(my_message)
@app.route('/result')
def op():
    conn = sqlite3.connect('email_db.db',check_same_thread=False)
    result=conn.execute("select * from EMAIL1").fetchall()
    return render_template("popup.html",status=result)
@app.route('/ext',methods=["GET","POST"])
def ext():
    conn = sqlite3.connect('email_db.db', check_same_thread=False)
    result = conn.execute("select * from EMAIL1").fetchall()
    num = len(result)
    Phish=conn.execute("select COUNT(URL_PHISHING) from EMAIL1 where URL_PHISHING=1").fetchone()
    ep=Phish[0]
    inbox={}
    inbox={'MailsChecked':num,'PhishingEmails':ep}

    return inbox

 
if __name__ == "__main__":
        app.run(debug=True)

