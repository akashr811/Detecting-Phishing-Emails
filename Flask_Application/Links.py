# import http
# from urllib import response
# import httplib2
# from bs4 import BeautifulSoup,SoupStrainer

# url='http://127.0.0.1:5000/unread'
# http=httplib2.Http()
# response,content = http.request(url)
# links=[]
# for link in BeautifulSoup(content).find_all('a',href=True):
#     links.append(link['href'])

# for link in links:
#     print(links)


from string import punctuation
from prettytable import PrettyTable
from asyncio.windows_events import NULL
from email.quoprimime import body_check
import json
import re
from urllib import response
#from flask import Flask,request
import requests
import pandas as pd
from integration import *
import sqlite3
import numpy as np
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

response=requests.get('http://127.0.0.1:5000/res')


sender=[]
sub=[]
hbody=[]
links=[]
data=len(response.json())
sr=response.json()

#------------------------------------------
#body1=response.json()[0]['subject']
# data=response.text
# json.loads(data)
# #sub=parse_json['subject']
# print(sub)
#------------------------------------------
def preprocess_text(text):
          text = text.lower()  # Lowercase text
          text = re.sub(f"[{re.escape(punctuation)}]", "", text)  # Remove punctuation
          text = " ".join(text.split())  # Remove extra spaces, tabs, and new lines
          return text
     
 


# if response.status_code == 200:
#         for i in range(data):
#             sender.append(sr[i]['from'])
#             sub.append(sr[i]['subject'])
#             hbody.append(sr[i]['html_body'])

#------------------------------------------
        # for i in response.json()[c]['subject']:
            # res.append(response.json()[0]['subject'])
            # c+=1
# print(f"sdetails: {sender}")
# print(f"subdetails: {sub}")
# print(f"hbodydetails: {hbody}")
#------------------------------------------



nltk.download("stopwords")
stopwords_ = set(stopwords.words("english"))

connection=sqlite3.connect("Project.db",check_same_thread=False)
listofTabs = connection.execute("select name from sqlite_master where type='table' AND name='user'").fetchall()

if listofTabs!=[]:
    print("Table exist already")
else:
    connection.execute('''create table user(
                             ID integer primary key autoincrement,
                             dbbfrom text,
                             dbsubject text,
                             dbhtmlbody text,
                             dbparsehtml text,
                             dblinks text
                             )''')
    print("Table Created Successfully")
cur = connection.cursor()

#global gethbody
if response.status_code == 200 and data is not None:
        for i in range(data):
            getsender=sr[i]['from']
            getsub=sr[i]['subject']
            gethbody=sr[i]['html_body']
            #------------------------------------------
            #urls=[]
            urls = re.findall('https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+', gethbody) 
            
            sender.append(sr[i]['from'])
            sub.append(sr[i]['subject'])
            hbody.append(sr[i]['html_body'])
            links.append(urls)
            #------------------------------------------
            df=pd.DataFrame(list(gethbody))
            # df.map(preprocess_text)
            sample_text=(preprocess_text(gethbody))
            clean_text = sample_text.lower()
            #print_text(sample_text, clean_text)
            #urls=[]
            #urls = re.findall('https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+', clean_text) 
            #re.findall(r'(https?://\S+)', s)
            #regex=r"\b((?:https?://)?(?:(?:www\.)?(?:[\da-z\.-]+)\.(?:[a-z]{2,6})|(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)|(?:(?:[0-9a-fA-F]{1,4}:){7,7}[0-9a-fA-F]{1,4}|(?:[0-9a-fA-F]{1,4}:){1,7}:|(?:[0-9a-fA-F]{1,4}:){1,6}:[0-9a-fA-F]{1,4}|(?:[0-9a-fA-F]{1,4}:){1,5}(?::[0-9a-fA-F]{1,4}){1,2}|(?:[0-9a-fA-F]{1,4}:){1,4}(?::[0-9a-fA-F]{1,4}){1,3}|(?:[0-9a-fA-F]{1,4}:){1,3}(?::[0-9a-fA-F]{1,4}){1,4}|(?:[0-9a-fA-F]{1,4}:){1,2}(?::[0-9a-fA-F]{1,4}){1,5}|[0-9a-fA-F]{1,4}:(?:(?::[0-9a-fA-F]{1,4}){1,6})|:(?:(?::[0-9a-fA-F]{1,4}){1,7}|:)|fe80:(?::[0-9a-fA-F]{0,4}){0,4}%[0-9a-zA-Z]{1,}|::(?:ffff(?::0{1,4}){0,1}:){0,1}(?:(?:25[0-5]|(?:2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(?:25[0-5]|(?:2[0-4]|1{0,1}[0-9]){0,1}[0-9])|(?:[0-9a-fA-F]{1,4}:){1,4}:(?:(?:25[0-5]|(?:2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(?:25[0-5]|(?:2[0-4]|1{0,1}[0-9]){0,1}[0-9])))(?::[0-9]{1,4}|[1-5][0-9]{4}|6[0-4][0-9]{3}|65[0-4][0-9]{2}|655[0-2][0-9]|6553[0-5])?(?:/[\w\.-]*)*/?)\b"
            #urls=re.findall(regex, clean_text)
            #clean_text=re.sub(regex,"", clean_text)
            #re.sub('https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+',"", clean_text)
            print(urls)
            print (links)
            tokens = clean_text.split()
            clean_tokens = [t for t in tokens if not t in stopwords_]
            clean_text = " ".join(clean_tokens)
            word_tokenize(clean_text)
            print(clean_text)
            #---------------------------
            connection.execute("INSERT INTO user (dbbfrom,dbsubject,dbhtmlbody,dbparsehtml) VALUES ('"+getsender+"','"+getsub+"','"+gethbody+"','"+clean_text+"')")
            connection.commit()
            #connection.execute("INSERT INTO user (dbparsehtml) VALUES ('"+clean_text+"')")
            
query = cur.execute("SELECT * FROM user").fetchall()   
table=PrettyTable(query)         
print(table)

#------------------------------------------
#############

# parsed data //html parser

##############
# abc=cur.execute("SELECT dbhtmlbody FROM user as qw").fetchall()
# ocs={}
# for row in abc:
#     #ocs[row[0]]=int(row[0])
#     print(row)
#------------------------------------------


from html.parser import HTMLParser
class Parser(HTMLParser):
  # method to append the start tag to the list start_tags.
  def handle_starttag(self, tag, attrs):
    global start_tags
    start_tags.append(tag)
    # method to append the end tag to the list end_tags.
  def handle_endtag(self, tag):
    global end_tags
    end_tags.append(tag)
  # method to append the data between the tags to the list all_data.
  def handle_data(self, data):
    global all_data
    all_data.append(data)
  # method to append the comment to the list comments.
  def handle_comment(self, data):
    global comments
    comments.append(data)
start_tags = []
end_tags = []
all_data = []
comments = []
mybody=[]
# Creating an instance of our class.
parser = Parser()
# Poviding the input.
#abc[0].encode('ascii','ignore').decode()
abc=cur.execute("SELECT dbhtmlbody FROM user as qw").fetchall()
ocs=len(abc)
def Find(stringed): 
    # findall() has been used  
    # with valid conditions for urls in string 
      pattern1='https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+'
      #pattern1='http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\), ]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
      url = re.findall(pattern1, stringed) 
      return url 
def is_phish(text_pred,url_pred,text_prob,url_prob):
        if(text_pred==1) and (url_pred==1):
            phishing = 1
        elif(text_pred==1) and (url_pred==0):
            if(text_prob>0.97):
                phishing = 1
            else:
                phishing = 0
        elif(text_pred==0) and (url_pred==1):
            if(url_prob>0.97):
                phishing = 1
            else:
                phishing = 0
        else:
            phishing = 0
        return phishing
for row in range(ocs):
    cleantext=abc[row]
    # url=Find(cleantext)
    # urls = [] 
    # for i in url: 
    #     if i not in urls: 
    #         urls.append(i)
    # print(urls)
    print('*'*30, 'MESSAGE', '*'*30)
    #print(string)
    text_prob,text_pred = text_prediction(cleantext)
    print(text_prob)
    if len(urls) == 0:
      url_prob = 0
      url_pred=0
    else:
      url_prob,url_pred = url_prediction(urls)

    print(url_prob)
    
    url=Find(cleantext)
    urls = [] 
    for i in url: 
        if i not in urls: 
            urls.append(i)
    print(urls)
    print('*'*30, 'MESSAGE', '*'*30)
    #print(string)
    text_prob,text_pred = text_prediction(cleantext)
    print(text_prob)
    if len(urls) == 0:
      url_prob = 0
      url_pred=0
    else:
      url_prob,url_pred = url_prediction(urls)

    print(url_prob)
    

    phishing = is_phish(text_pred,url_pred,text_prob,url_prob)
    print("final classify" +str(phishing))
    #new***********
    
  #*******************


    #******************************

    # #ocs[row[0]]=int(row[0])
    # print(abc[row])
    # parser.feed(str(abc[row]))
    # sample_text=all_data
    # #df=pd.DataFrame(list(hbody))
    # #df(hbody).map(preprocess_text)
    # #sample_text=df[hbody].map(preprocess_text)
    # clean_text = sample_text[row].lower()
    # #print_text(sample_text, clean_text)
    # clean_text = re.sub(r"<.*?>", " ", clean_text)
    # #print_text(sample_text, clean_text)
    # urls = re.findall('https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+', clean_text) 
    # #re.findall(r'(https?://\S+)', s)
    # regex=r"\b((?:https?://)?(?:(?:www\.)?(?:[\da-z\.-]+)\.(?:[a-z]{2,6})|(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)|(?:(?:[0-9a-fA-F]{1,4}:){7,7}[0-9a-fA-F]{1,4}|(?:[0-9a-fA-F]{1,4}:){1,7}:|(?:[0-9a-fA-F]{1,4}:){1,6}:[0-9a-fA-F]{1,4}|(?:[0-9a-fA-F]{1,4}:){1,5}(?::[0-9a-fA-F]{1,4}){1,2}|(?:[0-9a-fA-F]{1,4}:){1,4}(?::[0-9a-fA-F]{1,4}){1,3}|(?:[0-9a-fA-F]{1,4}:){1,3}(?::[0-9a-fA-F]{1,4}){1,4}|(?:[0-9a-fA-F]{1,4}:){1,2}(?::[0-9a-fA-F]{1,4}){1,5}|[0-9a-fA-F]{1,4}:(?:(?::[0-9a-fA-F]{1,4}){1,6})|:(?:(?::[0-9a-fA-F]{1,4}){1,7}|:)|fe80:(?::[0-9a-fA-F]{0,4}){0,4}%[0-9a-zA-Z]{1,}|::(?:ffff(?::0{1,4}){0,1}:){0,1}(?:(?:25[0-5]|(?:2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(?:25[0-5]|(?:2[0-4]|1{0,1}[0-9]){0,1}[0-9])|(?:[0-9a-fA-F]{1,4}:){1,4}:(?:(?:25[0-5]|(?:2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(?:25[0-5]|(?:2[0-4]|1{0,1}[0-9]){0,1}[0-9])))(?::[0-9]{1,4}|[1-5][0-9]{4}|6[0-4][0-9]{3}|65[0-4][0-9]{2}|655[0-2][0-9]|6553[0-5])?(?:/[\w\.-]*)*/?)\b"
    # urls=re.findall(regex, clean_text)
    # clean_text=re.sub(regex,"", clean_text)



    # #re.sub('https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+',"", clean_text)


    # print(urls)
    # tokens = clean_text.split()
    # clean_tokens = [t for t in tokens if not t in stopwords_]
    # clean_text = " ".join(clean_tokens)
    # word_tokenize(clean_text)
    # print(clean_text)

    #******************************



    # print("start tags:", start_tags)
    # print("end tags:", end_tags)
    # print("data:", all_data)
    # mybody.append(all_data)
    # print("comments", comments)


# import pandas as pd

# from string import punctuation
# length=len(mybody)
# for i in range(len(mybody)):

#   def print_text(sample, clean):
#           print(f"Before: {sample}")
#           print(f"After: {clean}")
