from abc import ABC, abstractmethod, abstractclassmethod


class Pizza(ABC):
    ingredients: list[str]

    def change_ingredients(self, ingredients: list[str]) -> None:
        self.ingredients = ingredients

    def prepare(self):
        message = f"preparing the pizza with "

        for ingredient in self.ingredients:
            message += ingredient + " "

        print(message)

    def bake(self):
        print("baking the pizza in the oven for 8 1/2 minutes.")

    def cut(self):
        print("cutting the pizza into 8 equally big slices")

    def box(self):
        print("boxing the pizza so it can stay warm and fresh")


class PizzaStore(ABC):
    @abstractmethod
    def process_order() -> Pizza:
        """prepare the pizza"""


