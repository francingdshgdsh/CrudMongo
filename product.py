class Product:
    def __init__(self, name, price, quantity, category, location):
        self.name = name
        self.price = price
        self.quantity = quantity
        self.category = category
        self.location = location

    def toDBCollection(self):
        return {
            'name': self.name,
            'price': self.price,
            'quantity': self.quantity,
            'category': self.category,
            'location': self.location
        }