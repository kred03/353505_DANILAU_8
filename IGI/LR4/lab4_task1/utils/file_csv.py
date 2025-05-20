import csv
from models.product import Product

def save_products_to_csv(filename: str, products: list[Product]) -> None:
    """Сохраняет список объектов продукта в CSV-файл"""
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=['name', 'old_price', 'new_price'])
        writer.writeheader()
        for product in products:
            writer.writerow(product.to_dict())

def load_products_from_csv(filename: str) -> list[Product]:
    """Загружает продукты из CSV-файла и возвращает список объектов Product"""
    products = []
    with open(filename, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            products.append(Product.from_dict(row))
    return products
