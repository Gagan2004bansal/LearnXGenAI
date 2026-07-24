

class BaseChai:

    def __init__(self, type_):
        self.type = type_

    def prepare(self):
        return f"Preparing {self.type}"
    

class MasalaChai(BaseChai):
    def add_spices(self):
        print("Adding spices to the chai")


class ChaiShop:
    chai_cls = BaseChai

    def __init__(self):
        self.chai = self.chai_cls("Regular")

    def serve_chai(self):
        print(f"Serving {self.chai.type} chai in the shop")
        self.chai.prepare()


class FancyChaiShop(ChaiShop):
    chai_cls = MasalaChai

    def serve_chai(self):
        print(f"Serving {self.chai.type} chai in the fancy shop")
        self.chai.prepare()
        self.chai.add_spices()


shop = ChaiShop()
fancyshop = FancyChaiShop()

fancyshop.serve_chai()
shop.serve_chai()

fancyshop.chai_cls.add_spices()


# zero shot prompting
# few shot prompting
# chain of thought
# auto-chain of thought
# persona based prompting