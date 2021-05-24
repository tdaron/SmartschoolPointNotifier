import fitz
import json

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
        self.data = {}
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
    




                



        
