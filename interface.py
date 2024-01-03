import os
import sys
from gestion_medecin import GestionMedecin
from gestion_rdv import GestionRendezVous

class InterfaceUtilisateur:
    def __init__(self):
        self.gestion_rdv = GestionRendezVous(fichier_db='rendezvous.db')
        self.gestion_medecin = GestionMedecin(fichier_db='medecins.db')

    def menu_principal(self):
        try:
            self.gestion_rdv.creer_tables()
            self.gestion_medecin.creer_tables()
        except FileNotFoundError as fnfe:
            print("\033[91mErreur : Fichier introuvable - {}\033[0m".format(str(fnfe)))
            sys.exit(1)
        except Exception as e:
            print("\033[91mErreur lors de l'exécution du programme : {}\033[0m".format(str(e)))
            sys.exit(1)

        while True:
            os.system('clear')  # Utilisez 'cls' au lieu de 'clear' si vous êtes sur Windows

            print("\nMenu Principal:")
            print("1. Gestion des RDV")
            print("2. Gestion des Médecins")
            print("3. Quitter")

            choix = input("Choisissez une option (1-3): ")

            if choix == '1':
                self.menu_gestion_rdv()
            elif choix == '2':
                self.menu_gestion_medecins()
            elif choix == '3':
                print("Au revoir!")
                break
            else:
                print("Option invalide. Veuillez choisir une option valide.")

    def menu_gestion_rdv(self):
        while True:
            os.system('clear')  # Retiré pour ne pas effacer le terminal pendant l'affichage des réponses

            print("\nGestion des RDV:")
            print("1. Afficher la liste de RDV")
            print("2. Ajouter un RDV")
            print("3. Modifier un RDV")
            print("4. Supprimer un RDV")
            print("5. Retour au menu principal")

            choix_rdv = input("Choisissez une option (1-5): ")

            if choix_rdv == '1':
                self.gestion_rdv.lister_rendezvous()
            elif choix_rdv == '2':
                self.menu_ajouter_rdv()
            elif choix_rdv == '3':
                self.menu_modifier_rdv()
            elif choix_rdv == '4':
                self.menu_supprimer_rdv()
            elif choix_rdv == '5':
                break
            else:
                print("Option invalide. Veuillez choisir une option valide.")

    def menu_gestion_medecins(self):
        while True:
            os.system('clear')  # Retiré pour ne pas effacer le terminal pendant l'affichage des réponses

            print("\nGestion de Médecins:")
            print("1. Ajouter un médecin")
            print("2. Supprimer un médecin")
            print("3. Lister les médecins")
            print("4. Afficher le planning d'un médecin")
            print("5. Retour au menu principal")

            choix_medecin = input("Choisissez une option (1-5): ")

            if choix_medecin == '1':
                self.menu_ajouter_medecin()
            elif choix_medecin == '2':
                self.menu_supprimer_medecin()
            elif choix_medecin == '3':
                self.gestion_medecin.lister_medecins()
            elif choix_medecin == '4':
                self.menu_afficher_planning()
            elif choix_medecin == '5':
                break
            else:
                print("Option invalide. Veuillez choisir une option valide.")

    def menu_ajouter_medecin(self):
        prenom_medecin = input("Entrez le prénom du médecin: ")
        nom_medecin = input("Entrez le nom du médecin: ")

        self.gestion_medecin.ajouter_medecin(prenom_medecin, nom_medecin)

    def menu_supprimer_medecin(self):
        id_medecin = input("Entrez l'ID du médecin à supprimer: ")

        self.gestion_medecin.supprimer_medecin(id_medecin)

    def menu_afficher_planning(self):
        id_medecin = input("Entrez l'ID du médecin pour afficher le planning: ")
        self.gestion_medecin.afficher_planning_semaine(id_medecin)

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
