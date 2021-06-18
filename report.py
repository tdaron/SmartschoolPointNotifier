import fitz
import json
import re


COURSE_GROUP = 2
COURSE_TOTAL_GROUP = 10
TEACHER_GROUP = 4
UAA_NAME_GROUP = 6
UAA_WEIGHT_GROUP = 7
UAA_RESULTS_GROUP = 8


def getCourseFromIndex(index, text):
    course = []
    while True:
        if index == len(text) - 1:
            break
        l = text[index]
        if l in ["1","2","3","4","5"] or l == "":
            pass
        else:
            if l.startswith("("):
                break 
            course.append(l)
        index += 1
    return course

class Report:
    def __init__(self, filename):
        self.filename = filename
        self.data = []
    def process(self):
        with fitz.open(self.filename) as doc:
            text = ""
            for page in doc:
                text += page.getText()
        text = text.split("Remédiation")
        if len(text) < 2:
            print("#################")
            print("BULLETIN INVALIDE")
            print("#################")
            return False
        text = text[1]
        text = text.split("\n")

        profs = []
        courses = []
        points = {}
        totals = []

        courses.append(" ".join(getCourseFromIndex(0, text))) #Getting first course

        for index in range(0,len(text) - 1):
            line = text[index]
            if line == "":
                continue #Ignore white lines
            if line.startswith("("):
                line = line.replace("(","")
                line = line.replace(")","")
                profs.append(line)
                continue
            if line.endswith("%"):
                try: 
                    linePoints = float(text[index+1].replace(",","."))
                except:
                    linePoints = None

                splitted = line.split(" ")
                ponderation = float(splitted[-1].replace("%",""))
                del splitted[-1]

                data = {"uaa": " ".join(splitted),
                    "weight": ponderation,
                    "value": linePoints
                }

                
                if profs[-1] in points.keys():
                    points[profs[-1]].append(data)
                else:
                    points[profs[-1]] = [data]
            if line == "TOTAL":
                totals.append(text[index + 1])
                courses.append(" ".join(getCourseFromIndex(index + 2, text)))
        del courses[-1] #Remove conseil comment from courses   

        data = []

        for prof in profs:
            index = profs.index(prof)
            data.append({
                "prof": prof,
                "cours": courses[index],
                "total": totals[index],
                "points": points[prof]
            })

        self.data = data
        return True
    

    def process_beta(self):

        with fitz.open(self.filename) as doc:
            text = ""
            for page in doc:
                text += page.getText()

        text = text.split("Remédiation")
        text = text[1]
        pattern = re.compile(r"((([A-Z\n\s]+)[a-zA-Z0-9\s\(\)]+)\n\(([\s\D]+)\)\n)?(([A-Z][^A-Z\%]+)\s(\d+)%\n?([\d\,]*)?)?(\n?TOTAL\n([\d\,]+)\n?)?", re.DOTALL | re.MULTILINE)
        results = list(re.finditer(pattern, text))
        current_course = ""
        data = []

        for (match, x) in zip(results, range(0,len(results) - 1)):
            # Case of course start
            course = match.group(COURSE_GROUP)
            teacher = match.group(TEACHER_GROUP)
            #Case of point line
            uaa_name = match.group(UAA_NAME_GROUP)
            uaa_weight = match.group(UAA_WEIGHT_GROUP)
            uaa_points = match.group(UAA_RESULTS_GROUP)
            total_value = match.group(COURSE_TOTAL_GROUP)
            if course == None and x == 0:
                print("#################")
                print("BULLETIN INVALIDE")
                print("#################")
                return False
            if course != None:
                current_course = course.replace("\n"," ")
                data.append({
                    "prof": "Bob",
                    "cours": current_course,
                    "total": None,
                    "points": []

                })
                if teacher != None:
                    data[-1]["prof"] = " ".join(teacher.split(" ")[::-1])
                else:
                    print("Missing teacher for ", course)
                
            if uaa_name != None:
                data[-1]["points"].append({
                    "uaa": uaa_name.replace("\n", " "),
                    "weight": int(uaa_weight),
                    "value": None if uaa_points == None or uaa_points == "" else float(uaa_points.replace(",",".")),
                })
                data[-1]["total"] = 0 if total_value == None or total_value == "" else float(total_value.replace(",","."))
        self.data = data
        return True






                



        
