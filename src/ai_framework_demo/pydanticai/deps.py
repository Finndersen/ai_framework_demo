from dataclasses import dataclass

from ai_framework_demo.services import MenuService, OrderService


@dataclass
class Dependencies:
    menu_service: MenuService
    order_service: OrderService
    restaurant_name: str
    table_number: int
