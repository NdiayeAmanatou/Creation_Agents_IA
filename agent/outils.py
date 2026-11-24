import sqlite3
from pathlib import Path

# outils.py est dans agent\ ; la base est dans donnees\
CHEMIN_BASE = Path(__file__).parent.parent / "donnees" / "catalogue.db"


def _connexion():
    connexion = sqlite3.connect(CHEMIN_BASE)
    connexion.row_factory = sqlite3.Row
    return connexion

def rechercher_biens(
    quartier: str | None = None,
    type_bien: str | None = None,
    pieces: int | None = None,
    loyer_max: int | None = None,
    meuble: bool | None = None,
) -> dict:
    """Recherche les biens DISPONIBLES à la location dans le catalogue de l'agence Sama Kër.

    Tous les critères sont facultatifs : ne renseigner que ceux exprimés par le client.

    Args:
        quartier: quartier de Dakar, ex. "Mermoz", "Almadies", "Point E".
        type_bien: "appartement", "studio", "villa" ou "duplex".
        pieces: nombre de pièces. Un F3 = 3 pièces, un F4 = 4 pièces, un studio = 1.
        loyer_max: loyer mensuel maximum en francs CFA, ex. 400000.
        meuble: True si le client veut un logement meublé, False s'il veut du non meublé.

    Returns:
        Les biens correspondants triés par loyer croissant, ou un message clair
        si aucun bien ne correspond.
    """
    # 1. Vérifier les arguments : une erreur claire vaut mieux qu'un résultat absurde.
    if loyer_max is not None and loyer_max <= 0:
        return {"erreur": "loyer_max doit être un nombre positif en F CFA, ex. 400000."}
    if pieces is not None and pieces <= 0:
        return {"erreur": "pieces doit être un entier positif, ex. 3 pour un F3."}

    connexion = _connexion()

    # 2. Si le quartier est inconnu, on le dit ET on donne la liste des quartiers valides.
    if quartier is not None:
        quartiers_connus = [
            ligne["quartier"]
            for ligne in connexion.execute("SELECT DISTINCT quartier FROM biens ORDER BY quartier")
        ]
        if quartier.strip().lower() not in [q.lower() for q in quartiers_connus]:
            connexion.close()
            return {
                "erreur": f"Le quartier '{quartier}' n'est pas couvert par l'agence.",
                "quartiers_couverts": quartiers_connus,
            }

    # 3. Construire la requête morceau par morceau, selon les critères fournis.
    conditions = ["disponible = 1"]      # on ne propose JAMAIS un bien déjà loué
    valeurs = []

    if quartier is not None:
        conditions.append("quartier = ? COLLATE NOCASE")   # NOCASE : "mermoz" = "Mermoz"
        valeurs.append(quartier.strip())
    if type_bien is not None:
        conditions.append("type = ? COLLATE NOCASE")
        valeurs.append(type_bien.strip())
    if pieces is not None:
        conditions.append("pieces = ?")
        valeurs.append(pieces)
    if loyer_max is not None:
        conditions.append("loyer <= ?")
        valeurs.append(loyer_max)
    if meuble is not None:
        conditions.append("meuble = ?")
        valeurs.append(1 if meuble else 0)

    requete = (
        "SELECT reference, type, quartier, pieces, loyer, meuble FROM biens WHERE "
        + " AND ".join(conditions)
        + " ORDER BY loyer"
    )
    lignes = connexion.execute(requete, valeurs).fetchall()
    connexion.close()

    # 4. Formater le résultat. Le cas "zéro résultat" est EXPLICITE.
    if not lignes:
        return {
            "nombre_resultats": 0,
            "message": "Aucun bien disponible ne correspond à ces critères.",
        }

    return {
        "nombre_resultats": len(lignes),
        "biens": [
            {
                "reference": l["reference"],
                "type": l["type"],
                "quartier": l["quartier"],
                "pieces": l["pieces"],
                "loyer_fcfa": l["loyer"],
                "meuble": bool(l["meuble"]),
            }
            for l in lignes
        ],
    }

def detail_bien(reference: str) -> dict:
    """Donne la fiche complète d'un bien du catalogue : adresse, description,
    disponibilité et conseiller responsable.

    Args:
        reference: référence du bien telle que renvoyée par rechercher_biens, ex. "SK-002".
    """
    reference = reference.strip().upper()

    connexion = _connexion()
    ligne = connexion.execute(
        "SELECT * FROM biens WHERE reference = ?", (reference,)
    ).fetchone()
    connexion.close()

    if ligne is None:
        return {
            "erreur": f"Aucun bien avec la référence '{reference}'.",
            "conseil": "Les références ont la forme SK-001 à SK-030. "
                       "Utiliser rechercher_biens pour trouver une référence valide.",
        }

    return {
        "reference": ligne["reference"],
        "type": ligne["type"],
        "quartier": ligne["quartier"],
        "adresse": ligne["adresse"],
        "pieces": ligne["pieces"],
        "loyer_fcfa": ligne["loyer"],
        "meuble": bool(ligne["meuble"]),
        "disponible": bool(ligne["disponible"]),
        "conseiller": ligne["conseiller"],
        "description": ligne["description"],
    }

if __name__ == "__main__":
    print(rechercher_biens(quartier="Mermoz", pieces=3, loyer_max=400000))
    print(rechercher_biens(quartier="Mermos"))
    print(rechercher_biens(type_bien="villa", quartier="Médina"))
    print(detail_bien("sk-002"))
    print(detail_bien("SK-999"))