import unittest

from abstractclasses import Pizza
from concreteclasses import BerlinerPlatz


class TestPizzaStoreProcessing(unittest.TestCase):
    """test that the store correctly bakes a pizza"""
    def setUp(self) -> None:
        """set up test fixtures"""
        self.store = BerlinerPlatz()

    def test_store_returns_pizza(self):
        """Whether process order returns a pizza"""
        pizza = self.store.process_order()
        self.assertIsInstance(obj=pizza, cls=Pizza)


if __name__ == '__main__':
    unittest.main()