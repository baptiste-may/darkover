import random


# UTILS

def bool_aleatoire() -> bool:
    """
    Renvoie vrai ou faux aléatoirement
    """
    return random.randint(0, 1) == 0


def lecture_csv(fichier: str) -> list:
    """
    importe le fichier csv, charge son contenu dans un tableau
    :param fichier: nom du fichier csv à traiter
    :return: tableau, liste de listes contenant toutes les informations du fichier
    """
    fichier = open(fichier, "r")
    table = [ligne.rstrip().split(";") for ligne in fichier]
    fichier.close()
    return table


def clear():
    """
    Envoie plusieurs retour à la ligne pour nétoyer la console
    """
    global CLEAR_LINES_NB
    print("\n" * CLEAR_LINES_NB)


def somme(lst: list) -> int:
    """
    Additionne tous les membres d'une liste
    :param lst: La liste
    :return: La somme
    """
    s = 0
    for e in lst:
        s += e
    return s


# OBJECTS

class Pair:
    """
    Une pair de mots
    """

    def __init__(self, mot1: str, mot2: str):
        self.mot1 = mot1
        self.mot2 = mot2

    def aleatoire(self) -> str:
        """
        Renvoie un des deux mots de la pair aléatoirement
        :return: Un des deux mots
        """
        if bool_aleatoire():
            return self.mot1
        return self.mot2

    def inverse(self, mot: str):
        """
        Renvoie l'autre mot de la pair
        :param mot: Le mot initial
        :return: L'autre mot
        """
        if mot == self.mot1:
            return self.mot2
        if mot == self.mot2:
            return self.mot1
        return None


class ListeMots:
    """
    Une liste de pairs de mots
    """

    def __init__(self, file_name: str):
        data = lecture_csv(file_name)
        self.data = []
        for mots in data:
            self.data.append(Pair(mots[0], mots[1]))

    def pair_aleatoire(self) -> Pair:
        """
        Renvoie une pair de deux mots aléatoirement
        """
        return self.data[random.randint(0, len(self.data))]


class Joueur:

    def __init__(self, nom):
        self.uuid = random.getrandbits(8)
        self.nom = nom
        self.role = None
        self.mot = None


class Mots:

    def __init__(self):
        self.donnee = {}

    def mot_existant(self, mot):
        s = False
        for p in self.donnee.values():
            for m in p:
                if m == mot:
                    s = True
        return s

    def personnel(self, uuid):
        return self.donnee[uuid]

    def ajouter_mot(self, uuid, mot):
        if uuid not in self.donnee.keys():
            self.donnee[uuid] = []
        self.donnee[uuid].append(mot)


class Game:
    """
    Les informations d'une partie
    """

    def __init__(self):
        self.joueurs = []
        self.nb_joueurs = 0
        self.pair = None
        self.vrai_mot = None
        self.compo = {}
        self.mots = Mots()

    def ajouter_joueur(self, nom_joueur: str):
        """
        Ajoute un joueur à la partie
        :param nom_joueur: Le nom du joueur
        """
        self.joueurs.append(Joueur(nom_joueur))
        self.nb_joueurs += 1

    def demarer(self, data, nb_espions, white):
        """
        Démmare la partie
        """

        self.pair = data.pair_aleatoire()

        self.compo["white"] = 1 if white else 0
        self.compo["espions"] = nb_espions
        self.compo["civils"] = self.nb_joueurs - self.compo["espions"] - self.compo["white"]

        temp_compo = []
        for role, nb in self.compo.items():
            for i in range(int(nb)):
                temp_compo.append(role)
        random.shuffle(temp_compo)

        self.vrai_mot = self.pair.mot1 if bool_aleatoire() else self.pair.mot2

        for i in range(len(self.joueurs)):
            clear()
            joueur = self.joueurs[i]
            joueur.role = temp_compo[i]
            input("{}, appuis sur [Entrer] pour voir ton mot".format(joueur.nom))
            if joueur.role == "white":
                mot = "Tu es Mister White"
            elif joueur.role == "civils":
                mot = self.vrai_mot
            else:
                mot = self.pair.inverse(self.vrai_mot)
            print("Ton mot est :", mot)
            input("[Suivant]")

        clear()

        manche = 0

        while somme(list(self.compo.values())) > 0:

            manche += 1

            random.shuffle(self.joueurs)

            for joueur in self.joueurs:
                clear()
                while True:
                    print("{}, entre ton {} mot".format(joueur.nom, str(manche) + ("er" if manche == 1 else "e")))
                    mot = input()
                    if mot == "":
                        print("Ce n'est pas un mot")
                    elif self.mots.mot_existant(mot):
                        print("Ce mot a déjà était dit")
                    else:
                        self.mots.ajouter_mot(joueur.uuid, mot)
                        break

            clear()

            message = "\n- Manche {} -\n\nVoici les mots dits :\n".format(manche)

            for joueur in self.joueurs:
                message += "* " + joueur.nom + ": "
                for mot in self.mots.personnel(joueur.uuid):
                    message += mot + ", "
                message = message[:-2]
                message += "\n"

            print(message)
            input("\n" + "[Passer au vote]")


# VARIABLES

DATA = ListeMots("data.csv")

CLEAR_LINES_NB = 100

# RUNNING

while True:
    clear()
    print("""
    -- DARKOVER --
    
    [A] Jouer
    [B] A propos
    [C] Quitter
    """)
    action = input().lower()
    match action:
        case "a":
            game = Game()

            while True:
                print("Entrez le nombre de joueurs")
                nb_joueurs = input()
                try:
                    nb_joueurs = int(nb_joueurs)
                    assert nb_joueurs >= 4, "NoAmontPlayer"
                    break
                except ValueError:
                    print()
                except AssertionError:
                    print("Il faut au moins 4 joueurs pour commencer une partie")

            while True:
                print("Veux-tu un Mister White ? (O/N)")
                white = input().lower()
                if "o" in white:
                    white = True
                    break
                elif "n" in white:
                    white = False
                    break

            max_espions = round(nb_joueurs * (1 / 5))
            nb_espions = 0
            if max_espions == 1:
                nb_espions = 1
            else:
                while True:
                    print("Entrez le nombre d'espions (entre {} et {})".format(1, max_espions))
                    nb_espions = input()
                    try:
                        nb_espions = int(nb_espions)
                        assert 1 <= nb_espions <= max_espions
                        break
                    except ValueError:
                        print()
                    except AssertionError:
                        print("")

            for i in range(nb_joueurs):
                print("Joueur {}, veuillez entrer votre pseudo".format(i + 1))
                pseudo = input()
                game.ajouter_joueur(pseudo)

            game.demarer(DATA, nb_espions, white)
        case "b":
            print("""
            - Darkover -
            
            Réalisé par :
            * MAY Baptiste
            * MERLIER Aleksandre
            * LANNOOTE Pierre
            """)
            input("[Fermer]")
        case "c":
            clear()
            break
