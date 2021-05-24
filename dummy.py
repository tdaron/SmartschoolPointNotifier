import pickle, os, random

def save(data):
    pickle.dump( data, open( "save.pickle", "wb" ) )
    print("Sauvé !")

if os.path.isfile("save.pickle"):
    data = pickle.load( open( "save.pickle", "rb" ) )
else:
    data = []
    save(data)

for user in data:
    userIndex = data.index(user)
    course = random.choice(user)
    courseIndex = user.index(course)
    toEdit = {
        "value": None
    }
    while toEdit["value"] == None:
        toEdit = random.choice(course["points"])

    index = course["points"].index(toEdit)
    toEdit["value"] = None
    print("Points de " + toEdit["uaa"]+" supprimés")
    data[userIndex][courseIndex][index] = toEdit
save(data)

