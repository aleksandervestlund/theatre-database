CREATE TABLE IF NOT EXISTS Teaterstykke (
    Navn TEXT NOT NULL,
    Forfatter TEXT NOT NULL,
    Klokkeslett TEXT NOT NULL,
    PRIMARY KEY (Navn)
);

CREATE TABLE IF NOT EXISTS Oppgave (
    TeaterstykkeNavn TEXT NOT NULL,
    Navn TEXT NOT NULL,
    PRIMARY KEY (TeaterstykkeNavn, Navn),
    FOREIGN KEY (TeaterstykkeNavn)
        REFERENCES Teaterstykke (Navn)
            ON DELETE CASCADE
            ON UPDATE NO ACTION
);

CREATE TABLE IF NOT EXISTS Ansatt (
    ID INTEGER NOT NULL,
    Ansattstatus TEXT NOT NULL,
    EPostadresse TEXT,
    Navn NOT NULL,
    TeaterstykkeNavn TEXT NOT NULL,
    OppgaveNavn TEXT NOT NULL,
    PRIMARY KEY (ID),
    FOREIGN KEY (TeaterstykkeNavn, OppgaveNavn)
        REFERENCES Oppgave (TeaterstykkeNavn, Navn)
            ON DELETE CASCADE
            ON UPDATE NO ACTION
);

CREATE TABLE IF NOT EXISTS Akt (
    TeaterstykkeNavn TEXT NOT NULL,
    Nummer INTEGER NOT NULL,
    Navn TEXT,
    PRIMARY KEY (TeaterstykkeNavn, Nummer),
    FOREIGN KEY (TeaterstykkeNavn)
        REFERENCES Teaterstykke (Navn)
            ON DELETE CASCADE
            ON UPDATE NO ACTION
);

CREATE TABLE IF NOT EXISTS Rolle (
    Navn TEXT NOT NULL,
    PRIMARY KEY (Navn)
);

CREATE TABLE IF NOT EXISTS DeltarI (
    RolleNavn TEXT NOT NULL,
    TeaterstykkeNavn TEXT NOT NULL,
    AktNummer INTEGER NOT NULL,
    PRIMARY KEY (RolleNavn, TeaterstykkeNavn, AktNummer),
    FOREIGN KEY (RolleNavn)
        REFERENCES Rolle (Navn)
            ON DELETE CASCADE
            ON UPDATE NO ACTION,
    FOREIGN KEY (TeaterstykkeNavn, AktNummer)
        REFERENCES Akt (TeaterstykkeNavn, Nummer)
            ON DELETE CASCADE
            ON UPDATE NO ACTION
);

CREATE TABLE IF NOT EXISTS Skuespiller (
    ID INTEGER NOT NULL,
    Navn TEXT NOT NULL,
    PRIMARY KEY (ID)
);

CREATE TABLE IF NOT EXISTS SpillerRolle (
    SkuespillerID INTEGER NOT NULL,
    RolleNavn TEXT NOT NULL,
    PRIMARY KEY (SkuespillerID, RolleNavn),
    FOREIGN KEY (SkuespillerID)
        REFERENCES Skuespiller (ID)
            ON DELETE CASCADE
            ON UPDATE NO ACTION,
    FOREIGN KEY (RolleNavn)
        REFERENCES Rolle (Navn)
            ON DELETE CASCADE
            ON UPDATE NO ACTION
);

CREATE TABLE IF NOT EXISTS Dato (
    Måned INTEGER NOT NULL,
    Dag INTEGER NOT NULL,
    PRIMARY KEY (Måned, Dag)
);

CREATE TABLE IF NOT EXISTS Sal (
    Navn TEXT NOT NULL,
    PRIMARY KEY (Navn)
);

CREATE TABLE IF NOT EXISTS Stol (
    SalNavn TEXT NOT NULL,
    Nummer INTEGER NOT NULL,
    RadNummer INTEGER NOT NULL,
    Område TEXT NOT NULL,
    PRIMARY KEY (SalNavn, Nummer, RadNummer, Område),
    FOREIGN KEY (SalNavn)
        REFERENCES Sal (Navn)
            ON DELETE CASCADE
            ON UPDATE NO ACTION
);

CREATE TABLE IF NOT EXISTS Forestilling (
    TeaterstykkeNavn TEXT NOT NULL,
    SalNavn TEXT NOT NULL,
    MånedVises INTEGER NOT NULL,
    DagVises INTEGER NOT NULL,
    PRIMARY KEY (TeaterstykkeNavn, SalNavn, MånedVises, DagVises),
    FOREIGN KEY (TeaterstykkeNavn)
        REFERENCES Teaterstykke (Navn)
            ON DELETE CASCADE
            ON UPDATE NO ACTION,
    FOREIGN KEY (SalNavn)
        REFERENCES Sal (Navn)
            ON DELETE CASCADE
            ON UPDATE NO ACTION,
    FOREIGN KEY (MånedVises, DagVises)
        REFERENCES Dato (Måned, Dag)
            ON DELETE CASCADE
            ON UPDATE NO ACTION
);

CREATE TABLE IF NOT EXISTS Kundeprofil (
    Mobilnummer TEXT NOT NULL,
    Adresse TEXT NOT NULL,
    Navn TEXT NOT NULL,
    PRIMARY KEY (Mobilnummer)
);

CREATE TABLE IF NOT EXISTS Billettkjøp (
    ID INTEGER NOT NULL,
    MånedKjøpt INTEGER NOT NULL,
    DagKjøpt INTEGER NOT NULL,
    KundeprofilMobilnummer TEXT NOT NULL,
    TeaterstykkeNavn TEXT NOT NULL,
    SalNavn TEXT NOT NULL,
    MånedVises INTEGER NOT NULL,
    DagVises INTEGER NOT NULL,
    PRIMARY KEY (ID),
    FOREIGN KEY (MånedKjøpt, DagKjøpt)
        REFERENCES Dato (Måned, Dag)
            ON DELETE CASCADE
            ON UPDATE NO ACTION,
    FOREIGN KEY (KundeprofilMobilnummer)
        REFERENCES Kundeprofil (Mobilnummer)
            ON DELETE CASCADE
            ON UPDATE NO ACTION,
    FOREIGN KEY (TeaterstykkeNavn, SalNavn, MånedVises, DagVises)
        REFERENCES Forestilling (TeaterstykkeNavn, SalNavn, MånedVises, DagVises)
            ON DELETE CASCADE
            ON UPDATE NO ACTION
);

CREATE TABLE IF NOT EXISTS Gruppe (
    TeaterstykkeNavn TEXT NOT NULL,
    Navn TEXT NOT NULL,
    Pris INTEGER NOT NULL,
    Pris10 INTEGER NOT NULL,
    PRIMARY KEY (TeaterstykkeNavn, Navn),
    FOREIGN KEY (TeaterstykkeNavn)
        REFERENCES Teaterstykke (Navn)
            ON DELETE CASCADE
            ON UPDATE NO ACTION
);

CREATE TABLE IF NOT EXISTS Billett (
    BillettkjøpID INTEGER NOT NULL,
    SalNavn TEXT NOT NULL,
    StolNummer INTEGER NOT NULL,
    RadNummer INTEGER NOT NULL,
    Område TEXT NOT NULL,
    TeaterstykkeNavn TEXT NOT NULL,
    GruppeNavn TEXT NOT NULL,
    PRIMARY KEY (BillettkjøpID, SalNavn, StolNummer, RadNummer, Område, TeaterstykkeNavn, GruppeNavn),
    FOREIGN KEY (BillettkjøpID)
        REFERENCES Billettkjøp (ID)
            ON DELETE CASCADE
            ON UPDATE NO ACTION,
    FOREIGN KEY (SalNavn, StolNummer, RadNummer, Område)
        REFERENCES Stol (SalNavn, Nummer, RadNummer, Område)
            ON DELETE CASCADE
            ON UPDATE NO ACTION,
    FOREIGN KEY (TeaterstykkeNavn, GruppeNavn)
        REFERENCES Gruppe (TeaterstykkeNavn, Navn)
            ON DELETE CASCADE
            ON UPDATE NO ACTION
);
