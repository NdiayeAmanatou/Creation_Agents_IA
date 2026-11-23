import sqlite3
from pathlib import Path

CHEMIN_BASE = Path(__file__).parent / "catalogue.db"

BIENS = [
    ("SK-001", "appartement", "Mermoz", "Rue MZ-12, villa 45, Mermoz", 3, 350000, 0, 1, "Awa", "F3 lumineux au 2e étage, balcon, proche VDN."),
    ("SK-002", "appartement", "Mermoz", "Rue MZ-27, immeuble Bamba, Mermoz", 3, 380000, 1, 1, "Awa", "F3 meublé, climatisé, gardien 24h/24."),
    ("SK-003", "appartement", "Mermoz", "Rue MZ-03, résidence Kër Gui, Mermoz", 3, 450000, 0, 1, "Moussa", "F3 standing avec parking et groupe électrogène."),
    ("SK-004", "appartement", "Mermoz", "Rue MZ-40, immeuble Diallo, Mermoz", 4, 550000, 0, 1, "Moussa", "F4 spacieux, 2 salles de bain, terrasse."),
    ("SK-005", "studio", "Mermoz", "Rue MZ-18, Mermoz", 1, 150000, 1, 1, "Fatou", "Studio meublé idéal pour étudiant ou jeune actif."),
    ("SK-006", "appartement", "Sacré-Cœur", "Sacré-Cœur 3, villa 112", 3, 300000, 0, 1, "Fatou", "F3 au rez-de-chaussée avec petite cour."),
    ("SK-007", "appartement", "Sacré-Cœur", "Sacré-Cœur 2, villa 8", 2, 200000, 0, 1, "Awa", "F2 calme, proche école et commerces."),
    ("SK-008", "appartement", "Sacré-Cœur", "Sacré-Cœur 1, immeuble Ndiaye", 4, 400000, 0, 0, "Awa", "F4 familial, actuellement loué."),
    ("SK-009", "villa", "Almadies", "Route des Almadies, lot 22", 5, 1500000, 0, 1, "Moussa", "Villa avec piscine, jardin et vue mer."),
    ("SK-010", "appartement", "Almadies", "Almadies, résidence Océan, apt 4B", 3, 700000, 1, 1, "Moussa", "F3 haut standing meublé, vue mer."),
    ("SK-011", "studio", "Almadies", "Almadies, zone 2, villa 9", 1, 250000, 1, 1, "Fatou", "Studio meublé à 5 minutes de la plage."),
    ("SK-012", "appartement", "Ngor", "Ngor village, rue NG-5", 2, 300000, 0, 1, "Fatou", "F2 avec terrasse, proche de l'île de Ngor."),
    ("SK-013", "villa", "Ngor", "Ngor, route de la plage, lot 3", 4, 1200000, 0, 0, "Awa", "Villa 4 pièces avec jardin, actuellement louée."),
    ("SK-014", "appartement", "Ouakam", "Ouakam, cité Comico, bloc C", 3, 280000, 0, 1, "Awa", "F3 dans cité calme et sécurisée."),
    ("SK-015", "appartement", "Ouakam", "Ouakam, rue OK-14", 2, 180000, 0, 1, "Moussa", "F2 simple, proche des transports."),
    ("SK-016", "appartement", "Point E", "Point E, rue PE-6, immeuble Fall", 3, 420000, 0, 1, "Moussa", "F3 rénové, proche de l'université."),
    ("SK-017", "appartement", "Point E", "Point E, rue PE-11", 2, 320000, 1, 1, "Fatou", "F2 meublé et équipé, internet fibre."),
    ("SK-018", "appartement", "Fann", "Fann Résidence, rue FN-2", 4, 600000, 0, 1, "Fatou", "F4 dans quartier résidentiel calme."),
    ("SK-019", "appartement", "Plateau", "Plateau, avenue Pompidou, immeuble 31", 2, 350000, 1, 1, "Awa", "F2 meublé en centre-ville, ascenseur."),
    ("SK-020", "appartement", "Plateau", "Plateau, rue Carnot, immeuble 7", 3, 500000, 0, 1, "Awa", "F3 avec vue sur le port."),
    ("SK-021", "studio", "Plateau", "Plateau, rue Vincens, immeuble 15", 1, 200000, 1, 0, "Moussa", "Studio meublé, actuellement loué."),
    ("SK-022", "appartement", "Médina", "Médina, rue 22 x 15", 2, 150000, 0, 1, "Moussa", "F2 traditionnel, proche du marché Tilène."),
    ("SK-023", "appartement", "Liberté 6", "Liberté 6 extension, villa 201", 3, 250000, 0, 1, "Fatou", "F3 neuf, carrelé, avec placards."),
    ("SK-024", "appartement", "Liberté 6", "Liberté 6, rond-point JVC, immeuble 4", 4, 320000, 0, 1, "Fatou", "F4 familial au 1er étage."),
    ("SK-025", "appartement", "Yoff", "Yoff, cité Tonghor, villa 17", 3, 230000, 0, 1, "Awa", "F3 proche de la plage de Yoff."),
    ("SK-026", "villa", "Yoff", "Yoff Virage, lot 58", 5, 650000, 0, 1, "Awa", "Villa 5 pièces avec garage."),
    ("SK-027", "appartement", "HLM", "HLM 5, villa 340", 2, 130000, 0, 1, "Moussa", "F2 économique, proche du marché HLM."),
    ("SK-028", "appartement", "Grand Yoff", "Grand Yoff, rue GY-30", 3, 200000, 0, 1, "Moussa", "F3 au 1er étage, quartier animé."),
    ("SK-029", "appartement", "Parcelles Assainies", "Parcelles Assainies, unité 15, villa 88", 3, 175000, 0, 1, "Fatou", "F3 avec petite terrasse."),
    ("SK-030", "duplex", "Sicap Baobab", "Sicap Baobab, villa 210", 4, 480000, 0, 1, "Fatou", "Duplex 4 pièces avec jardinet."),
]

def creer_catalogue():
    if CHEMIN_BASE.exists():
        CHEMIN_BASE.unlink()

    connexion=sqlite3.connect(CHEMIN_BASE)

    connexion.execute("""
        CREATE TABLE biens (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            reference   TEXT    NOT NULL UNIQUE,
            type        TEXT    NOT NULL,
            quartier    TEXT    NOT NULL,
            adresse     TEXT    NOT NULL,
            pieces      INTEGER NOT NULL,
            loyer       INTEGER NOT NULL,
            meuble      INTEGER NOT NULL,
            disponible  INTEGER NOT NULL,
            conseiller  TEXT    NOT NULL,
            description TEXT    NOT NULL
        )
    """)

    connexion.executemany(
        """
        INSERT INTO biens (reference, type, quartier, adresse, pieces, loyer,
                           meuble, disponible, conseiller, description)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        BIENS,
    )

    nombre = connexion.execute("SELECT COUNT(*) FROM biens").fetchone()[0]
    print(f"Catalogue créé : {nombre} biens")

    connexion.commit()
    connexion.close()


if __name__ == "__main__":
    creer_catalogue()