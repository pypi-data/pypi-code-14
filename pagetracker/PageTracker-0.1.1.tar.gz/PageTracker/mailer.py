#!/usr/bin/python
# Adapted from http://kutuma.blogspot.com/2007/08/sending-emails-via-gmail-with-python.html
import json
import getpass
import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email.MIMEText import MIMEText
from email import Encoders
# from textMessenger import *
import os

with open('config.JSON','r') as f:
  credentials = json.load(f)
  # print credentials


gmail_user = credentials['gmail_id']
gmail_pwd = credentials['gmail_password']
# print gmail_user
# print gmail_pwd
# server    = 'http://ec2-54-200-231-81.us-west-2.compute.amazonaws.com:8080'

def generate_message(text):
   print 'generating messages'
   print text
   for user in text:
      textMessage = ''
      htmlcode = '<table style="border-collapse: collapse;width: 100%;">\
  <tr>\
    <th style="text-align: left;padding: 8px;background-color: #CC0000;color: white;">Course</th>\
    <th style="text-align: left;padding: 8px;background-color: #CC0000;color: white;">Status</th>\
    <th style="text-align: left;padding: 8px;background-color: #CC0000;color: white;">Seats</th>\
    <th style="text-align: left;padding: 8px;background-color: #CC0000;color: white;">Unsubscribe</th>\
  </tr>'

      for course in text.get(user):
        textMessage = ' '.join(course[:-2])
        htmlcode = htmlcode + '<tr>\
    <td style="text-align: left;padding: 8px;">'+ course[0]+' '+course[3]+'</td>\
    <td style="text-align: left;padding: 8px;">'+ course[1]+'</td>\
    <td style="text-align: left;padding: 8px;">'+ course[2]+'</td>\
    <td style="text-align: left;padding: 8px;"><a href="http://ec2-54-200-231-81.us-west-2.compute.amazonaws.com/unsubscribe?id='+course[4]+'">Unsubscribe</a></td>\
    </tr>'
    #unsubscribe is the last of the columns
      htmlcode = htmlcode+ '</table>'
      print htmlcode
      stock_message = "Pssstt there've been some changes in the courses you wanted us to track "
      mail(user,"Course updates - Course Sentinel",htmlcode,stock_message)
      # if course[5]:
      #   publish_message(str(course[5]), textMessage)

# def generate_acknowledgement(text):
#   print 'generating acknowledgement'
#   for user in text:
#       htmlcode = '<table style="border-collapse: collapse;width: 100%;">\
#   <tr>\
#     <th style="text-align: left;padding: 8px;background-color: #CC0000;color: white;">Course</th>\
#   </tr>'

#       for course in text.get(user):
#          htmlcode = htmlcode + '<tr>\
#     <td style="text-align: left;padding: 8px;">'+ course+'</td>\
#     </tr>'
#       htmlcode = htmlcode+ '</table>'
#       print htmlcode
#       stock_message = " Hey there !!,\
#       Thank for signing up, alerts for the following courses have been enabled"

#       mail(user,"Course updates - Course Sentinel",htmlcode,stock_message)


# def mail(to, subject, text, stock_message, attach=None):
def mail(to, subject, stock_message, attach=None):
  msg = MIMEMultipart()
  msg['From'] = gmail_user
  msg['To'] = to
  msg['Subject'] = subject
  #msg.attach(MIMEText(plain, 'plain'))



  msg.attach(MIMEText(stock_message,'plain'))
  # msg.attach(MIMEText(text, 'html'))

  if attach:
    part = MIMEBase('application', 'octet-stream')
    part.set_payload(open(attach, 'rb').read())
    Encoders.encode_base64(part)
    part.add_header('Content-Disposition', 'attachment; filename="%s"' % os.path.basename(attach))
    msg.attach(part)

  mailServer = smtplib.SMTP("smtp.gmail.com", 587)
  mailServer.ehlo()
  mailServer.starttls()
  mailServer.ehlo()
  mailServer.login(gmail_user, gmail_pwd)
  mailServer.sendmail(gmail_user, to, msg.as_string())
  mailServer.close()

# 