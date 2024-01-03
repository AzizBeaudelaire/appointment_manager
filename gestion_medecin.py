import sqlite3
from datetime import datetime, timedelta

class GestionMedecin:
    def __init__(self, fichier_db='rendezvous.db'):  # Modifié le nom du fichier_db ici
        self.fichier_db = fichier_db

    def __enter__(self):
        self.conn = sqlite3.connect(self.fichier_db)
        self.c = self.conn.cursor()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.conn.close()

    def creer_tables(self):
        if not hasattr(self, 'conn') or not self.conn:
            self.conn = sqlite3.connect(self.fichier_db)
            self.c = self.conn.cursor()

        with self.conn:
            self.c.execute('''
                CREATE TABLE IF NOT EXISTS Medecin (
                    ID_medecin INTEGER PRIMARY KEY,
                    Nom TEXT,
                    Prenom TEXT
                )
            ''')

    def ajouter_medecin(self, prenom, nom):
        with self.conn:
            self.c.execute('''
                INSERT INTO Medecin (Nom, Prenom)
                VALUES (?, ?)
            ''', (nom, prenom))

            print("Médecin ajouté avec succès.")

    def lister_medecins(self):
        self.c.execute('''
            SELECT ID_medecin, Nom, Prenom
            FROM Medecin
            ORDER BY Nom, Prenom
        ''')
        medecins = self.c.fetchall()

        if not medecins:
            print("Aucun médecin enregistré.")
        else:
            for medecin in medecins:
                id_medecin, nom, prenom = medecin
                print(f"ID: {id_medecin}, Nom: {nom}, Prénom: {prenom}")

    def supprimer_medecin(self, id_medecin):
        with self.conn:
            self.c.execute('''
                DELETE FROM Medecin
                WHERE ID_medecin = ?
            ''', (id_medecin,))

            print("Médecin supprimé avec succès.")

    def afficher_planning_semaine(self, id_medecin):
        # Récupérer le nom et prénom du médecin
        self.c.execute('''
            SELECT Nom, Prenom
            FROM Medecin
            WHERE ID_medecin = ?
        ''', (id_medecin,))
        result = self.c.fetchone()

        if result:
            nom_medecin, prenom_medecin = result
            print(f"Planning de la semaine pour le Dr {prenom_medecin} {nom_medecin} (ID: {id_medecin})\n")

            # Générer les plages horaires de 8h à 20h
            debut_journee = datetime.strptime('08:00', '%H:%M')
            fin_journee = datetime.strptime('20:00', '%H:%M')
            temps_entre_rdv = timedelta(minutes=30)
            plage_horaire = debut_journee

            while plage_horaire <= fin_journee:
                print(f"{plage_horaire.strftime('%H:%M')} - {(plage_horaire + temps_entre_rdv).strftime('%H:%M')}")
                plage_horaire += temps_entre_rdv
        else:
            print(f"Aucun médecin trouvé avec l'ID {id_medecin}.")
