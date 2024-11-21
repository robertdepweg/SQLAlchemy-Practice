"""User Interface module"""

# System imports.
import os

# First-party imports
from colors import (
    print_error,
    print_info,
    print_success,
    print_warning,
)


class UserInterface:
    """UserInterface class"""

    MAX_MENU_CHOICES = 7

    # region public methods

    def display_welcome_greeting(self):
        """Display Welcome Greeting."""
        print_info("Welcome to the beverage program")

    def display_menu_and_get_response(self):
        """Display Menu and get response."""

        # Display menu and prompt
        self.__display_menu()
        self.__display_main_prompt()

        # Get the selection they enter
        selection = self.__get_selection()

        # While the response is not valid.
        while not self.__verify_selection_valid(selection):
            # Display error message.
            self.__display_error_message()
            # Display prompt again.
            self.__display_main_prompt()
            # Get selection again.
            selection = self.__get_selection()

        # Return the selection casted to an int
        return int(selection)

    def get_search_query(self):
        """Get the search query from the user."""
        print()
        print("What ID would you like to search for?")
        self.__display_prompt()
        return input()

    def get_new_beverage_information(self):
        """Get new Beverage information from the user."""
        return (
            self.__get_str_field("Id"),
            self.__get_str_field("Name"),
            self.__get_str_field("Pack"),
            self.__get_decimal_field("Price"),
            self.__get_bool_field("Active"),
        )
    
    def get_updated_information(self):
        """Get updated information from the user"""

        # Defaults if they aren't chosen
        name = None
        pack = None
        price = None
        active = None

        # Asks user for each field's information
        # Asks for name
        response = self.__get_bool_field("Name", "Do you want to update the beverage's name? (y/n)")
        if response == "True":
            price = self.__get_str_field("Name")
        # Asks for pack
        response = self.__get_bool_field("Pack", "Do you want to update the beverage's pack? (y/n)")
        if response == "True":
            price = self.__get_str_field("Pack")
        # Asks for price
        response = self.__get_bool_field("Price", "Do you want to update the beverage's price? (y/n)")
        if response == "True":
            price = self.__get_str_field("Price")
        # Asks for availability
        response = self.__get_bool_field("Active", "Do you want to update the beverage's availability? (y/n)")
        if response == "True":
            active = self.__get_bool_field("Active")

        return (
            name,
            pack,
            price,
            active
        )

    def display_import_success(self):
        """Display import success."""
        print()
        print_success("Beverage list has been imported successfully.")

    def display_import_error(self):
        """Display import error."""
        print()
        print_error("There was an error importing the CSV file.")

    def display_already_imported_error(self):
        """Display already imported error"""
        self.display_import_error()
        print_error("The CSV file has already been imported into the database.")

    def display_database_import_error(self):
        """Display database import error"""
        self.display_import_error()
        print_error("The database already exists.")

    def display_file_not_found_error(self):
        """Display file not found error"""
        self.display_import_error()
        print_error("File not found for opening.")

    def display_empty_file_error(self):
        """Display empty file error"""
        self.display_import_error()
        print_error("The file was unexpectedly empty.")

    def display_all_beverages(self, all_beverages_output):
        """Display all Beverages."""
        print()
        print_success("Printing list")
        print()
        print_warning(self.__get_beverage_header())
        print(all_beverages_output, end="")
        print(self.__get_line_separator())

    def display_all_beverages_error(self):
        """Display all Beverages error."""
        print()
        print_error("There are no beverages in the list to print.")

    def display_beverage_found(self, beverage_information):
        """Display Beverage found success."""
        print()
        print_success("Beverage Found!")
        print()
        print_warning(self.__get_beverage_header())
        print(beverage_information)
        print(self.__get_line_separator())

    def display_beverage_found_error(self):
        """Display Beverage found error."""
        print()
        print_error("Could not find a beverage with that id.")

    def display_add_beverage_success(self):
        """Display Add Beverage success."""
        print()
        print_success("The beverage was successfully added to the database.")

    def display_beverage_already_exists_error(self):
        """Display Beverage already exists error."""
        print()
        print_error("Unable to add. A Beverage with that id already exists in the database.")

    def display_update_beverage_success(self):
        """Display Beverage update success message."""
        print()
        print_success("The beverage's information was successfully updated.")

    def display_beverage_update_error(self):
        """Display Beverage update error."""
        print()
        print_error("Could not find a beverage to be updated with that id.")
    
    def display_delete_beverage_success(self):
        """Display Beverage deletion success message."""
        print()
        print_success("The beverage was successfully deleted from the database.")

    # endregion public methods

    # region private methods

    def __display_prompt(self):
        """Display the prompt"""
        print("> ", end="")

    def __display_menu(self):
        """Display the Menu"""
        print()
        print("What would you like to do?")
        print()
        print("1. Load Beverage List From CSV")
        print("2. Print Entire Beverage Database")
        print("3. Search For A Beverage")
        print("4. Add New Beverage To The Database")
        print("5. Update an existing Beverage")
        print("6. Delete an existing Beverage")
        print("7. Exit Program")

    def __display_main_prompt(self):
        """Display the Prompt"""
        print()
        print("Enter Your Choice:")
        self.__display_prompt()

    def __display_error_message(self):
        """Display error message."""
        print()
        print_error("That is not a valid option. Please make a valid choice")

    def __get_line_separator(self):
        """Display a line separator"""
        line_str = "-"
        return f"+{line_str*8}+{line_str*58}+{line_str*17}+{line_str*8}+{line_str*8}+"

    def __get_beverage_header(self):
        """Display the Beverage header."""
        id_str = "Id"
        name_str = "Name"
        pack_str = "Pack"
        price_str = "Price"
        active_str = "Active"

        header = f"| {id_str:>6} | {name_str:<56} | {pack_str:<15} | {price_str:>6} | {active_str:<6} |"
        lines = self.__get_line_separator()
        return f"{lines}{os.linesep}{header}{os.linesep}{lines}"

    def __get_selection(self):
        """Get the selection from the user."""
        return input()

    def __verify_selection_valid(self, selection):
        """Verify that a selection from the main menu is valid."""

        # Declare a return value variable and init to False
        return_value = False

        try:
            # Parse the selection into a choice var
            choice = int(selection)

            # If the choice is between 0 and the MAX_MENU_CHOICES
            if choice > 0 and choice <= self.MAX_MENU_CHOICES:
                # Set the return value to True
                return_value = True
        # If not a valid int, this exception will get raised.
        except ValueError:
            # Ensure return value is False. Should not need this.
            return_value = False

        # Return the return_value
        return return_value

    def __get_str_field(self, field_name):
        """Get a valid string field from the console."""
        print(f"What is the new Beverage's {field_name}?")
        self.__display_prompt()
        valid = False
        while not valid:
            value = input()
            if value:
                valid = True
            else:
                print_error("You must provide a value.")
                print()
                print(f"What is the new Beverage's {field_name}?")
                self.__display_prompt()
        return str(value)

    def __get_decimal_field(self, field_name):
        """Get a valid Decimal field from the console."""
        print(f"What is the new Beverage's {field_name}?")
        self.__display_prompt()
        valid = False
        while not valid:
            try:
                value = float(input())
                valid = True
            except ValueError:
                print_error("That is not a valid Decimal. Please enter a valid Decimal.")
                print()
                print(f"What is the new Beverage's {field_name}?")
                self.__display_prompt()
        return str(value)

    def __get_bool_field(self, fieldname, message=None):
        """Get a valid Bool field from the console."""
        if message is None:
            message = f"Should the Beverage be {fieldname}? (y/n)"
        print(message)
        self.__display_prompt()
        valid = False
        while not valid:
            user_input = input()
            if user_input.lower() == "y" or user_input.lower() == "n":
                valid = True
                value = user_input.lower() == "y"
            else:
                print_error("That is not a valid Entry.")
                print()
                print(f"Should the Beverage be {fieldname}? (y/n)")
                self.__display_prompt()

        return str(value)

    # endregion private methods
