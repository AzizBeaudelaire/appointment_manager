-- Création de la table Patient
CREATE TABLE Patient (
    ID_patient INTEGER PRIMARY KEY,
    Nom TEXT,
    Prenom TEXT,
    DateNaissance DATE,
    Adresse TEXT,
    NumeroTelephone TEXT
    -- Ajoutez d'autres colonnes pour les détails du patient si nécessaire
);

-- Création de la table Medecin
CREATE TABLE Medecin (
    ID_medecin INTEGER PRIMARY KEY,
    Nom TEXT,
    Prenom TEXT
    -- Ajoutez d'autres colonnes pour les détails du médecin si nécessaire
);

-- Création de la table Secretaire
CREATE TABLE Secretaire (
    ID_secretaire INTEGER PRIMARY KEY,
    Nom TEXT,
    Prenom TEXT
    -- Ajoutez d'autres colonnes pour les détails de la secrétaire si nécessaire
);

-- Création de la table CreneauHoraire
CREATE TABLE CreneauHoraire (
    ID_creneau INTEGER PRIMARY KEY,
    DebutCreneau TIME,
    FinCreneau TIME
    -- Ajoutez d'autres colonnes pour des données supplémentaires si nécessaire
);

-- Création de la table RendezVous
CREATE TABLE RendezVous (
    ID_rendezvous INTEGER PRIMARY KEY,
    DateRendezVous DATE,
    HeureRendezVous TIME,
    ID_patient INTEGER,
    ID_medecin INTEGER,
    ID_secretaire INTEGER,
    ID_creneau INTEGER,
    -- Ajoutez d'autres colonnes pour des données supplémentaires si nécessaire
    FOREIGN KEY (ID_patient) REFERENCES Patient(ID_patient),
    FOREIGN KEY (ID_medecin) REFERENCES Medecin(ID_medecin),
    FOREIGN KEY (ID_secretaire) REFERENCES Secretaire(ID_secretaire),
    FOREIGN KEY (ID_creneau) REFERENCES CreneauHoraire(ID_creneau)
);

-- Fin du script
