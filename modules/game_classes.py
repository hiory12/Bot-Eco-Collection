class Objet:
    def __init__(self, nom, prix, rarete):
        self.nom = nom
        self.prix = prix
        self.rarete = rarete  # [Barème: Complexité] Ajout de rareté

    def to_dict(self):
        return {"nom": self.nom, "prix": self.prix, "rarete": self.rarete}

class Joueur:
    def __init__(self, id_discord, argent=0, inventaire=None):
        self.id = id_discord
        self.argent = argent
        self.inventaire = inventaire if inventaire else []

    def acheter(self, objet):
        if self.argent >= objet.prix:
            self.argent -= objet.prix
            self.inventaire.append(objet.nom)
            return True
        return False
