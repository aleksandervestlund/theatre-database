TEATERSTYKKER = [
    ("Kongsemnene", "Henrik Ibsen", "19.00"),
    ("Størst av alt er kjærligheten", "Jonas Corell Petersen", "18.30"),
]

GRUPPER = [
    ("Kongsemnene", "Ordinær", "450"),
    ("Kongsemnene", "Honnør", "380"),
    ("Kongsemnene", "Student", "280"),
    ("Størst av alt er kjærligheten", "Ordinær", "350"),
    ("Størst av alt er kjærligheten", "Honnør", "300"),
    ("Størst av alt er kjærligheten", "Student", "220"),
    ("Størst av alt er kjærligheten", "Barn", "220"),
]

OPPGAVER = [
    ("Kongsemnene", "Regi og musikkutvelgelse"),
    ("Kongsemnene", "Scenografi og kostymer"),
    ("Kongsemnene", "Lysdesign"),
    ("Kongsemnene", "Dramaturg"),
    ("Størst av alt er kjærligheten", "Regi"),
    ("Størst av alt er kjærligheten", "Scenografi og kostymer"),
    ("Størst av alt er kjærligheten", "Musikalsk ansvarlig"),
    ("Størst av alt er kjærligheten", "Lysdesign"),
    ("Størst av alt er kjærligheten", "Dramaturg"),
]

# Ansattstatus, Navn, TeaterstykkeNavn, OppgaveNavn
# fmt: off
ANSATTE = [
    ("Fast", "Yury Butusov", "Kongsemnene", "Regi og musikkutvelgelse"),
    ("Fast", "Aleksandr Shishkin-Hokusai", "Kongsemnene", "Scenografi og kostymer"),
    ("Fast", "Eivind Myren", "Kongsemnene", "Lysdesign"),
    ("Fast", "Mina Rype Stokke", "Kongsemnene", "Dramaturg"),
    ("Fast", "Jonas Corell Petersen", "Størst av alt er kjærligheten", "Regi"),
    ("Fast", "David Gehrt", "Størst av alt er kjærligheten", "Scenografi og kostymer"),
    ("Fast", "Gaute Tønder", "Størst av alt er kjærligheten", "Musikalsk ansvarlig"),
    ("Fast", "Magnus Mikaelsen", "Størst av alt er kjærligheten", "Lysdesign"),
    ("Fast", "Kristoffer Spender", "Størst av alt er kjærligheten", "Dramaturg"),
]
# fmt: on

# TeaterstykkeNavn, Nummer
AKTER = [
    ("Kongsemnene", 1),
    ("Kongsemnene", 2),
    ("Kongsemnene", 3),
    ("Kongsemnene", 4),
    ("Kongsemnene", 5),
    ("Størst av alt er kjærligheten", 1),
]

ROLLER = [
    # Kongsemnene
    ("Haakon Haakonssønn",),
    ("Inga fra Vartejg",),
    ("Skule jarl",),
    ("Fru Ragnhild",),
    ("Margrete",),
    ("Sigrid",),
    ("Ingebjørg",),
    ("Biskop Nikolas",),
    ("Gregorius Jonssønn",),
    ("Paal Flida",),
    ("Baard Bratte",),
    ("Jatgeir Skald",),
    ("Dagfinn Bonde",),
    ("Peter",),
    # Størst av alt er kjærligheten
    ("Sunniva Du Mond Nordal",),
    ("Jo Saberniak",),
    ("Marte M. Steinholt",),
    ("Tor Ivar Hagen",),
    ("Trond-Ove Skrødal",),
    ("Natalie Grøndahl Tangen",),
    ("Åsmund Flaten",),
]

# fmt: off
DELTAR_I = []
DELTAR_I.extend([("Haakon Haakonssønn", "Kongsemnene", i) for i in range(1, 6)])
DELTAR_I.extend([("Inga fra Vartejg", "Kongsemnene", i) for i in (1, 3)])
DELTAR_I.extend([("Skule jarl", "Kongsemnene", i) for i in range(1, 6)])
DELTAR_I.extend([("Fru Ragnhild", "Kongsemnene", i) for i in (1, 5)])
DELTAR_I.extend([("Margrete", "Kongsemnene", i) for i in range(1, 6)])
DELTAR_I.extend([("Sigrid", "Kongsemnene", i) for i in (1, 2, 5)])
DELTAR_I.append(("Ingebjørg", "Kongsemnene", 4))
DELTAR_I.extend([("Biskop Nikolas", "Kongsemnene", i) for i in range(1, 4)])
DELTAR_I.extend([("Gregorius Jonssønn", "Kongsemnene", i) for i in range(1, 6)])
DELTAR_I.extend([("Paal Flida", "Kongsemnene", i) for i in range(1, 6)])
DELTAR_I.extend([("Baard Bratte", "Kongsemnene", i) for i in (4, 5)])
DELTAR_I.append(("Jatgeir Skald", "Kongsemnene", 1))
DELTAR_I.extend([("Dagfinn Bonde", "Kongsemnene", i) for i in range(2, 6)])
DELTAR_I.extend([("Peter", "Kongsemnene", i) for i in range(3, 6)])
DELTAR_I.append(("Sunniva Du Mond Nordal", "Størst av alt er kjærligheten", 1))
DELTAR_I.append(("Jo Saberniak", "Størst av alt er kjærligheten", 1))
DELTAR_I.append(("Marte M. Steinholt", "Størst av alt er kjærligheten", 1))
DELTAR_I.append(("Tor Ivar Hagen", "Størst av alt er kjærligheten", 1))
DELTAR_I.append(("Trond-Ove Skrødal", "Størst av alt er kjærligheten", 1))
DELTAR_I.append(("Natalie Grøndahl Tangen", "Størst av alt er kjærligheten", 1))
DELTAR_I.append(("Åsmund Flaten", "Størst av alt er kjærligheten", 1))
# fmt: on

# Navn
SKUESPILLERE = [
    # Kongsemnene
    ("Arturo Scotti",),
    ("Ingunn Beate Strige Øyen",),
    ("Hans Petter Nilsen",),
    ("Madeleine Brandtzæg Nilsen",),
    ("Synnøve Fossum Eriksen",),
    ("Emma Caroline Deichmann",),
    ("Thomas Jensen Takyi",),
    ("Per Bogstad Gulliksen",),
    ("Isak Holmen Sørensen",),
    ("Fabian Heidelberg Lunde",),
    ("Emil Olafsson",),
    ("Snorre Ryen Tøndel",),
    # Størst av alt er kjærligheten
    ("Sunniva Du Mond Nordal",),
    ("Jo Saberniak",),
    ("Marte M. Steinholt",),
    ("Tor Ivar Hagen",),
    ("Trond-Ove Skrødal",),
    ("Natalie Grøndahl Tangen",),
    ("Åsmund Flaten",),
]

SPILLER_ROLLER = [
    # Kongsemnene
    (1, "Haakon Haakonssønn"),
    (2, "Inga fra Vartejg"),
    (3, "Skule jarl"),
    (4, "Fru Ragnhild"),
    (5, "Margrete"),
    (6, "Sigrid"),
    (6, "Ingebjørg"),
    (7, "Biskop Nikolas"),
    (8, "Gregorius Jonssønn"),
    (9, "Paal Flida"),
    (10, "Baard Bratte"),
    (11, "Jatgeir Skald"),
    (11, "Dagfinn Bonde"),
    (12, "Peter"),
    # Størst av alt er kjærligheten
    (13, "Sunniva Du Mond Nordal"),
    (14, "Jo Saberniak"),
    (15, "Marte M. Steinholt"),
    (16, "Tor Ivar Hagen"),
    (17, "Trond-Ove Skrødal"),
    (18, "Natalie Grøndahl Tangen"),
    (19, "Åsmund Flaten"),
]

DATOER = []
DATOER.extend([(1, day) for day in range(1, 32)])
DATOER.extend([(2, day) for day in range(1, 15)])  # Siste forestilling 14/2

SALER = [
    ("Hovedscenen",),
    ("Gamle Scene",),
    ("Studioscenen",),
    ("Teaterkjelleren",),
    ("Teaterkafeen",),
]

# fmt: off
STOLER = []
HOVEDSCENE_STOLER = []
HOVEDSCENE_STOLER.extend([("Hovedscenen", plass, ((plass - 1) // 28) + 1, "") for plass in range(1, 467)])
HOVEDSCENE_STOLER.extend([("Hovedscenen", plass, ((plass - 1) // 28) + 1, "") for plass in range(471, 495)])
HOVEDSCENE_STOLER.extend([("Hovedscenen", plass, ((plass - 1) // 28) + 1, "") for plass in range(499, 505)])
HOVEDSCENE_STOLER.extend([("Hovedscenen", plass, ((plass - 505) // 10) + 1, "Galleri") for plass in range(505, 525)])
STOLER.extend(HOVEDSCENE_STOLER)

GAMLE_SCENE_STOLER = []
GAMLE_SCENE_STOLER.extend([("Gamle Scene", plass, 1, "Parkett") for plass in range(1, 19)])
GAMLE_SCENE_STOLER.extend([("Gamle Scene", plass, 2, "Parkett") for plass in range(1, 17)])
GAMLE_SCENE_STOLER.extend([("Gamle Scene", plass, 3, "Parkett") for plass in range(1, 18)])
GAMLE_SCENE_STOLER.extend([("Gamle Scene", plass, rad, "Parkett") for plass in range(1, 19) for rad in (4, 5)])
GAMLE_SCENE_STOLER.extend([("Gamle Scene", plass, 6, "Parkett") for plass in range(1, 18)])
GAMLE_SCENE_STOLER.extend([("Gamle Scene", plass, 7, "Parkett") for plass in range(1, 19)])
GAMLE_SCENE_STOLER.extend([("Gamle Scene", plass, rad, "Parkett") for plass in range(1, 18) for rad in (8, 9)])
GAMLE_SCENE_STOLER.extend([("Gamle Scene", plass, 10, "Parkett") for plass in range(1, 15)])
GAMLE_SCENE_STOLER.extend([("Gamle Scene", plass, 1, "Balkong") for plass in range(1, 29)])
GAMLE_SCENE_STOLER.extend([("Gamle Scene", plass, 2, "Balkong") for plass in range(1, 28)])
GAMLE_SCENE_STOLER.extend([("Gamle Scene", plass, 3, "Balkong") for plass in range(1, 23)])
GAMLE_SCENE_STOLER.extend([("Gamle Scene", plass, 4, "Balkong") for plass in range(1, 18)])
GAMLE_SCENE_STOLER.extend([("Gamle Scene", plass, 1, "Galleri") for plass in range(1, 34)])
GAMLE_SCENE_STOLER.extend([("Gamle Scene", plass, 2, "Galleri") for plass in range(1, 19)])
GAMLE_SCENE_STOLER.extend([("Gamle Scene", plass, 3, "Galleri") for plass in range(1, 18)])
STOLER.extend(GAMLE_SCENE_STOLER)
# fmt: on

FORESTILLINGER = [
    ("Kongsemnene", "Hovedscenen", 2, 1),
    ("Kongsemnene", "Hovedscenen", 2, 2),
    ("Kongsemnene", "Hovedscenen", 2, 3),
    ("Kongsemnene", "Hovedscenen", 2, 5),
    ("Kongsemnene", "Hovedscenen", 2, 6),
    ("Størst av alt er kjærligheten", "Gamle Scene", 2, 3),
    ("Størst av alt er kjærligheten", "Gamle Scene", 2, 6),
    ("Størst av alt er kjærligheten", "Gamle Scene", 2, 7),
    ("Størst av alt er kjærligheten", "Gamle Scene", 2, 12),
    ("Størst av alt er kjærligheten", "Gamle Scene", 2, 13),
    ("Størst av alt er kjærligheten", "Gamle Scene", 2, 14),
]

# Admin-bruker
KUNDEPROFILER = [("004700000000", "Høgskoleringen 1", "Holters")]

TABLES = [
    "Teaterstykke",
    "Gruppe",
    "Oppgave",
    "Ansatt",
    "Akt",
    "Rolle",
    "DeltarI",
    "Skuespiller",
    "SpillerRolle",
    "Dato",
    "Sal",
    "Stol",
    "Forestilling",
    "Kundeprofil",
    "Billettkjøp",
    "Billett",
]

ATTRIBUTES = {
    "Adresse",
    "AktNummer",
    "Ansattstatus",
    "BillettkjøpID",
    "Dag",
    "DagKjøpt",
    "DagVises",
    "EPostadresse",
    "Forfatter",
    "GruppeNavn",
    "ID",
    "Klokkeslett",
    "KundeprofilMobilnummer",
    "Mobilnummer",
    "Måned",
    "MånedKjøpt",
    "MånedVises",
    "Navn",
    "Nummer",
    "Område",
    "OppgaveNavn",
    "Pris",
    "RadNummer",
    "RolleNavn",
    "SalNavn",
    "SkuespillerID",
    "StolNummer",
    "TeaterstykkeNavn",
}
