from models.product import Product
from utils.file_csv import save_products_to_csv, load_products_from_csv
from utils.file_pickle import save_products_to_pickle, load_products_from_pickle
from utils.validation import input_float, input_nonempty_string

def menu():
    print("\nProduct Price Analyzer (Lab #4)")
    print("1. Add product")
    print("2. Save to CSV")
    print("3. Load from CSV")
    print("4. Save to Pickle")
    print("5. Load from Pickle")
    print("6. Show products with price increase")
    print("7. Search product by name")
    print("0. Exit")

def search_product(products, name):
    for p in products:
        if p.name.lower() == name.lower():
            return p
    return None

def main():
    products = []

    while True:
        menu()
        choice = input("Choose option: ")

        if choice == '1':
            name = input_nonempty_string("Enter product name: ")
            old_price = input_float("Enter old price: ")
            new_price = input_float("Enter new price: ")
            products.append(Product(name, old_price, new_price))
            print("Product added.")
        elif choice == '2':
            save_products_to_csv('products.csv', products)
            print("Saved to products.csv")
        elif choice == '3':
            try:
                products = load_products_from_csv('products.csv')
                print("Loaded from products.csv")
            except FileNotFoundError:
                print("File not found.")
        elif choice == '4':
            save_products_to_pickle('products.pkl', products)
            print("Saved to products.pkl")
        elif choice == '5':
            try:
                products = load_products_from_pickle('products.pkl')
                print("Loaded from products.pkl")
            except FileNotFoundError:
                print("File not found.")
        elif choice == '6':
            increased = [p for p in products if p.has_increased()]
            if increased:
                print("\nProducts with price increase:")
                for p in increased:
                    print(p)
            else:
                print("No price increases found.")
        elif choice == '7':
            name = input_nonempty_string("Enter product name to search: ")
            result = search_product(products, name)
            if result:
                print(result)
            else:
                print("Product not found.")
        elif choice == '0':
            print("Exiting. Goodbye!")
            break
        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    main()
