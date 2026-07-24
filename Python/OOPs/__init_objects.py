
class Chai_order:

    # Constructor 
    def __init__(self, type_, size):
        self.type = type_
        self.size = size

    def summary(self):
        return f"A {self.size}ml {self.type} order"

order = Chai_order("Masala Chai", 200)
print(order.summary())