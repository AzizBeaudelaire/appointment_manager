import sqlite3
from datetime import datetime, timedelta

class GestionRendezVous:
    def __init__(self, fichier_db='rendezvous.db'):
        self.fichier_db = fichier_db

    def __enter__(self):
        self.conn = sqlite3.connect(self.fichier_db)
        self.c = self.conn.cursor()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.conn.close()

    def creer_tables(self):
        with self.conn:
            self.c.execute('''
                CREATE TABLE IF NOT EXISTS Patient (
                    ID_patient INTEGER PRIMARY KEY,
                    Nom TEXT,
                    Prenom TEXT,
                    DateNaissance DATE,
                    Adresse TEXT,
                    NumeroTelephone TEXT
                )
            ''')
            self.c.execute('''
                CREATE TABLE IF NOT EXISTS RendezVous (
                    ID_rendezvous INTEGER PRIMARY KEY,
                    DateRendezVous DATE,
                    HeureRendezVous TIME,
                    ID_patient INTEGER,
                    Medecin TEXT,
                    Secretaire TEXT,
                    FOREIGN KEY (ID_patient) REFERENCES Patient(ID_patient)
                )
            ''')

    def prendre_rdv(self, nom_patient, prenom_patient, date_naissance_patient, adresse_patient,
                    numero_telephone_patient, medecin, date_rdv, heure_rdv, nom_secretaire):
        with self.conn:
            heure_rdv_datetime = datetime.strptime(heure_rdv, "%H:%M")

            # Vérifier que l'heure est entre 8h et 20h
            if heure_rdv_datetime < datetime.strptime("08:00", "%H:%M") or heure_rdv_datetime >= datetime.strptime("20:00", "%H:%M"):
                print("Vous ne pouvez prendre de rendez-vous qu'entre 8h et 20h.")
                return

            # Créer le patient s'il n'existe pas
            self.c.execute('''
                INSERT OR IGNORE INTO Patient (Nom, Prenom, DateNaissance, Adresse, NumeroTelephone)
                VALUES (?, ?, ?, ?, ?)
            ''', (nom_patient, prenom_patient, date_naissance_patient, adresse_patient, numero_telephone_patient))

            # Récupérer l'ID du patient
            self.c.execute('''
                SELECT ID_patient FROM Patient
                WHERE Nom = ? AND Prenom = ?
            ''', (nom_patient, prenom_patient))
            patient_id = self.c.fetchone()[0]

            # Créer le rendez-vous
            debut_rdv = datetime.strptime(f"{date_rdv} {heure_rdv}", "%Y-%m-%d %H:%M")
            fin_rdv = debut_rdv + timedelta(minutes=30)

            # Vérifier si le créneau est disponible
            if self.creneau_disponible(debut_rdv, fin_rdv):
                self.c.execute('''
                    INSERT INTO RendezVous (DateRendezVous, HeureRendezVous, ID_patient, Medecin, Secretaire)
                    VALUES (?, ?, ?, ?, ?)
                ''', (date_rdv, heure_rdv, patient_id, medecin, nom_secretaire))

                print("Rendez-vous enregistré avec succès.")
            else:
                print("Créneau non disponible. Choisissez un autre créneau.")

    # ... (autres méthodes)

    def modifier_rendezvous(self, id_rendezvous, nouvelle_date, nouvelle_heure):
        with self.conn:
            # Vérifier que l'heure est entre 8h et 20h
            heure_rdv_datetime = datetime.strptime(nouvelle_heure, "%H:%M")
            if heure_rdv_datetime < datetime.strptime("08:00", "%H:%M") or heure_rdv_datetime >= datetime.strptime("20:00", "%H:%M"):
                print("Vous ne pouvez modifier de rendez-vous qu'entre 8h et 20h.")
                return

            # Vérifier si le nouveau créneau est disponible
            debut_rdv = datetime.strptime(f"{nouvelle_date} {nouvelle_heure}", "%Y-%m-%d %H:%M")
            fin_rdv = debut_rdv + timedelta(minutes=30)

            if self.creneau_disponible(debut_rdv, fin_rdv):
                self.c.execute('''
                    UPDATE RendezVous
                    SET DateRendezVous = ?, HeureRendezVous = ?
                    WHERE ID_rendezvous = ?
                ''', (nouvelle_date, nouvelle_heure, id_rendezvous))

                print("Rendez-vous modifié avec succès.")
            else:
                print("Créneau non disponible. Choisissez un autre créneau.")

    def lister_rendezvous(self, date_jour):
        self.c.execute('''
            SELECT R.ID_rendezvous, R.DateRendezVous, R.HeureRendezVous, P.Nom, P.Prenom, R.Medecin, R.Secretaire
            FROM RendezVous R
            JOIN Patient P ON R.ID_patient = P.ID_patient
            WHERE R.DateRendezVous = ?
        ''', (date_jour,))

        rendezvous = self.c.fetchall()

        if not rendezvous:
            print(f"Aucun rendez-vous prévu pour le {date_jour}.")
        else:
            for rdv in rendezvous:
                id_rendezvous, date_rdv, heure_rdv, nom_patient, prenom_patient, medecin, nom_secretaire = rdv
                debut_rdv = datetime.strptime(f"{date_rdv} {heure_rdv}", "%Y-%m-%d %H:%M")
                fin_rdv = debut_rdv + timedelta(minutes=30)

                print(
                    f"ID: {id_rendezvous}, Date: {date_rdv}, Heure: {heure_rdv}-{fin_rdv.strftime('%H:%M')}, Patient: {nom_patient} {prenom_patient}, Médecin: {medecin}, Secrétaire: {nom_secretaire}")

    def supprimer_rendezvous(self, id_rendezvous):
        with self.conn:
            # Récupérer les informations du rendez-vous avant la suppression
            self.c.execute('''
                SELECT DateRendezVous, HeureRendezVous
                FROM RendezVous
                WHERE ID_rendezvous = ?
            ''', (id_rendezvous,))
            rdv_info = self.c.fetchone()

            if rdv_info:
                date_rdv, heure_rdv = rdv_info
                debut_rdv = datetime.strptime(f"{date_rdv} {heure_rdv}", "%Y-%m-%d %H:%M")
                fin_rdv = debut_rdv + timedelta(minutes=30)

                # Supprimer le rendez-vous
                self.c.execute('''
                    DELETE FROM RendezVous
                    WHERE ID_rendezvous = ?
                ''', (id_rendezvous,))

                print("Rendez-vous supprimé avec succès.")
            else:
                print("Rendez-vous introuvable.")
