class Product:
    """Класс с информацией о ценах"""

    def __init__(self, name: str, old_price: float, new_price: float):
        self.name = name
        self.old_price = old_price
        self.new_price = new_price

    @property
    def price_increase(self) -> float:
        """Увеличение цены на проценты либо 0"""
        if self.new_price > self.old_price:
            return round(((self.new_price - self.old_price) / self.old_price) * 100, 2)
        return 0.0

    def has_increased(self) -> bool:
        """Возвращает True, если цена выросла"""
        return self.new_price > self.old_price

    def __str__(self):
        return (f"Product: {self.name}, Old Price: {self.old_price:.2f}, "
                f"New Price: {self.new_price:.2f}, "
                f"Increase: {self.price_increase:.2f}%")

    def __repr__(self):
        return f"Product('{self.name}', {self.old_price}, {self.new_price})"

    @staticmethod
    def from_dict(data: dict):
        """Создает экземпляр продукта из словаря"""
        return Product(data['name'], float(data['old_price']), float(data['new_price']))

    def to_dict(self) -> dict:
        """Возвращает продукт в виде словаря"""
        return {
            'name': self.name,
            'old_price': self.old_price,
            'new_price': self.new_price
        }
