from dataclasses import dataclass


@dataclass
class Order:
    """Data structure to represent and order for a table"""

    menu_items: list[str]
    table_number: int


class MenuService:
    def get_menu(self) -> dict[str, list[str]]:
        return {
            "Appetizers": [
                "Bruschetta with Fresh Tomatoes and Basil (V)",
                "Crispy Calamari with Lemon Aioli",
                "French Onion Soup (GF option)",
                "Quinoa Stuffed Bell Peppers (VG, GF)",
                "Beef Carpaccio with Arugula (GF)",
            ],
            "Main Courses": [
                "Grilled Salmon with Herb Butter (GF)",
                "Filet Mignon with Red Wine Reduction (GF)",
                "Wild Mushroom Risotto (V option, GF)",
                "Pan-Seared Duck Breast",
                "Chickpea and Sweet Potato Curry (VG, GF)",
                "Gluten-Free Pasta with Roasted Vegetables (VG, GF)",
                "Beyond Meat Burger with Avocado (VG)",
            ],
            "Desserts": [
                "Crème Brûlée (V, GF)",
                "Dark Chocolate Mousse (V option)",
                "New York Style Cheesecake",
                "Vegan Apple Crumble (VG)",
                "Fresh Fruit Sorbet (VG, GF)",
                "Classic Tiramisu",
            ],
        }


class OrderService:
    orders: list[Order]

    def __init__(self):
        self.orders = []

    def create_order(self, table_number: int, menu_items: list[str]):
        self.orders.append(Order(table_number=table_number, menu_items=menu_items))

    def get_orders(self) -> list[Order]:
        return self.orders
