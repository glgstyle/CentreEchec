# CentreEchec
CentreEchec est un programme qui permet de gérer des tournois d échecs hebdomadaires. 

# Installation :

---

1. Placez-vous dans le répertoire qui contiendra le projet 
  
2. Récupérer le code venant de GitHub (faire un clone) :  
```
git clone https://github.com/glgstyle/CentreEchec.git
cd CentreEchec
```
3. Créer un environnement virtuel : 

```python -m venv env```

4. Activer l'environnement :  

```source env/bin/activate ```

5. Installer les packages :

```pip install -r requirements.txt```  
```pip freeze``` (pour vérifier que les packages se sont bien installés)

# Utilisation

---

Pour démarrer le programme, exécutez simplement la commande suivante:
```python main.py```
Pour valider chaque commande dans le terminal appuyez sur la touche  entrée 

## Menu Tournoi

Pour accéder au menu tournoi, depuis le menu principal, sélectionnez l'option 1

### Création d'un nouveau tournoi 

1. Sélectionnez l'option 1
2. Saisir le nom du tournoi
3. Saisir la date
4. Saisir le lieu du tournoi
5. Saisir le commentaire
6. Saisir le controle du temps
7. Saisir le nombre de tours

#### Si ajout de nouveaux joueurs dans le tournoi

1. Sélectionnez l'option 1 
2. Saisir le nom du joueur
3. Saisir le prénom du joueur
4. Saisir la date de naissance du joueur
5. Saisir le sexe du joueur(F/M)
6. Saisir le classement du joueur
7. Répétez les opérations 1 à 10 jusqu'à l'obtention du nombre de joueurs
8. Le tournoi et les joueurs se sont enregistrés en base de données

#### Si sélection de joueurs depuis la base de données

1. Sélectionnez l'option 2
2. La liste des joueurs existants s'affiche
3. Sélectionnez les joueur

##### Pour commencer le tournoi 
1. Saisir O pour oui sinon N pour ne pas continuer
2. Appuyez sur entrée
3. Le numéro du round s'affiche ainsi que les paires de joueurs
4. Appuyez sur entrée pour commencer le match
5. L'heure de démarrage du match s'affiche 
6. Appuyez sur entrée lorsque le match est terminée
7. L'heure de fin du match s'affiche
8. Le numro du match s'affiche
9. Saisir le score de chaque joueur dans chacun des matchs
10. Une mise à jour des scores des joueurs s'affiche
11. Un tableau récapitulatif du round s'affiche également
12. Répétez les opérations 3 à 9 jusqu'à la fin du tournoi

### Reprendre un tournoi 

1. Sélectionnez l'option 2
2. Une liste des tournoi enregistrés s'affiche
3. Sélectionnez le tournoi souhaité
4. Si le tournoi n'est pas terminé il reprend au round arrêté,
   sinon un récapitulatif s'affiche

## Menu Joueurs

Pour accéder au menu des joueurs, depuis le menu principal, sélectionnez l'option 2

### Ajouter un nouveau joueur

1. Sélectionnez l'option 1
2. Saisir le nom du joueur
3. Saisir le prénom du joueur
4. Saisir la date de naissance du joueur
5. Saisir le sexe du joueur(F/M)
6. Saisir le classement du joueur
7. Si vous souhaitez ajouter un autre joueur, sélectionnez O sinon N

### Ajouter une équipe de joueurs

1. Sélectionnez l'option 2
2. Saisir le nom du joueur
3. Saisir le prénom du joueur
4. Saisir la date de naissance du joueur
5. Saisir le sexe du joueur(F/M)
6. Saisir le classement du joueur
7. Répetez les opérations 2 à 6 jusqu'à ce que l'équipe soit complète

### Modifier le rang d'un joueur

1. Sélectionnez l'option 3
2. La liste des joueurs s'affiche
3. Sélectionnez le joueur concerné (pas son rang)
4. Saisir le nouveau rang

### Voir la liste des joueurs

1. Sélectionnez l'option 4
2. La liste des joueurs s'affiche

## Menu Rapports

Pour accéder au menu des rapports, depuis le menu principal, sélectionnez l'option 3

### Lister tous les joueurs par ordre alphabétique

1. Sélectionnez l'option 1
2. La liste des joueurs s'affiche

### Lister tous les joueurs par classement

1. Sélectionnez l'option 2
2. La liste des joueurs s'affiche 

### Lister tous les joueurs d'un tournoi par ordre alphabétique

1. Sélectionnez l'option 3
2. Sélectionnez le numéro du tournoi concerné
3. La liste des joueurs s'affiche 

### Lister tous les joueurs d'un tournoi par classement

1. Sélectionnez l'option 4
2. Sélectionnez le numéro du tournoi concerné
3. La liste des joueurs s'affiche 

### Lister tous les joueurs de tous les tournois

1. Sélectionnez l'option 5
2. La liste des joueurs s'affiche 

### Lister tous les tours d'un tournoi

1. Sélectionnez l'option 6
2. Sélectionnez le numéro du tournoi concerné
3. La liste des rounds s'affiche 

### Lister tous les matchs d'un tournoi

1. Sélectionnez l'option 7
2. Sélectionnez le numéro du tournoi concerné
3. La liste des rounds s'affiche 










