-- Ce script SQL crée la base de données pour le gestionnaire de rendez-vous

-- Création de la table Patient
CREATE TABLE Patient (
    ID_patient INT PRIMARY KEY,
    Nom VARCHAR(255),
    Prenom VARCHAR(255),
    DateNaissance DATE,
    Adresse VARCHAR(255),
    NumeroTelephone VARCHAR(20)
    -- Ajoutez d'autres colonnes pour les détails du patient si nécessaire
);

-- Création de la table Medecin
CREATE TABLE Medecin (
    ID_medecin INT PRIMARY KEY,
    Nom VARCHAR(255),
    Prenom VARCHAR(255)
    -- Ajoutez d'autres colonnes pour les détails du médecin si nécessaire
);

-- Création de la table Secretaire
CREATE TABLE Secretaire (
    ID_secretaire INT PRIMARY KEY,
    Nom VARCHAR(255),
    Prenom VARCHAR(255)
    -- Ajoutez d'autres colonnes pour les détails de la secrétaire si nécessaire
);

-- Création de la table RendezVous
CREATE TABLE RendezVous (
    ID_rendezvous INT PRIMARY KEY,
    DateRendezVous DATE,
    HeureRendezVous TIME,
    ID_patient INT,
    ID_medecin INT,
    ID_secretaire INT,
    -- Ajoutez d'autres colonnes pour des données supplémentaires si nécessaire
    FOREIGN KEY (ID_patient) REFERENCES Patient(ID_patient),
    FOREIGN KEY (ID_medecin) REFERENCES Medecin(ID_medecin),
    FOREIGN KEY (ID_secretaire) REFERENCES Secretaire(ID_secretaire)
);

-- Fin du script
