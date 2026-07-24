
favourite_chais = [
    "Masala Chai", "Green Tea", "Masala Chai",
    "Lemon Tea", "Green Tea", "Elaichi Chai"
]

unique_chais = {chai for chai in favourite_chais if len(chai) > 9}
print(unique_chais)

recipes = {
    "Masala Chai": ["ginger", "cardamom", "clove"],
    "Elaichi Chai": ["cardamom", "sugar", "milk"],
    "Spicy Chai": ["ginger", "black pepper", "clove"]
} 

unique_ingredients = {ingredient for ingredients in recipes.values() for ingredient in ingredients}
print(unique_ingredients)