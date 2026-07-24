
class Chai:
    temperature = "hot"
    strength = "Strong"

cutting = Chai()
print(cutting.temperature)

cutting.temperature = "Mild"
print(cutting.temperature)
print(Chai.temperature)

del cutting.temperature
print(cutting.temperature)