import random


# UTILS

def bool_aleatoire() -> bool:
    """
    Renvoie vrai ou faux aléatoirement
    """
    return random.randint(0, 1) == 0


def lecture_csv(separe: str, fichier: str) -> list:
    """
    importe le fichier csv, charge son contenu dans un tableau
    :param separe: Le sépérateur
    :param fichier: nom du fichier csv à traiter
    :return: tableau, liste de listes contenant toutes les informations du fichier
    """
    fichier = open(fichier, "r")
    table = [ligne.rstrip().split(separe) for ligne in fichier]
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

    def __init__(self, separe: str, file_name: str):
        data = lecture_csv(separe, file_name)
        self.data = []
        for mots in data:
            self.data.append(Pair(mots[0], mots[1]))

    def pair_aleatoire(self) -> Pair:
        """
        Renvoie une pair de deux mots aléatoirement
        """
        index = random.randint(0, len(self.data) - 1)
        return self.data[index]


class Joueur:
    """
    Un joueur
    """

    def __init__(self, nom):
        self.uuid = random.getrandbits(8)
        self.nom = nom
        self.role = None
        self.mot = None


class Mots:
    """
    Une liste de mots proposés par les joueurs
    """

    def __init__(self):
        self.donnee = {}

    def mot_existant(self, mot: str) -> bool:
        """
        Vérifie si un mot a déjà était dit
        """
        s = False
        for p in self.donnee.values():
            for m in p:
                if m == mot:
                    s = True
        return s

    def personnel(self, uuid: int) -> Joueur:
        """
        Renvoie le joueur correspondant à l'id
        :param uuid: L'id du joueur
        :return: Le joueur
        """
        return self.donnee[uuid]

    def ajouter_mot(self, uuid: int, mot: str):
        """
        Ajoute un mot dans les mots proposés
        :param uuid: L'id du joueur
        :param mot: Le mot proposé
        """
        if uuid not in self.donnee.keys():
            self.donnee[uuid] = []
        self.donnee[uuid].append(mot)

    def mots_joueur(self, uuid: int) -> list:
        """
        Renvoie les mots proposés par un joueur
        :param uuid: L'id du joueur
        :return: La liste de tous les mots proposés
        """
        return self.donnee[uuid]


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

    def demarrer(self, data: ListeMots, nb_espions: int, white: bool):
        """
        Démarre la partie
        :param data: La liste des mots
        :param nb_espions: Le nombre d'espions dans la partie
        :param white: Si un mister white est présent dans la partie
        """

        # SETUP
        self.pair = data.pair_aleatoire()

        self.compo["Mister White"] = 1 if white else 0
        self.compo["Espion"] = nb_espions
        self.compo["Civil"] = self.nb_joueurs - self.compo["Espion"] - self.compo["Mister White"]

        temp_compo = []
        for role, nb in self.compo.items():
            for _ in range(int(nb)):
                temp_compo.append(role)
        random.shuffle(temp_compo)

        self.vrai_mot = self.pair.mot1 if bool_aleatoire() else self.pair.mot2

        # DISTRIBUTION DES MOTS (ET ROLE)
        for i in range(len(self.joueurs)):
            clear()
            joueur = self.joueurs[i]
            joueur.role = temp_compo[i]
            input("{}, appuis sur [Entrer] pour voir ton mot".format(joueur.nom))
            if joueur.role == "Mister White":
                mot = "Tu es Mister White"
            elif joueur.role == "Civil":
                mot = self.vrai_mot
            else:
                mot = self.pair.inverse(self.vrai_mot)
            print("Ton mot est :", mot)
            input("[Suivant]")

        clear()

        manche = 0

        # LOOP GAME
        end = 0
        while end == 0:

            manche += 1

            random.shuffle(self.joueurs)
            while self.joueurs[0].role == "Mister White":
                random.shuffle(self.joueurs)

            # DEMANDE MOT
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

            # AFFICHAGE DES MOTS
            message = "\n- Manche {} -\n\nVoici les mots dits :\n".format(manche)

            for joueur in self.joueurs:
                message += "* " + joueur.nom + ": "
                for mot in self.mots.mots_joueur(joueur.uuid):
                    message += mot + ", "
                message = message[:-2]
                message += "\n"

            print(message)
            input("\n" + "[Passer au vote]")

            # VOTES
            clear()
            while True:
                message = "Choisis quelqu'un à éliminé parmis :\n"
                for i in range(len(self.joueurs)):
                    message += "{} - {}\n".format(i + 1, self.joueurs[i].nom)
                message += "\n"

                print(message)
                vote = input()
                try:
                    vote = int(vote)
                    assert len(self.joueurs) >= vote >= 1
                    vote -= 1
                    break
                except ValueError:
                    print()
                except AssertionError:
                    print("Ce joueur n'existe pas")

            # ELIMINATION
            clear()
            tue = self.joueurs[vote]
            print("{} a été éliminé ! Il était : {}".format(tue.nom, tue.role))
            if tue.role == "Mister White":
                while True:
                    print("{}, propose un mot".format(tue.nom))
                    mot_white = input()
                    if mot_white.lower() == self.vrai_mot.lower():
                        end = 3
                    break
                white = False
            elif tue.role == "Espion":
                nb_espions -= 1
            self.joueurs.pop(vote)
            input("[Suivant]")

            # CONDITION D'ARRET
            if nb_espions == 0:
                if not white:
                    end = 1
            if nb_espions + (1 if white else 0) >= round(len(self.joueurs) * (1 / 2)):
                end = 2

        # PHRASE DE FIN
        if end == 1:
            print("Les civils ont gagné !")
        elif end == 2:
            print("Les espions ont gagné !")
        else:
            print("Mister White a gagné !")
        print()
        print("Le mot des civils était " + self.pair.inverse(self.vrai_mot))
        print("Le mot des espions était " + self.vrai_mot)
        input()


# VARIABLES

DATA = ListeMots(",", "data.csv")

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

            # NOMBRE DE JOUEURS
            while True:
                print("Entrez le nombre de joueurs")
                nb_joueurs = input()
                try:
                    nb_joueurs = int(nb_joueurs)
                    assert 3 <= nb_joueurs <= 9, "NoAmontPlayer"
                    break
                except ValueError:
                    print()
                except AssertionError:
                    if nb_joueurs < 4:
                        print("Il faut au moins 4 joueurs pour commencer une partie")
                    elif nb_joueurs > 9:
                        print("Il peut y avoir au maximum 9 joueurs")

            # AJOUT D'UN MISTER WHITE
            if nb_joueurs != 3:
                while True:
                    print("Veux-tu un Mister White ? (O/N)")
                    white = input().lower()
                    if "o" in white:
                        white = True
                        break
                    elif "n" in white:
                        white = False
                        break
            else:
                white = False

            # CALCUL NOMBRE D'ESPIONS
            max_espions = round(nb_joueurs * (1 / 3))
            nb_espions = 0
            if max_espions == (2 if white else 1):
                nb_espions = 1
            else:
                min_espions = 0 if nb_espions == 1 else 1
                if min_espions == max_espions:
                    nb_espions = min_espions
                else:
                    while True:
                        print("Entrez le nombre d'espions (entre {} et {})".format(min_espions, max_espions))
                        nb_espions = input()
                        try:
                            nb_espions = int(nb_espions)
                            assert min_espions <= nb_espions <= max_espions
                            break
                        except ValueError:
                            print()
                        except AssertionError:
                            print("")

            # ENTREE DES NOMS DES JOUEURS
            for i in range(nb_joueurs):
                print("Joueur {}, veuillez entrer votre pseudo".format(i + 1))
                pseudo = input()
                game.ajouter_joueur(pseudo)

            # DEMARRE LA PARTIE
            game.demarrer(DATA, nb_espions, white)
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
