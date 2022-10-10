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


class Mots:
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
        self.nom = nom
        self.role = None
        self.mot = None


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
            print("\n" * 100)
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

        print("\n" * 100)
        print("La partie peut commencer !")
        input()


DATA = Mots("data.csv")

while True:
    print("\n" * 100)
    print("""
    [A] Jouer
    [B] Options
    [C] A propos
    [D] Quitter
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
            input("WIP")
        case "c":
            print("""
            - Darkover -
            
            Réalisé par :
            * MAY Baptiste
            * MERLIER Aleksandre
            * LANNOOTE Pierre
            """)
            input("[Fermer]")
        case "d":
            print("\n" * 100)
            break
