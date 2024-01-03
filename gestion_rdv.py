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
        if not hasattr(self, 'conn') or not self.conn:
            self.conn = sqlite3.connect(self.fichier_db)
            self.c = self.conn.cursor()
    
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
                CREATE TABLE IF NOT EXISTS Medecin (
                    ID_medecin INTEGER PRIMARY KEY,
                    Nom TEXT,
                    Prenom TEXT
                )
            ''')
            self.c.execute('''
                CREATE TABLE IF NOT EXISTS Secretaire (
                    ID_secretaire INTEGER PRIMARY KEY,
                    Nom TEXT,
                    Prenom TEXT
                )
            ''')
            self.c.execute('''
                CREATE TABLE IF NOT EXISTS CreneauHoraire (
                    ID_creneau INTEGER PRIMARY KEY,
                    DebutCreneau TIME,
                    FinCreneau TIME
                )
            ''')
            self.c.execute('''
                CREATE TABLE IF NOT EXISTS RendezVous (
                    ID_rendezvous INTEGER PRIMARY KEY,
                    DateRendezVous DATE,
                    HeureRendezVous TIME,
                    ID_patient INTEGER,
                    ID_medecin INTEGER,
                    ID_secretaire INTEGER,
                    ID_creneau INTEGER,
                    FOREIGN KEY (ID_patient) REFERENCES Patient(ID_patient),
                    FOREIGN KEY (ID_medecin) REFERENCES Medecin(ID_medecin),
                    FOREIGN KEY (ID_secretaire) REFERENCES Secretaire(ID_secretaire),
                    FOREIGN KEY (ID_creneau) REFERENCES CreneauHoraire(ID_creneau)
                )
            ''')

    def obtenir_creneaux_disponibles(self):
        with self.conn:
            self.c.execute('SELECT ID_creneau, DebutCreneau, FinCreneau FROM CreneauHoraire')
            return self.c.fetchall()

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
            patient_info = self.c.fetchone()

            if not patient_info:
                print("Patient introuvable.")
                return

            patient_id = patient_info[0]

            # Récupérer l'ID du médecin
            self.c.execute('''
                SELECT ID_medecin FROM Medecin
                WHERE Nom = ?
            ''', (medecin,))
            medecin_info = self.c.fetchone()

            if not medecin_info:
                print("Médecin introuvable.")
                return

            medecin_id = medecin_info[0]

            # Récupérer l'ID de la secrétaire
            self.c.execute('''
                SELECT ID_secretaire FROM Secretaire
                WHERE Nom = ?
            ''', (nom_secretaire,))
            secretaire_info = self.c.fetchone()

            if not secretaire_info:
                print("Secrétaire introuvable.")
                return

            secretaire_id = secretaire_info[0]

            # Récupérer les créneaux horaires disponibles
            creneaux_disponibles = self.obtenir_creneaux_disponibles()

            if not creneaux_disponibles:
                print("Aucun créneau horaire disponible.")
                return

            creneau_disponible = False

            for creneau in creneaux_disponibles:
                creneau_id, debut_creneau, fin_creneau = creneau
                debut_creneau = datetime.strptime(debut_creneau, "%H:%M")
                fin_creneau = datetime.strptime(fin_creneau, "%H:%M")

                if heure_rdv_datetime >= debut_creneau and heure_rdv_datetime < fin_creneau:
                    creneau_disponible = True
                    break

            if creneau_disponible:
                # Insérer le rendez-vous et mettre à jour le créneau horaire
                self.c.execute('''
                    INSERT INTO RendezVous (DateRendezVous, HeureRendezVous, ID_patient, ID_medecin, ID_secretaire, ID_creneau)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', (date_rdv, heure_rdv, patient_id, medecin_id, secretaire_id, creneau_id))

                print("Rendez-vous enregistré avec succès.")
            else:
                print("Créneau non disponible. Choisissez un autre créneau.")

    def lister_rendezvous(self, date_jour):
        self.c.execute('''
            SELECT R.ID_rendezvous, R.DateRendezVous, R.HeureRendezVous, P.Nom, P.Prenom, M.Nom AS Medecin, S.Nom AS Secretaire,
                C.DebutCreneau, C.FinCreneau
            FROM RendezVous R
            JOIN Patient P ON R.ID_patient = P.ID_patient
            JOIN CreneauHoraire C ON R.ID_creneau = C.ID_creneau
            JOIN Medecin M ON R.ID_medecin = M.ID_medecin
            JOIN Secretaire S ON R.ID_secretaire = S.ID_secretaire
            WHERE R.DateRendezVous = ?
        ''', (date_jour,))
        
        rendezvous = self.c.fetchall()

        if not rendezvous:
            print(f"Aucun rendez-vous prévu pour le {date_jour}.")
        else:
            for rdv in rendezvous:
                id_rendezvous, date_rdv, heure_rdv, nom_patient, prenom_patient, medecin, secret_creneau, debut_creneau, fin_creneau = rdv
                debut_rdv = datetime.strptime(f"{date_rdv} {heure_rdv}", "%Y-%m-%d %H:%M")
                fin_rdv = debut_rdv + timedelta(minutes=30)

                print(
                    f"ID: {id_rendezvous}, Date: {date_rdv}, Heure: {heure_rdv}-{fin_rdv.strftime('%H:%M')}, Patient: {nom_patient} {prenom_patient}, Médecin: {medecin}, Secrétaire: {secret_creneau}, Créneau: {debut_creneau}-{fin_creneau}")

    # Modifiez la signature de la méthode modifier_rendezvous
    def modifier_rendezvous(self, nom_patient, prenom_patient, date_rdv, heure_rdv, nouvelle_date, nouvelle_heure):
        with self.conn:
            # Vérifier que l'heure est entre 8h et 20h
            heure_rdv_datetime = datetime.strptime(nouvelle_heure, "%H:%M")
            if heure_rdv_datetime < datetime.strptime("08:00", "%H:%M") or heure_rdv_datetime >= datetime.strptime("20:00", "%H:%M"):
                print("Vous ne pouvez modifier de rendez-vous qu'entre 8h et 20h.")
                return

            # Récupérer l'ID du patient
            self.c.execute('''
                SELECT ID_patient FROM Patient
                WHERE Nom = ? AND Prenom = ?
            ''', (nom_patient, prenom_patient))
            patient_info = self.c.fetchone()

            if not patient_info:
                print("Patient introuvable.")
                return

            patient_id = patient_info[0]

            # Vérifier si le nouveau créneau est disponible
            debut_rdv = datetime.strptime(f"{nouvelle_date} {nouvelle_heure}", "%Y-%m-%d %H:%M")
            fin_rdv = debut_rdv + timedelta(minutes=30)

            if self.creneau_disponible(debut_rdv, fin_rdv):
                # Mettre à jour le rendez-vous
                self.c.execute('''
                    UPDATE RendezVous
                    SET DateRendezVous = ?, HeureRendezVous = ?
                    WHERE ID_patient = ? AND DateRendezVous = ? AND HeureRendezVous = ?
                ''', (nouvelle_date, nouvelle_heure, patient_id, date_rdv, heure_rdv))

                print("Rendez-vous modifié avec succès.")
            else:
                print("Créneau non disponible. Choisissez un autre créneau.")

    # Modifiez la signature de la méthode supprimer_rendezvous
    def supprimer_rendezvous(self, nom_patient, prenom_patient, date_rdv, heure_rdv):
        with self.conn:
            # Récupérer les informations du rendez-vous avant la suppression
            self.c.execute('''
                SELECT ID_rendezvous
                FROM RendezVous
                WHERE ID_patient = (
                    SELECT ID_patient
                    FROM Patient
                    WHERE Nom = ? AND Prenom = ?
                ) AND DateRendezVous = ? AND HeureRendezVous = ?
            ''', (nom_patient, prenom_patient, date_rdv, heure_rdv))

            rendezvous_info = self.c.fetchone()

            if rendezvous_info:
                id_rendezvous = rendezvous_info[0]
                date_rdv, heure_rdv = rendezvous_info

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

    # Ajoutez la méthode creneau_disponible
    def creneau_disponible(self, debut_rdv, fin_rdv):
        with self.conn:
            self.c.execute('''
                SELECT COUNT(*) 
                FROM RendezVous 
                WHERE (strftime('%Y-%m-%d %H:%M', DateRendezVous || ' ' || HeureRendezVous) >= ? AND 
                       strftime('%Y-%m-%d %H:%M', DateRendezVous || ' ' || HeureRendezVous) < ?)
                   OR (strftime('%Y-%m-%d %H:%M', DateRendezVous || ' ' || HeureRendezVous) <= ? AND 
                       strftime('%Y-%m-%d %H:%M', DateRendezVous || ' ' || HeureRendezVous) + '30 minutes' > ?)
            ''', (debut_rdv, debut_rdv, fin_rdv, fin_rdv))

            count = self.c.fetchone()[0]

            return count == 0
