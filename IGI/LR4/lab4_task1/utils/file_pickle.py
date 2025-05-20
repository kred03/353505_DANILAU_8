import pickle
from models.product import Product

def save_products_to_pickle(filename: str, products: list[Product]) -> None:
    """Сохраняет список объектов Product в файле pickle"""
    with open(filename, 'wb') as file:
        pickle.dump(products, file)

def load_products_from_pickle(filename: str) -> list[Product]:
    """Загружает продукты из файла pickle."""
    with open(filename, 'rb') as file:
        return pickle.load(file)
