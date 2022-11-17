# Projet n°1 : Darkover

## Explication du projet

Créer un jeu dans le style du jeu [Undercover](https://play.google.com/store/apps/details?id=com.yanstarstudio.joss.undercover&hl=fr&gl=US&pli=1) dans lequel un ou plusieurs espions cachent leurs identitées. Le but est, pour les civils, de démasquer les espions. Pour les aider, les civils ont un mot en commun et les espions ont un même mot similaire aux civils. Chaque tour, chaque joueur entre un mot en rapport avec le sien. A chaque fin de tour, il y a un vote et les joueurs peuvent démasquer les espions.
- `Civils` : Ils ont le même mot et doivent démasquer les différents imposteurs
- `Espions` : Il ne doivent pas se faire remarquer et doivent tenter de survivre en sachant qu'il ne se connaissent pas entre eux.
- `Mr White` : Il n'a pas de mots. Il gagne en réussissant à trouver le mot des civils ou en éliminant tous les civils.

## Carnet de bord

### Jour 1 : Début du projet

- [x] Programme commencé, utilisation d’un `CSV`
- [x] Trouvaille de 86 mots

#### Entre le jour 1 et 2 : Avancement du projet en dehors

> Code du jeu commencé : attribution des cartes aux différents joueurs du jeu, demande d’un Mr. White pour savoir si il entre dans la partie ou non.

### Jour 2 : Continuation du projet

- [x] Création d'un système de vote
- [x] Tableau de 100 mots (50 par colonne) se ressemblant ou ayant un point commun
- [x] Lors du vote, affichaque du role de la personne éliminée
- [ ] Système de vote fonctionnel

### Jour 3 : Projet en cours de finition

- [x] Plusieurs bugs au niveau du choix du nombre d’espions à cause du Mr. White
- [x] Installation d’un nombre maximum de joueur
- [ ] Bugs mineurs à régler
- [ ] Problèmes majeurs : Arrêt du jeu, Vote (vote une personne aléatoire)
- [x] Concentration sur le problème du vote

### Jour 4 : Finalisation du projet

- [x] Fin du programme
- [x] Bug de l’arrêt du jeu
- [x] Bug Mister White doit deviner le mot

### Jour 5 : Projet fini

> Aucun nouveau bug de signaler. Projet terminé.

## Explications des objets python

- `Pair`:
  - Un couple de deux mots (l'un va aux civils et l'autre aux espions)
- `ListeMot`:
  - Une liste de `Pair` de mots, liste implémentée avec un `CSV`
- `Joueur`:
  - Un joueur contenant ses données (son id, son nom, son role et son nom)
- `Mots`:
  - Tous les mots proposés par les joueurs
- `Game`:
  - Une partie contenant toute ses informations (ses joueurs, son nombre de joueurs, la `Pair` de mots, le mot des civils, la composition et les `Mots` proposés)

## Crédits

Réalisé par :
- Lannoote Pierre
- May Baptiste
- Merlier Aleksandre
