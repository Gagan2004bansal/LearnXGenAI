orders = ["masala", "ginger"]

try:
    print(orders[2])
except IndexError:
    print("The index you are trying to access is out of range. Please check the index and try again.")

print("Program continues to run after handling the exception.")


def serve_chai(flavor):
    try:
        print("preparing " + flavor + " chai...")
        if flavor == "unknown":
            raise ValueError("Unknown flavor. Please choose a valid flavor.")
    except ValueError as e:
        print(e)
    else:
        print(flavor + " chai is ready to serve!")
    finally:
        print("Thank you for visiting our chai shop!")
    
serve_chai("unknown")


# RASING AN ERROR 
def brew_chai(flavor):
        if flavor not in ["masala", "ginger"]:
            raise ValueError("Invalid flavor. Please choose either 'masala' or 'ginger'.")
    
brew_chai("mint")  # This will raise a ValueError since "mint" is not a valid flavor.