from smartschool import SmartschoolApi
from report import Report
from messages import getMessage
from ifttt import sendNotification
import pickle, json, os


users = json.load(open("users.json","r"))
api = SmartschoolApi("https://cnddinant.smartschool.be")


def save(data):
    pickle.dump( data, open( "save.pickle", "wb" ) )


if os.path.isfile("save.pickle"):
    data = pickle.load( open( "save.pickle", "rb" ) )
else:
    data = []
    save(data)


for user in users["users"]:
#for user in []:
    print(user["username"])
    userIndex = users["users"].index(user)
    api.authenticate(user["username"],user["password"])
    api.getGrade("report.pdf")
    report = Report("report.pdf")
    if report.process_beta():
        if data == [] or len(data) < userIndex + 1:
            print("Saving for the first time")
            data.append(report.data)
            save(data)
            continue


        for cours in report.data:
            courseIndex = report.data.index(cours)
            for uaa in cours["points"]:
                uaaIndex = cours["points"].index(uaa)
                points = uaa["value"]
                current = data[userIndex][courseIndex]["points"][uaaIndex]["value"]
                if current != points:
                    isRetry = True if current != None else False
                    print("Sending notification...")
                    message = getMessage(cours["prof"],points,cours["cours"],uaa["uaa"], isRetry)
                    print(message)
                    print(sendNotification(message, user["token"]))
        data[userIndex] = report.data
        save(data)


