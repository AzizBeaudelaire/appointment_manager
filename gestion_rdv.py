import sqlite3
from datetime import datetime

class GestionRendezVous:
    def __init__(self, fichier_db='rendezvous.db'):
        self.conn = sqlite3.connect(fichier_db)
        self.c = self.conn.cursor()

    def creer_tables(self):
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
        self.conn.commit()

    def prendre_rdv(self, nom_patient, prenom_patient, date_naissance_patient, adresse_patient, numero_telephone_patient, medecin, date_rdv, heure_rdv, nom_secretaire):
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
        self.c.execute('''
            INSERT INTO RendezVous (DateRendezVous, HeureRendezVous, ID_patient, Medecin, Secretaire)
            VALUES (?, ?, ?, ?, ?)
        ''', (date_rdv, heure_rdv, patient_id, medecin, nom_secretaire))

        self.conn.commit()

    def lister_rendezvous(self):
        self.c.execute('''
            SELECT R.ID_rendezvous, R.DateRendezVous, R.HeureRendezVous, P.Nom, P.Prenom, R.Medecin, R.Secretaire
            FROM RendezVous R
            JOIN Patient P ON R.ID_patient = P.ID_patient
        ''')
        rendezvous = self.c.fetchall()
        for rdv in rendezvous:
            print(f"ID: {rdv[0]}, Date: {rdv[1]}, Heure: {rdv[2]}, Patient: {rdv[3]} {rdv[4]}, Médecin: {rdv[5]}, Secrétaire: {rdv[6]}")

    def modifier_rendezvous(self, id_rendezvous, nouvelle_date):
        self.c.execute('''
            UPDATE RendezVous
            SET DateRendezVous = ?
            WHERE ID_rendezvous = ?
        ''', (nouvelle_date, id_rendezvous))

        self.conn.commit()

    def supprimer_rendezvous(self, id_rendezvous):
        self.c.execute('''
            DELETE FROM RendezVous
            WHERE ID_rendezvous = ?
        ''', (id_rendezvous,))

        self.conn.commit()
