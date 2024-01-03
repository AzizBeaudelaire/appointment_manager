import sqlite3

class GestionSecretaire:
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
                CREATE TABLE IF NOT EXISTS Secretaire (
                    ID_secretaire INTEGER PRIMARY KEY,
                    Nom TEXT,
                    Prenom TEXT
                )
            ''')

    def ajouter_secretaire(self, prenom, nom):
        with self.conn:
            self.c.execute('''
                INSERT INTO Secretaire (Nom, Prenom)
                VALUES (?, ?)
            ''', (nom, prenom))

            print("Secrétaire ajoutée avec succès.")

    def lister_secretaires(self):
        self.c.execute('''
            SELECT ID_secretaire, Nom, Prenom
            FROM Secretaire
            ORDER BY Nom, Prenom
        ''')
        secretaires = self.c.fetchall()

        if not secretaires:
            print("Aucune secrétaire enregistrée.")
        else:
            for secretaire in secretaires:
                id_secretaire, nom, prenom = secretaire
                print(f"ID: {id_secretaire}, Nom: {nom}, Prénom: {prenom}")

    def supprimer_secretaire(self, id_secretaire):
        with self.conn:
            self.c.execute('''
                DELETE FROM Secretaire
                WHERE ID_secretaire = ?
            ''', (id_secretaire,))

            print("Secrétaire supprimée avec succès.")
