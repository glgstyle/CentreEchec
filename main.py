'''Entry point'''

from controllers.base import Controller


def mainMenu():
    print("----------------------------")
    print("Sélectionnez une option")
    print("1 - Tournois")
    print("2 - Joueurs")
    print("3 - Rapports")
    print("----------------------------")
    while True:
        try :
            option = input("Veuillez saisir votre choix :")
            if option == "1":
                tournament_submenu()
                break
            elif option == "2":
                joueurs_submenu()
                break
            elif option == "3":
                rapports_submenu()
                break
        except : 
            print("Cette entrée n'est pas valide")
            

def tournament_submenu():

    print("----------------------------")
    print("Sélectionnez une option")
    print("1 - Créer un nouveau tournoi")
    print("2 - Voir un tournoi existant")
    print("3 - >> Retour")
    print("----------------------------")

def joueurs_submenu():
    print("----------------------------")
    print("Sélectionnez une option")
    print("1 - Ajouter un nouveau joueur")
    print("2 - Voir la liste des joueurs")
    print("3 - >> Retour")
    print("----------------------------")

def rapports_submenu():
    print("----------------------------")
    print("Sélectionnez une option")
    print("1 - Liste de tous les joueurs par ordre alphabétique")
    print("2 - Liste de tous les joueurs par classement")
    print("3 - Liste de tous les joueurs d'un tournoi par ordre alphabétique")
    print("4 - Liste de tous les joueurs d'un tournoi par classement")
    print("5 - Liste de tous les joueurs de tous les tournois")
    print("6 - Liste de tous les tours d'un tournoi")
    print("7 - Liste de tous les matchs d'un tournoi")
    print("3 - >> Retour")
    print("----------------------------")

def main():
    print(" ____           _              _____     _                   ")
    print("/ ___|___ _ __ | |_ _ __ ___  | ____|___| |__   ___  ___ ___ ")
    print("| |   / _ \ '_ \| __| '__/ _ \ |  _| / __| '_ \ / _ \/ __/ __|")
    print("| |__|  __/ | | | |_| | |  __/ | |__| (__| | | |  __/ (__\__ \"")
    print("\____\___|_| |_|\__|_|  \___| |_____\___|_| |_|\___|\___|___/")
    mainMenu()
    #controller = Controller()
    #controller.start_a_tournament()

if __name__ == "__main__":
    main()



