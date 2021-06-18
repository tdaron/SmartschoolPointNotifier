import random
import string

def sanitize(matiere):
    m = string.capwords(matiere.replace("Gr2","").replace("Gr1","").replace("6h","").replace("2h","").replace("LM1","").replace("(","").replace(")","").lower().lstrip())
    return m
def getMessage(prof, points, matiere,uaa,isRetry):
    if points == 10:
        s =  random.choice(sentences["full"])
    elif points > 8:
        s =  random.choice(sentences["gg"])
    elif points >= 5:
        s = random.choice(sentences["ok"])
    elif points >= 4.8:
        s = random.choice(sentences["fuck"])
    elif points >= 3.5:
        s = random.choice(sentences["bad"])
    else:
        s = random.choice(sentences["nul"])

    return s.replace("$PR",prof).replace("$UAA",uaa).replace("$PO",str(points).replace(".0","")).replace("$M",sanitize(matiere)) + (" (REPASSE)" if isRetry else "")


sentences = {
    "full": [
        "La légende disait vrai: 100% en $M pour $UAA",
        "10 en $M ( $UAA )! Même $PR ne sait pas comment t'as fait!",
        "Impossible d'avoir le maximum en $M, surtout pour $UAA, juste respect",
        "Wow la vache ! 10 en $M pour $UAA, tout le monde sera jaloux !"
    ],
    "gg": [
        "GG t'as eu $PO en $M pour $UAA",
        "$PR t'a mis $PO en $M ( $UAA ), bien joué",
        "T'as géré mec t'as eu $PO en $M - $UAA",
        "$PO en $M ( $UAA ), de la chance ou du talent?",
        "Bien joué pour $M, t'as eu $PO - $UAA"
    ],
    "ok": [
        "T'as eu $PO en $M pour $UAA",
        "C'est carré, $PO en $M sur $UAA",
        "Franchement $PO en $M c'est clean ($UAA)",
        "T'as réussi l'exam de $UAA en $M ($PO)",
        "Rien à dire, $PO en $M sur $UAA",
        "$PO en $M - $UAA;)"
    ],
    "fuck": [
        "Arrêteee, $PR a fait le chien ($PO) #IlFaudraRecommencer",
        "Le seummm, $PO en $M",
        "T'inquiète ça arrive, faut pas se pendre ($PO en $M, $UAA)",
        "$PR a même pas arrondi ($PO)",
        "NOOOOOOOON $PO en $M, faudra repasser $UAA",
        "Espèce de victime ! $PO en $M lol"
    ],
    "bad": [
        "Ohh merde, $PR vient de mettre $PO pour $UAA",
        "Tu vas devoir repasser l'exam sur $UAA en $M",
        "Nonnn ça craint $PO en $M ( $UAA )",
        "T'as raté l'exam en $M ($PO)",
        "Pour coder y a du monde, mais pour réussir $M la y a personne..."
    ],
    "nul": [
        "$PO en $M? T'es sérieux là? Tu me désespères...",
        "Tu pues la merde en $M, non? ($PO)",
        "A mon avis t'as rien branlé avant l'exam de $M ($PO)",
        "$PR fait chier, il t'a mis $PO",
        "Je préfère pas faire de commentaire sur l'exam de $M",
        "N'importe quoi, $PO en $M",
        "Bon.. Sors toi les dois du cul en $M, t'as eu $PO"
    ]
}

