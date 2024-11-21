"""Program code"""

# System Imports
import os

# Internal imports.
from beverage import BeverageRepository
from errors import AlreadyImportedError, DatabaseImportError
from user_interface import UserInterface
from utils import CSVProcessor

# Set a constant for the path to the CSV file
PATH_TO_CSV = "./datafiles/beverage_list.csv"

def main(*args):
    """Method to run program"""

    # Create an instance of User Interface class
    ui = UserInterface()

    # Create an instance of the BeverageRepository class.
    beverage_repository = BeverageRepository()

    # Create an instance of the CSVProcessor class.
    csv_processor = CSVProcessor()

    # Display the Welcome Message to the user.
    ui.display_welcome_greeting()

    # Display the Menu and get the response. Store the response in the choice
    # integer. This is the 'primer' run of displaying and getting.
    choice = ui.display_menu_and_get_response()

    # While the choice is not exit program
    while choice != 7:
        if choice == 1:
            # Load the CSV File, populates the database
            try:
                # If we do not have the database, we can create it.
                if not os.path.exists("./db.sqlite3"):
                    
                    # Create the database
                    beverage_repository.create_database()
                else:
                    raise DatabaseImportError

                # Check to see if there are any records in the DB
                # If not, use CSV to load up Beverages. Then put in DB.
                if beverage_repository.db_status() is None:
                                
                    # Call the import_csv method sending in our path to the csv and the Employee list.
                    csv_processor.import_csv(PATH_TO_CSV, beverage_repository)

                    # Populate the database with data from the CSV
                    beverage_repository.populate_database()

                    # Displays import success message
                    ui.display_import_success()
            except AlreadyImportedError:
                ui.display_already_imported_error()
            except DatabaseImportError:
                ui.display_database_import_error()
            except FileNotFoundError:
                ui.display_file_not_found_error()
            except EOFError:
                ui.display_empty_file_error()

        elif choice == 2:
            # Print Entire List Of Beverages
            all_beverage_string = str(beverage_repository)
            if all_beverage_string:
                ui.display_all_beverages(all_beverage_string)
            else:
                ui.display_all_beverages_error()

        elif choice == 3:
            # Search for an Beverage by it's id in the database
            search_query = ui.get_search_query()
            beverage_by_id = beverage_repository.query_by_id(search_query)
            if beverage_by_id:
                ui.display_beverage_found(beverage_by_id)
            else:
                ui.display_beverage_found_error()

        elif choice == 4:
            # Collect information for a new beverage and insert it into the database
            new_beverage_info = ui.get_new_beverage_information()
            if beverage_repository.query_by_id(new_beverage_info[0]) is None:
                beverage_repository.insert(
                    new_beverage_info[0],
                    new_beverage_info[1],
                    new_beverage_info[2],
                    float(new_beverage_info[3]),
                    new_beverage_info[4] == "True",
                )
                ui.display_add_beverage_success()
            else:
                ui.display_beverage_already_exists_error()
        
        elif choice == 5:
            # Update existing beverage
            search_query = ui.get_search_query()
            # If the item does exist
            if beverage_repository.query_by_id(search_query) is not None:
                new_beverage_info = ui.get_updated_information()

                # Checks updated price
                updated_price = new_beverage_info[2]
                if updated_price is not None:
                    updated_price = float(updated_price)
                # Checks updated active
                updated_active = new_beverage_info[3]
                if updated_active is not None:
                    updated_active = updated_active == "True"

                beverage_repository.update(
                    search_query, 
                    new_beverage_info[0],
                    new_beverage_info[1],
                    updated_price,
                    updated_active
                    )
                
                ui.display_update_beverage_success()
            else:
                ui.display_beverage_update_error()

        elif choice == 6:
            # Delete existing beverage
            search_query = ui.get_search_query()
            if beverage_repository.query_by_id(search_query) is not None:
                beverage_repository.delete(search_query)
                ui.display_delete_beverage_success()
            else:
                ui.display_beverage_found_error()

        # Get the new choice of what to do from the user.
        choice = ui.display_menu_and_get_response()
