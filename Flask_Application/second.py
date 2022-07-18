from flask import Blueprint, jsonify, render_template
import base64, imaplib, email, re, os
import sqlite3,requests

second=Blueprint("second",__name__,static_folder="static",template_folder="templates")   

@second.route('/unread')
def unread():
    global UN, PW, host
    UN='sandeep.18bec@cmr.edu.in'
    PW='Sandeep#2911'
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
@second.route('/result')
def op():
    conn = sqlite3.connect('email_db.db',check_same_thread=False)
    result=conn.execute("select * from EMAIL").fetchall()
    return render_template("popup.html",q=result)
    

# user = '1ep18cs017.cse@eastpoint.ac.in'
# password = 'charlie_X95'
# imap_url = 'imap.gmail.com'
# con = imaplib.IMAP4_SSL(imap_url)  
  
# # logging the user in 
# con.login(user, password)
# con.select('inbox')
