class Item:
    def __init__(self, name, price, rarity, description, image_url):
        self.name = name
        self.price = price
        self.rarity = rarity
        self.description = description
        self.image_url = image_url

    def to_dict(self):
        return {
            "name": self.name, 
            "price": self.price, 
            "rarity": self.rarity,
            "description": self.description,
            "image_url": self.image_url
        }

class Player:
    def __init__(self, discord_id, money=0, inventory=None):
        self.id = discord_id
        self.money = money
        self.inventory = inventory if inventory else []

    def buy(self, item):
        if self.money >= item.price:
            self.money -= item.price
            self.inventory.append(item.name)
            return True
        return False