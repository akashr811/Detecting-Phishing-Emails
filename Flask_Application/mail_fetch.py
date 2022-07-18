import re
import sqlite3, requests
from integration import *

response = requests.get('http://127.0.0.1:5000/res')
data = len(response.json())
sr = response.json()
conn = sqlite3.connect('email_db.db', check_same_thread=False)

listofTabs = conn.execute("select name from sqlite_master where type='table' AND name='EMAIL'").fetchall()

if listofTabs != []:
    print("Table exist already")
else:
    conn.execute('''create table EMAIL1(
                             ID integer primary key autoincrement,
                             SENDER text,
                             SUBJECT text,
                             DATE text,
                             MESSAGE_BODY text,
                             PHISHING text,
                             TEXT_PHISHING text,
                             TEXT_PROB number,
                             URL_PHISHING text,
                             LINKS text,
                             LINK_PROB number
                             )''')
    print("Table Created Successfully")
cur = conn.cursor()
if response.status_code == 200 and data is not None:
    for i in range(data):
        # getbody=sr[i]['body']
        getsender = sr[i]['from']
        getsub = sr[i]['subject']
        gethbody = sr[i]['html_body']
        getdate = sr[i]['date']

        # result, data = con.uid('search', None, "ALL") # search and return uids instead
        # latest_email_uid = data[0].split()[-1]
        # result, data = con.uid('fetch', latest_email_uid, '(RFC822)')
        # raw_email = data[0][1]
        # email_message = email.message_from_bytes(raw_email)
        # #### parsing email
        # sender = email_message['From']
        # date = email_message['Date']
        # subject = email_message['Subject']

        # print('To:', email_message['To'])
        # print('Sent from:', email_message['From'])
        # print('Date:', email_message['Date'])
        # print ('Subject:', email_message['Subject'])
        print('*' * 69)
        # cleantext=email_message.get_payload()[0].get_payload()
        cleantext = gethbody


        def Find(string):
            # findall() has been used
            # with valid conditions for urls in string
            url = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\), ]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', string)

            # url = re.findall('https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+', string)
            return url


        url = Find(cleantext)
        urls = []
        for i in url:
            if i not in urls:
                urls.append(i)
        print(urls)
        print('*' * 30, 'MESSAGE', '*' * 30)
        # print(string)
        text_prob, text_pred = text_prediction(cleantext)
        print(text_prob)
        if len(urls) == 0:
            url_prob = 0
            url_pred = 0
        else:
            url_prob, url_pred = url_prediction(urls)

        print(url_prob)


        def is_phish(text_pred, url_pred, text_prob, url_prob):
            if (text_pred == 1) and (url_pred == 1):
                phishing = 1
            elif (text_pred == 1) and (url_pred == 0):
                if (text_prob > 0.97):
                    phishing = 1
                else:
                    phishing = 0
            elif (text_pred == 0) and (url_pred == 1):
                if (url_prob > 0.97):
                    phishing = 1
                else:
                    phishing = 0
            else:
                phishing = 0
            return phishing


        phishing = is_phish(text_pred, url_pred, text_prob, url_prob)
        print("final classify " + str(phishing))
        RES = conn.execute('''INSERT INTO EMAIL1 (SENDER,SUBJECT,DATE,MESSAGE_BODY,PHISHING,TEXT_PHISHING,TEXT_PROB,URL_PHISHING,LINK_PROB)
            VALUES (?,?,?,?,?,?,?,?,?)''', (getsender, getsub, getdate, cleantext, int(phishing), int(text_pred), text_prob, int(url_pred), url_prob));
        conn.commit()
        conn.close()
