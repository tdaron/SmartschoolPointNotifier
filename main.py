from smartschool import SmartschoolApi
from report import Report
from messages import getMessage
api = SmartschoolApi("https://cnddinant.smartschool.be")
#api.authenticate("USERNAME","PASSWORD")
#api.getGrade("test.pdf")

#report = Report("test.pdf")
#report.process()

# Testing messages génération

print(getMessage("Théo Daron",8.7,"MATH"))