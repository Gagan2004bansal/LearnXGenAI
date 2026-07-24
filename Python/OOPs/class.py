

## TO CREATE CLASS
class Chai: 
    pass

class ChaiTime:
    pass

# print(type(Chai))  

## TO CREATE OBJECTS
ginger_tea = Chai()

# print(type(ginger_tea))
# print(type(ginger_tea) is Chai)
# print(type(ginger_tea) is ChaiTime)


class Chai_class:
    origin = "India"  # class variable

print(Chai_class.origin)  # Accessing class variable using class name

# we can add more properties like these also
Chai_class.is_hot = True
print(Chai_class.is_hot)  # Accessing class variable using class name

masala = Chai_class()  # Creating an object of the class

print(f"Chai Origin : {masala.origin}")  # Accessing class variable using object

