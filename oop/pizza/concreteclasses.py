from abstractclasses import Pizza, PizzaStore


class CheesePizza(Pizza):
    ingredients: list[str] = ["dough", "tomatoes", "cheese"]



class PepperoniPizza(Pizza):
    ingredients: list[str] = ["dough", "tomatoes", "pepperoni"]



class BerlinerPlatz(PizzaStore):
    def process_order(self) -> Pizza:
        berliner_cheese = CheesePizza()
        berliner_platz_ingredients = ['dough', 'tomatoes', 'cheese', 'basil']

        berliner_cheese.change_ingredients(berliner_platz_ingredients)
        berliner_cheese.prepare()
        berliner_cheese.bake()
        berliner_cheese.cut()
        berliner_cheese.box()

        return berliner_cheese