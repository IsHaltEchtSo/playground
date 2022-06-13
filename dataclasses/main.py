from dataclasses import dataclass

@dataclass(frozen=True, order=True)
class Smartphone:
    brand: str
    price: int

    def stats(self):
        print(f'the smartphone is from {self.brand} and costs {self.price}$!')


iPhone7 = Smartphone('apple', 650)
iPhone8 = Smartphone('apple', 555)
print(iPhone8)
iPhone8.stats()
print(iPhone7 < iPhone8)
