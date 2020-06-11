from itertools import chain
from sys import stdout

ELEMENTS = ['Fraise', 'Pomme', 'Banane', 'Melon', 'Pêche', 'Cerise',
            'Mandarine', 'Orange', 'Raisin', 'Framboise', 'Abricot',
            'Poire', 'Ananas', 'Kiwi', 'Mangue','Pasteque', 'Pamplemousse',
            'Prune', 'Mirtille', 'Mûre', 'Figue']

ELEMENTS = ['Fraise', 'Pomme', 'Banane', 'Melon', 'Pêche', 'Cerise',
            'Mandarine', 'Orange', 'Raisin', 'Framboise']

QUESTION = 'Qui est le meilleur ?'

NOMBRE_QUESTION_TOTAL = 0
NOMBRE_QUESTION_FAIT = 0
NOMBRE_QUESTION_REEL = 0

CHOIX_GAUCHE = ''.join(map(chr, [27, 91, 68]))
CHOIX_DROITE = ''.join(map(chr, [27, 91, 67]))
CHOIX_ANNULER = 'annuler'


def main():
    global NOMBRE_QUESTION_TOTAL
    NOMBRE_QUESTION_TOTAL = calculerNombreQuestion(ELEMENTS)
    elements = ELEMENTS.copy()
    triFusion(elements, 0, len(elements))
    afficherResultat(elements)
    afficherStatistiques()


# réalise un tri en place de élements entre debut (inclus) et fin (exclus)
def triFusion(elements, debut, fin):
    if fin-debut == 1:
        return
    else:
        milieu = (debut+fin) // 2
        triFusion(elements, debut, milieu)
        triFusion(elements, milieu, fin)
        fusionneTriee(elements, debut, milieu, fin)


# fusionne 2 listes triés (debut-milieu et milieu-fin) en une seule liste triée
def fusionneTriee(elements, debut, milieu, fin):
    global NOMBRE_QUESTION_FAIT, NOMBRE_QUESTION_REEL
    liste1 = elements[debut:milieu]
    liste2 = elements[milieu:fin]
    iterListe1 = iter(liste1)
    iterListe2 = iter(liste2)
    smallestListe1 = None
    smallestListe2 = None
    listeResultat = []
    derniersChoix = [] # 1 pour la liste 1 et 2 pour la liste 2

    try:
        smallestListe1 = next(iterListe1)
        smallestListe2 = next(iterListe2)
        while True:
            comparaison = estMieuxQue(smallestListe1, smallestListe2)
            if comparaison == 1:
                derniersChoix.append(1)
                listeResultat.append(smallestListe1)
                smallestListe1 = None
                smallestListe1 = next(iterListe1)
            elif comparaison == 2:
                derniersChoix.append(2)
                listeResultat.append(smallestListe2)
                smallestListe2 = None
                smallestListe2 = next(iterListe2)
            else: # annuler
                haut = '\033[A'
                gauche = 60 * '\b'
                espace = 60 * ' '
                if derniersChoix == []:
                    print(2 * (haut + espace + gauche) + 'Retour en arriere impossible :(')
                else:
                    print(3 * (haut + espace + gauche), end = haut)
                    choix = derniersChoix.pop()
                    NOMBRE_QUESTION_REEL -= 1
                    NOMBRE_QUESTION_FAIT -= 1
                    if choix == 1:
                        iterListe1 = chain([smallestListe1], iterListe1)
                        smallestListe1 = listeResultat.pop()
                    elif choix == 2:
                        iterListe2 = chain([smallestListe2], iterListe2)
                        smallestListe2 = listeResultat.pop()
    except:
        reste = [smallestListe1] + list(iterListe1) if smallestListe2 is None else \
                [smallestListe2] + list(iterListe2) 
        listeResultat.extend(reste)
        NOMBRE_QUESTION_FAIT += len(reste)-1
    elements[debut:fin] = listeResultat


# compare les deux éléments et renvoie 1 lorsque le premier est le meilleur,
#  0 sinon et -1 en cas de retour en arriere
def estMieuxQue(element1, element2):
    global NOMBRE_QUESTION_FAIT, NOMBRE_QUESTION_TOTAL, NOMBRE_QUESTION_REEL
    choix = ''
    nombreTentative = 0
    while choix not in (CHOIX_GAUCHE, CHOIX_DROITE, CHOIX_ANNULER):
        nombreTentative += 1
        if nombreTentative >= 2:
            print('{} n\'est pas un choix valide !\n'.format(choix))
        ratio = int(100 * NOMBRE_QUESTION_FAIT / NOMBRE_QUESTION_TOTAL)
        print('{} {} ou {} [{}%]'.format(QUESTION, element1, element2, ratio))
        choix = input()

        if choix == CHOIX_ANNULER:
            return -1

    print("\033[A" + (element1 if choix == CHOIX_GAUCHE else element2))
    NOMBRE_QUESTION_FAIT += 1
    NOMBRE_QUESTION_REEL += 1
    return 1 if choix == CHOIX_GAUCHE else 2


# affiche les éléments de façon jolie avec leur place
def afficherResultat(elements):
    print("\n ----- Resultats -----")
    for i,e in enumerate(elements):
        print('\t{}\t{}'.format(i, e))

# affiche quelques statistiques à la fin du classement
def afficherStatistiques():
    print("\n ----- Stats -----")
    print("\t{}\tquestions posées".format(NOMBRE_QUESTION_REEL))
    print("\t{}\tquestions maximum".format(NOMBRE_QUESTION_TOTAL))


# calcule le nombre maximal de question pour trier les éléments
def calculerNombreQuestion(elements):
    n = len(elements)
    puissance2superieure = 1
    log2n = 0
    nombreQuestion = 0
    for i in range(1, n+1):
        nombreQuestion += log2n
        if i == puissance2superieure:
            puissance2superieure *= 2
            log2n += 1
    return nombreQuestion


main()
