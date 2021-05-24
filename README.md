# This is a tool to notify you when you got new points on smartschool

## Setup

1. Create IFTTT Applet with webhook ( eventName: "notification" ) , message will be in value1
   Exemple: 
        IF webhook
        THEN notify , message: {{ value1 }}
2. Complete users.json with your smartschool credentials ( username, password ) and with your ifttt webhooks token
3. Edit main.py to put your smartschool base url instead of mine
4. Regulary run main.py to check if there is new points in your grade. 