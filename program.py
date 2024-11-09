"""Program code"""

# System Imports
import os

# Internal imports.
from beverage import BeverageRepository
from errors import AlreadyImportedError
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
            # Load the CSV File
            try:
                # Check to see if there are any records in the DB
                # If not, use CSV to load up Employees. Then put in DB.
                if beverage_repository.db_status() is None:
                                
                    # Call the import_csv method sending in our path to the csv and the Employee list.
                    csv_processor.import_csv(PATH_TO_CSV, beverage_repository)

                    # Populate the database with data from the CSV
                    csv_processor.populate_database(beverage_repository)

                # If we do not have the database, we can create it.
                if not os.path.exists("./db.sqlite3"):
                    # Create the database
                    beverage_repository.create_database()
                    csv_processor.import_csv(beverage_repository, PATH_TO_CSV)
                    ui.display_import_success()
            except AlreadyImportedError:
                ui.display_already_imported_error()
            except FileNotFoundError:
                ui.display_file_not_found_error()
            except EOFError:
                ui.display_empty_file_error()

        elif choice == 2:
            # Print Entire List Of Items
            all_item_string = str(beverage_repository)
            if all_item_string:
                ui.display_all_items(all_item_string)
            else:
                ui.display_all_items_error()

        elif choice == 3:
            # Search for an Item by it's id
            search_query = ui.get_search_query()
            item_info = beverage_repository.find_by_id(search_query)
            if item_info:
                # beverage_by_id = session.query(Employee).get(1)
                ui.display_item_found(item_info)
            else:
                ui.display_item_found_error()

        elif choice == 4:
            # Collect information for a new item and insert it into the database
            new_item_info = ui.get_new_item_information()
            if beverage_repository.find_by_id(new_item_info[0]) is None:
                beverage_repository.insert(
                    new_item_info[0],
                    new_item_info[1],
                    new_item_info[2],
                    float(new_item_info[3]),
                    new_item_info[4] == "True",
                )
                ui.display_add_beverage_success()
            else:
                ui.display_beverage_already_exists_error()
        
        elif choice == 5:
            # Update existing beverage
            new_item_info = ui.get_new_item_information()
            if beverage_repository.find_by_id(new_item_info[0]) is not None:
                beverage_repository.update(new_item_info)
                ui.display_update_beverage_success()
            else:
                ui.display_beverage_update_error()

        elif choice == 6:
            # Delete existing beverage
            new_item_info = ui.get_new_item_information()
            if beverage_repository.find_by_id(new_item_info[0]) is not None:
                beverage_repository.delete(new_item_info)
                ui.display_delete_beverage_success()
            else:
                ui.display_item_found_error()

        # Get the new choice of what to do from the user.
        choice = ui.display_menu_and_get_response()
