Depends:
========
* oath2client (https://github.com/google/oauth2client/)
* certifi (https://github.com/certifi/python-certifi/)
* gdata-python-client (https://code.google.com/p/gdata-python-client/)

gdata-python-client is also available as python-gdata RPM package.

Usage:
======
When you run this script first time, you'll asked like:

> Please go to this URL and get an authentication code:
> http2://accounts.google.com/o/oauth...

Then open the browser with the URL above, and you'll see a page requesting your grants for accessing your data in Google Apps.
If you accept, you can get auth code.
Copy the code and paste on the terminal in which this script is running.

Note that your credential information is stored in ./cred.json.
