#!/usr/bin/python
# vi: set et sts=4 sw=4 ts=4 :

import re
import certifi
import httplib2
import gdata.gauth
import gdata.spreadsheets.client
#from oauth2client.client import flow_from_clientsecrets
#from oauth2client.file import Storage
import oauth2client.client
import oauth2client.file

scope = 'https://www.googleapis.com/auth/userinfo.email https://www.googleapis.com/auth/userinfo.profile https://docs.google.com/feeds/ https://docs.googleusercontent.com/ https://spreadsheets.google.com/feeds/'
redirect_uri = 'urn:ietf:wg:oauth:2.0:oob'
user_agent = 'orimanabu'
secret_file = 'clientsecret.json'
cred_file = 'cred.json'

flow = oauth2client.client.flow_from_clientsecrets(secret_file, scope=scope, redirect_uri=redirect_uri)
storage = oauth2client.file.Storage(cred_file)
cred = storage.get()
if cred is None or cred.invalid:
    #cred = run_flow(flow, storage, None)
    auth_uri = flow.step1_get_authorize_url()
    print 'Please go to this URL and get an authentication code:'
    print auth_uri
    print
    code = raw_input('Please input the authentication code here:')
    h = httplib2.Http(ca_certs=certifi.where())
    cred = flow.step2_exchange(code, http=h)
    storage.put(cred)

token = gdata.gauth.OAuth2Token(client_id=cred.client_id, client_secret=cred.client_secret, scope=scope, access_token=cred.access_token, refresh_token=cred.refresh_token, user_agent=user_agent)

client = gdata.spreadsheets.client.SpreadsheetsClient()
token.authorize(client)

print
print "Test #1: list all spreadsheets"
sheets = client.get_spreadsheets()
for entry in sheets.entry:
    sid = re.sub(r'.*\/', '', entry.get_id())
    print "title:", entry.title.text
    print "  url:", entry.get_id()
    print "   id:", sid
    if entry.title.text == 'platform-gps-prjs-201408':
        prjs_sheet_id = sid

print
print "Test#2: list all worksheets in 'platform-gps-prjs-201408 (%s)'" % prjs_sheet_id
worksheets = client.get_worksheets(prjs_sheet_id)
for entry in worksheets.entry:
    wid = re.sub(r'.*\/', '', entry.get_id())
    print "title:", entry.title.text
    print "  url:", entry.get_id()
    print "   id:", wid
    if entry.title.text == 'platform-gps-prjs-201407':
        prjs_worksheet_id = wid

print
print "Test#3: list some columns of raw #1 in 'platform-gps-prjs-201408'"
row = 1
for column in range(1, 10):
    cell = client.get_cell(prjs_sheet_id, prjs_worksheet_id, 1, column)
    print "  [%d, %d] %s" % (row, column, cell.content.text)
