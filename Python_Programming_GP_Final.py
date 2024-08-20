# Python Programming Group 14 Final Code Submission
# Jade Gosar, Melanieanthony Vadakkepeedika, Okechukwu Agomuozwsp

# make necessary imports
import csv
import sys

from db_base import DBbase

# Create Recipe class from DBbase
class Recipe(DBbase):

    def __init__(self):
        super().__init__("recipe_manager.sqlite")

    # Define the function that resets the database
    def reset_database(self):
        sql = """
        DROP TABLE IF EXISTS Recipe;
        DROP TABLE IF EXISTS INGREDIENTS;
        DROP TABLE IF EXISTS USERS;

        CREATE TABLE Recipe (
            recipe_id  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            recipe_Name   TEXT,
            category   TEXT,
            ingredients_id INTEGER
        );

        CREATE TABLE INGREDIENTS (
            recipe_id   INTEGER,
            ingredients_ID   INTEGER,
            ingredients   TEXT
        );

        CREATE TABLE USERS (
            user_id  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            role TEXT
        );
        """
        self.execute_script(sql)

    # Create function that gets data from csv file we created containing dishes and ingredients and creates
    # three distinct entities: the Recipe table containing recipe details, the Ingredients table and the User table
    def populate_db_from_csv(self, csv_file):
        with open(csv_file, "r") as file:
            csv_reader = csv.reader(file)
            next(csv_reader)
            for row in csv_reader:
                try:
                    recipe_id, recipe_name, category, ingredient_id, ingredients, user_id, name, role = row
                    sql = "INSERT INTO Recipe (recipe_id, recipe_Name, category, ingredients_id) VALUES (?, ?, ?, ?)"
                    data = (recipe_id, recipe_name, category, ingredient_id)
                    self._cursor.execute(sql, data)
                    self._conn.commit()

                    sql_ingredients = "INSERT INTO INGREDIENTS (recipe_id, ingredients_ID, ingredients) VALUES (?, ?, ?)"
                    data_ingredients = (recipe_id, ingredient_id, ingredients)
                    with self._conn:
                        self._cursor.execute(sql_ingredients, data_ingredients)

                    sql_user = "INSERT INTO USERS (user_id, name, role) VALUES (?, ?, ?)"
                    data_user = (user_id, name, role)
                    with self._conn:
                        self._cursor.execute(sql_user, data_user)

                except ValueError:
                    print(f"Warning: Incorrect data format in row: {row}")

    # Function to enable the database to be closed at the user's request
    def close_db(self):
        print("Closing database...")
        try:
            self._conn.close()
            print("Database closed successfully.")
        except Exception as e:
            print("Error closing database:", e)

    # Add function for adding recipe id, recipe name, category, and ingredients id into the recipes table
    def add(self, recipe_id, recipe_Name, category, ingredients_id):
        try:
            super().get_cursor.execute("insert or ignore into Recipe (recipe_id, recipe_Name, category, ingredients_id) values(?,?,?,?);",
                                       (recipe_id, recipe_Name, category, ingredients_id))
            super().get_connection.commit()
            print(f"Successfully added {recipe_Name} with id #{recipe_id} under '{category}'.")

        except Exception as e:
            print("An error has occurred:", e)

    # Update function for updating recipe name and category when given recipe id
    def update(self, recipe_id, recipe_Name, category):
        try:
            super().get_cursor.execute("update Recipe set recipe_Name = ?, category = ? where recipe_id = ?;",
                                   (recipe_Name, category, recipe_id))
            super().get_connection.commit()
            print(f"Updated recipe name to {recipe_Name} and category name to {category} successfully")
            return True
        except Exception as e:
            print("An error has occurred:", e)
            return False

    # Delete a recipe from the recipe table using recipe id
    def delete(self, recipe_id):
        try:
            super().get_cursor.execute("DELETE FROM Recipe where recipe_id = ?;", (recipe_id,))
            super().get_connection.commit()
            print(f"Deleted recipe with id #{recipe_id} successfully")
            return True

        except Exception as e:
            print("An error has occurred:", e)
            return False

    # Retrieve function to get recipe details when given recipe id
    def fetch(self, recipe_id = None):
        try:
            if recipe_id is not None:
                return super().get_cursor.execute("SELECT * FROM Recipe WHERE recipe_id = ?",
                                                  (recipe_id,)).fetchone()
            else:
                return super().get_cursor.execute("SELECT * FROM Recipe").fetchall()
        except Exception as e:
            print("An error has occurred:", e)

# Ingredients class inherits from Recipe class
class Ingredients(Recipe):

    # Add function for adding recipe id, ingredient id and ingredients list into the ingredients table
    def add_ing(self, recipe_id, ingred_id, list):
        try:
            super().add(recipe_id)
        except Exception as e:
            print("An error occurred in the recipe class.", e)
        else:
            try:
                ingredient = super().fetch(ingredients_id=ingred_id)[0]
                if ingredient is not None:
                    super().get_cursor.execute("""INSERT INTO INGREDIENTS (recipe_id, ingredients_ID, ingredients)
                    VALUES (?,?,?");""", (recipe_id, ingred_id, list))
                    super().get_connection.commit()
                    print(f"Ingredients for recipe id #{recipe_id} added successfully")
                else:
                    raise Exception("The id of the recipe name was not found")
            except Exception as ex:
                print("An error occurred in the ingredients class.", ex)

    # Update function for updating ingredient list when given ingredients id
    def update_ing(self, ingred_id, list):
        try:
            super().get_cursor.execute("""UPDATE INGREDIENTS SET ingredients = ? WHERE ingredients_ID = ?;""",
                                       (list, ingred_id))
            super().get_connection.commit()
            print(f"Updated the list for ingredients with id #{ingred_id} successfully")
            return True
        except Exception as e:
            print("An error occurred.", e)
            return False

    # Delete a ingredient from the ingredients table using ingredients id
    def delete_ing(self, ingred_id):
        try:
            ingredient = self.fetch_ing(ingred_id)[1]
            if ingredient is not None:
                rsts = super().delete_ing(ingredient)
                super().get_connection.commit()

                if rsts is False:
                    raise Exception("Delete method in Recipe failed. Delete aborted.")

        except Exception as e:
            print("An error occurred.", e)
        else:
            try:
                super().get_cursor.execute("""DELETE FROM INGREDIENTS WHERE id = ?;""", (ingred_id,))
                super().get_connection.commit()
            except Exception as e:
                print("an error occurred in ingredients delete", e)

    # Retrieve function to get all recipe details when given ingredient id
    def fetch_ing(self, id=None):
        try:
            if id is not None:
                retval = super().get_cursor.execute("""SELECT r.recipe_id, recipe_Name, category, 
                INGREDIENTS.ingredients_ID, ingredients
                FROM INGREDIENTS JOIN Recipe r on INGREDIENTS.ingredients_ID = r.ingredients_ID
                WHERE INGREDIENTS.ingredients_ID = ?;""", (id,)).fetchone()
                return retval
            else:
                return super().get_cursor.execute("""SELECT r.recipe_id, recipe_Name, category, 
                INGREDIENTS.ingredients_ID, ingredients
                FROM INGREDIENTS JOIN Recipe r on INGREDIENTS.ingredients_ID = r.ingredients_ID;""").fetchall()
        except Exception as e:
            print("An error occurred.", e)

# Create User class from DBbase
class User(DBbase):

    def __init__(self):
        super().__init__("recipe_manager.sqlite")

    # Add user details (id, name and the user's role) to the user table
    def add_user(self, id, name, user_role):
        try:
            super().get_cursor.execute("insert or ignore into USERS (user_id, name, role) values(?,?,?);",
                                       (id, name, user_role))
            super().get_connection.commit()
            print(f"Successfully added user with the name {name} and id #{id} as a '{user_role}'.")

        except Exception as e:
            print("An error has occurred:", e)

    # Update user details when user id is given, not a part of program so that user information is protected from any user
    # trying to update or change other user's information
    def update_user(self, id, name, role):
        try:
            super().get_cursor.execute("update USERS set name = ?, role = ? where user_id = ?;",
                                   (name, role, id))
            super().get_connection.commit()
            print(f"Updated user name to {name} and role to {role} successfully")
            return True
        except Exception as e:
            print("An error has occurred:", e)
            return False

    # Delete user when given a user id
    def delete_user(self, id):
        try:
            super().get_cursor.execute("DELETE FROM USERS where user_id = ?;", (id,))
            super().get_connection.commit()
            print(f"Deleted user with id #{id} successfully")
            return True

        except Exception as e:
            print("An error has occurred:", e)
            return False

    # Fetch user details when user id is given, not a part of program so that sensitive user information is protected from any user
    # of the program trying to gain access to another user's information
    def fetch_user(self, id = None):
        try:
            if id is not None:
                return super().get_cursor.execute("SELECT * FROM USERS WHERE user_id = ?",
                                                  (id,)).fetchone()
            else:
                print("That id does not exist or you do not have access to that user's information.")
        except Exception as e:
            print("An error has occurred:", e)

if __name__ == "__main__":
    recipe = Recipe()
    recipe.reset_database()

    csv_file = "Recipe_Managers.csv"
    recipe.populate_db_from_csv(csv_file)

# Create class Recipe_Manager to run interactive menu program
class Recipe_Manager:

    def run(self):

        # Create options for user to select from
        inv_options = {"1": "Display all dishes available in recipe book",
                       "2": "Get recipe details using recipe id",
                       "3": "Get all recipe and ingredient details using ingredient id",
                       "4": "Update recipe name and category",
                       "5": "Update ingredients",
                       "6": "Add new recipe and recipe details",
                       "7": "Delete recipe and its ingredients",
                       "8": "Delete ingredients",
                       "9": "Add user",
                       "10": "Delete user",
                       "11": "Reset database",
                       "12": "Exit program"
                       }

        print("Welcome to our recipe manager and creator program, please choose a selection")

        user_selection = ""
        while user_selection != "exit":
            print("*** Option List ***")
            for option in inv_options.items():
                print(option)

            # Allow user to select option or exit the program
            user_selection = input("Select an option or type 'exit' to quit: ").lower()
            recipe = Recipe()
            ingredients = Ingredients()
            user = User()

            # Display menu to user
            if user_selection == "1":
                results = ingredients.fetch_ing()
                for item in results:
                    print(item)
                input("Please press return if you would like to continue the program " )

            # Display recipe details from recipe table to user
            elif user_selection == "2":
                rec_id = input("Enter recipe id to view it's associated name, category and ingredient id: ")
                rec_results = recipe.fetch(rec_id)
                print(rec_results)
                input("Please press return if you would like to continue the program ")

            # Show complete recipe record to user
            elif user_selection == "3":
                inv_id = input("Enter the ingredient id for the recipe you would like to view: ")
                results = ingredients.fetch_ing(inv_id)
                print(results)
                input("Please press return if you would like to continue the program ")

            # Display details of the recipe table and update when given correct recipe id
            elif user_selection == "4":

                results = recipe.fetch()
                for item in results:
                    print(item)

                recipe_id = input("Enter the recipe id of the record you would like to update: ")
                recipe_Name = input("Enter the updated name for your recipe: ")
                category = input("Enter desired category for your updated recipe: ")
                recipe.update(recipe_id, recipe_Name, category)
                print(recipe.fetch(recipe_id))
                input("Please press return if you would like to continue the program ")

            # Display details of the ingredients table and update when given correct ingredient id
            elif user_selection == "5":

                results = ingredients.fetch_ing()
                for item in results:
                    print(item)

                id = input("Enter the id of the ingredients you would like to update: ")
                ingred_list = input("Create a list of the updated ingredients: ")
                ingredients.update_ing(id, ingred_list)
                print(ingredients.fetch_ing(id))
                input("Please press return if you would like to continue the program ")

            # Add a new recipe into the recipe table
            elif user_selection == "6":
                recipe_id = input("Enter an id for your new recipe (make it is a new value unless you want to overwrite an existing record): ")
                recipe_name = input("Enter the name of your new recipe: ")
                recipe_cat = input("Enter desired category for your new recipe: ")
                ingred_id = input("Enter id to be used for ingredients: ")
                recipe.add(recipe_id, recipe_name, recipe_cat, ingred_id)
                print("Done\n")
                input("Please press return if you would like to continue the program ")

            # Delete recipe details when given recipe id only after user confirms they would like to delete the record
            elif user_selection == "7":
                rec_id = input("Enter the recipe id of the recipe you would like to delete: ")
                confirm = input("This will permanently delete the recipe associated with the given id, are you sure you would like to continue? (y/n) ").lower()
                if confirm == "y":
                    recipe.delete(rec_id)
                else:
                    print("Deletion canceled.")
                print("Done!\n")
                input("Please press return if you would like to continue the program")

            # Delete ingredient details when given ingredient id only after user confirms they would like to delete the record
            elif user_selection == "8":
                ing_id = input("Enter the id of the ingredients you would like to delete: ")
                confirm = input("This will permanently delete the ingredient list associated with the given id, are you sure you would like to continue? (y/n) ").lower()
                if confirm == "y":
                    ingredients.delete_ing(ing_id)
                else:
                    print("Deletion canceled.")
                print("Done!\n")
                input("Please press return if you would like to continue the program")

            # Allow addition of new user into user table
            elif user_selection == "9":
                user_id = input("Enter an id for the new user: ")
                user_name = input("Enter name of the new user: ")
                role = input("Enter a role for the new user: ")
                user.add_user(user_id, user_name, role)
                print("Done\n")
                input("Please press return if you would like to continue the program ")

            # Allow deletion of user from user table
            elif user_selection == "10":
                user_id = input("Enter the id of the user you would like to remove from the database: ")
                confirm = input("This will permanently delete the user associated with the given id, are you sure you would like to continue? (y/n) ").lower()
                if confirm == "y":
                    user.delete_user(user_id)
                else:
                    print("Deletion canceled.")
                print("Done!\n")
                input("Please press return if you would like to continue the program")

            # Allow user to reset database after confirming this is the option they intended to select from the menu
            # or else the reset is terminated and the program is continued
            elif user_selection == "11":
                confirm = input("This will reset all records in recipes and ingredients, are you sure you would like to continue? (y/n) ").lower()
                if confirm == "y":
                    recipe.reset_database()
                    Recipes = recipe
                    Recipes.reset_database()
                    print("Reset complete")
                    input("Press return to continue")
                else:
                    print("Reset aborted")
                    input("Please press return if you would like to continue the program")

            # Allow the user to exit the program after confirming that is the action they want to take else continue program
            # If yes is selected, this closes the database and ends the program
            elif user_selection == "12":
                exit_confirm = input("Are you sure you want to exit the program? Confirm by typing 'yes' or press any other key to return to recipe manager program: ").lower()
                if exit_confirm == "yes":
                    print("Thank you for using the recipe manager program! We hope to assist you next time you want to manage your cookbook!")
                    print("The database will close now and the program will end")
                    recipe.close_db()
                    sys.exit()
                else:
                    print("Continuing program...")
                    input("Please press return if you would like to continue the program")

            else:
                if user_selection != "exit":
                    print("Invalid selection, please try again\n")

# Run interactive menu
recipe_manager = Recipe_Manager()
recipe_manager.run()
