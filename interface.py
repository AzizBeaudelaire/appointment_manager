import os, sys
from gestion_rdv import GestionRendezVous

class InterfaceUtilisateur:
    def __init__(self):
        self.gestion_rdv = GestionRendezVous(fichier_db='rendezvous.db')

    def menu_principal(self):
        try:
            self.gestion_rdv.creer_tables()
        except FileNotFoundError as fnfe:
            print("\033[91mErreur : Fichier introuvable - {}\033[0m".format(str(fnfe)))
            sys.exit(1)
        except Exception as e:
            print("\033[91mErreur lors de l'exécution du programme : {}\033[0m".format(str(e)))
            sys.exit(1)

        while True:
            os.system('clear')  # Utilisez 'cls' au lieu de 'clear' si vous êtes sur Windows

            print("\nMenu Principal:")
            print("1. Afficher la liste de RDV")
            print("2. Ajouter un RDV")
            print("3. Modifier un RDV")
            print("4. Supprimer un RDV")
            print("5. Quitter")

            choix = input("Choisissez une option (1-5): ")

            if choix == '1':
                date_jour = input("Entrez la date pour afficher les RDV (format YYYY-MM-DD): ")
                self.gestion_rdv.lister_rendezvous(date_jour)
                # self.gestion_rdv.lister_rendezvous()
            elif choix == '2':
                self.menu_ajouter_rdv()
            elif choix == '3':
                self.menu_modifier_rdv()
            elif choix == '4':
                self.menu_supprimer_rdv()
            elif choix == '5':
                print("Au revoir!")
                break
            else:
                print("Option invalide. Veuillez choisir une option valide.")

    def menu_ajouter_rdv(self):
        nom_patient = input("Entrez le nom du patient: ")
        prenom_patient = input("Entrez le prénom du patient: ")
        date_naissance_patient = input("Entrez la date de naissance du patient (format YYYY-MM-DD): ")
        adresse_patient = input("Entrez l'adresse du patient: ")
        numero_telephone_patient = input("Entrez le numéro de téléphone du patient: ")
        medecin = input("Entrez le nom du médecin: ")
        date_rdv = input("Entrez la date du rendez-vous (format YYYY-MM-DD): ")
        heure_rdv = input("Entrez l'heure du rendez-vous (format HH:MM): ")
        nom_secretaire = input("Entrez le nom de la secrétaire: ")

        self.gestion_rdv.prendre_rdv(
            nom_patient, prenom_patient, date_naissance_patient, adresse_patient, numero_telephone_patient,
            medecin, date_rdv, heure_rdv, nom_secretaire
        )

    def menu_modifier_rdv(self):
        nom_patient = input("Entrez le nom du patient: ")
        prenom_patient = input("Entrez le prénom du patient: ")
        date_rdv = input("Entrez la date du rendez-vous à modifier (format YYYY-MM-DD): ")
        heure_rdv = input("Entrez l'heure du rendez-vous à modifier (format HH:MM): ")
        nouvelle_date = input("Entrez la nouvelle date du rendez-vous (format YYYY-MM-DD): ")
        nouvelle_heure = input("Entrez la nouvelle heure du rendez-vous (format HH:MM): ")

        self.gestion_rdv.modifier_rendezvous(nom_patient, prenom_patient, date_rdv, heure_rdv, nouvelle_date, nouvelle_heure)

    def menu_supprimer_rdv(self):
        nom_patient = input("Entrez le nom du patient: ")
        prenom_patient = input("Entrez le prénom du patient: ")
        date_rdv = input("Entrez la date du rendez-vous à supprimer (format YYYY-MM-DD): ")
        heure_rdv = input("Entrez l'heure du rendez-vous à supprimer (format HH:MM): ")

        self.gestion_rdv.supprimer_rendezvous(nom_patient, prenom_patient, date_rdv, heure_rdv)

