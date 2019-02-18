import re
import os

from check50 import *
import check50

room_1_name = "Outside building"
room_1_description = ("You are standing at the end of a road before a "
                      "small brick building.  A small stream flows out of "
                      "the building and down a gully to the south.  A road "
                      "runs up a small hill to the west.")

room_2_name = "End of road"
room_2_description = ("You are at the end of a road at the top of a small "
                      "hill. You can see a small building in the valley to "
                      "the east.")

room_3_name = "Inside building"
room_3_description = ("You are inside a building, a well house for a large "
                      "spring.")
room_3_items = ["KEYS", "a set of keys"]

room_8_name = "Beneath grate"
room_8_description = ("You are in a small chamber beneath a 3x3 steel "
                      "grate to the surface.  A low crawl over cobbles "
                      "leads inward to the west.")
room_8_items = ["LAMP", "a brightly shining brass lamp"]

room_14_description = ("You are in a splendid chamber thirty feet high.  "
                       "The walls are frozen rivers of orange stone.  A narrow "
                       "canyon and a good passage exit from east and west "
                       "sides of the chamber.")
room_15_description = ("You are in a splendid chamber thirty feet high.  "
                       "The walls are frozen rivers of orange stone.  A narrow "
                       "canyon and a good passage exit from east and west "
                       "sides of the chamber. High in the cavern, you see a "
                       "little bird flying around the rocks.  It takes one "
                       "look at the black rod and quickly flies out of sight.")

help_statement = ["EAST/WEST/IN/OUT", "QUIT quits", "HELP prints",
                  "INVENTORY lists", "LOOK lists", "TAKE <item>", "DROP <item>"]
no_item = "No such item"


class Adventure(Checks):
    def tiny_spawn(self):
        return self.spawn("python3 adventure.py tiny")

    def small_spawn(self):
        return self.spawn("python3 adventure.py small")

    @check()
    def exists(self):
        """Checking if all files exist."""
        self.require("adventure.py", "room.py")

        # self.add can't create directories :(
        # give v3 pls
        cwd = os.getcwd()
        dest = os.path.join(cwd, "data")
        os.mkdir(dest)
        with check50.cd(check50.config.check_dir):
            data_files = [os.path.join("data", data_file) for data_file in os.listdir("data")]
            for path in data_files:
                check50.copy(path, dest)


    @check("exists")
    def move_once(self):
        """Starting Adventure then moving once to the WEST."""
        try:
            self.tiny_spawn().stdout(re.escape(room_1_description), str_output=room_1_description)
        except Error as error:
            raise Error(rationale=f"Expected the description of initial "
                                  f"room when Adventure starts.\n    {error}")

        self.tiny_spawn().stdin("WEST").stdout(re.escape(room_2_description), str_output=room_2_description)


    @check("move_once")
    def move_invalid(self):
        """Attempt to move EAST into an unconnected room."""
        self.tiny_spawn().stdin("EAST").stdout("Invalid command")


    @check("move_once")
    def move_repeatedly(self):
        """Moving WEST, EAST, WEST in succession."""
        check = self.tiny_spawn()
        check.stdin("WEST").stdout(re.escape(room_2_description), str_output=room_2_description)
        check.stdin("EAST").stdout(re.escape(room_1_name), str_output=room_1_name)
        check.stdin("WEST").stdout(re.escape(room_2_name), str_output=room_2_name)


    @check("move_repeatedly")
    def move_mixed_case(self):
        """Move with mixed case command."""
        self.tiny_spawn().stdin("west").stdout(re.escape(room_2_description), str_output=room_2_description)
        self.tiny_spawn().stdin("wESt").stdout(re.escape(room_2_description), str_output=room_2_description)
        self.tiny_spawn().stdin("west").stdin("EAST").stdout(re.escape(room_1_name), str_output=room_1_name)


    @check("move_mixed_case")
    def helper_commands(self):
        """Testing helper commands; HELP, LOOK, QUIT."""
        # Test HELP
        try:
            check = self.tiny_spawn().stdin("HELP")
            for help in help_statement:
                check.stdout(help)
        except Error as error:
            raise Error(rationale=f"HELP did not print the expected message.\n"
                                  f"    {error}")

        # Test LOOK command
        try:
            self.tiny_spawn().stdin("LOOK").stdout(re.escape(room_1_description), str_output=room_1_description)
            self.tiny_spawn().stdin("look").stdout(re.escape(room_1_description), str_output=room_1_description)
        except Error as error:
            raise Error(rationale=f"LOOK/look did not print the expected room"
                                  f"description.\n    {error}")

        # Test QUIT
        try:
            self.tiny_spawn().stdin("QUIT").stdout(re.escape("Thanks for playing!"), str_output="Thanks for playing!").exit(0)
        except Error as error:
            raise Error(rationale=f"QUIT did not function as expected.\n"
                                  f"    {error}")


    @check("helper_commands")
    def commands(self):
        """Test if program handles invalid commands."""
        # Check invalid command
        check = self.tiny_spawn().stdin("cs50")
        check.stdout(re.escape("Invalid command"), str_output="Invalid command")


    @check("helper_commands")
    def find_items(self):
        """Finds items in rooms."""
        self.require("item.py")

        # Check initial description
        try:
            check = self.tiny_spawn().stdin("in")
            check.stdout(re.escape(room_3_description), str_output=room_3_description)

            for item in room_3_items:
                check.stdout(re.escape(item), str_output=item)
        except Error as error:
            raise Error(rationale=f"Could not find items upon first entering room.\n"
                                  f"    Remember to seperate multiple items by a "
                                  f"single newline.\n"
                                  f"    {error}")

        # Check for look command
        try:
            check = self.tiny_spawn()
            moves = ["IN", "OUT", "IN", "LOOK"]

            for move in moves:
                check.stdout("> ")
                check.stdin(move, prompt=False)

            for item in room_3_items:
                check.stdout(re.escape(item), str_output=item)
        except Error as error:
            raise Error(rationale=f"Could not find items when using LOOK.\n"
                                  f"    {error}")


    @check("find_items")
    def handle_items(self):
        """Take and drop items."""
        self.require("inventory.py")

        # Take keys check
        check = self.tiny_spawn()
        moves = ["IN", "TAKE keys"]

        for move in moves:
            check.stdout("> ")
            check.stdin(move, prompt=False)

        check.stdout(re.escape("KEYS taken"), str_output="KEYS taken")

        # Drop keys check then look for dropped keys check
        check = self.tiny_spawn()
        moves = ["IN", "TAKE keys", "OUT", "DROP keys"]

        for move in moves:
            check.stdout("> ")
            check.stdin(move, prompt=False)

        check.stdout(re.escape("KEYS dropped"), str_output="KEYS dropped")
        check.stdin("look").stdout(re.escape("KEYS"), str_output="KEYS")
        check.stdout(re.escape("a set of keys"), str_output="a set of keys")


    @check("handle_items")
    def handle_invalid_items(self):
        """Take and drop nonexistent items."""
        # Take a non-existent item.
        check = self.tiny_spawn().stdin("TAKE kes")
        check.stdout(re.escape(no_item), str_output=no_item)

        # Take an item twice.
        check = self.tiny_spawn()
        moves = ["IN", "TAKE keys", "TAKE keys"]

        for move in moves:
            check.stdout("> ")
            check.stdin(move, prompt=False)
        check.stdout(re.escape(no_item), str_output=no_item)

        # Drop non-existent item.
        check = self.tiny_spawn().stdin("DROP something")
        check.stdout(re.escape(no_item), str_output=no_item)


    @check("handle_items")
    def inventory(self):
        """Using the INVENTORY command."""
        # Check empty inventory.
        try:
            check = self.tiny_spawn().stdin("INVENTORY")
            check.stdout(re.escape("Your inventory is empty"), str_output="Your inventory is empty")
        except Error as error:
            raise Error(rationale=f"Let the player know they have no items.\n"
                                  f"    {error}")

        # Check having keys.
        check = self.tiny_spawn()
        moves = ["IN", "TAKE keys", "INVENTORY"]

        for move in moves:
            check.stdout("> ")
            check.stdin(move, prompt=False)

        check.stdout(re.escape("KEYS"), str_output="KEYS")
        check.stdout(re.escape("a set of keys"), str_output="KEYS")


    @check("handle_items")
    def conditional_move(self):
        """Check if holding an item affects conditional movement."""
        check = self.small_spawn()
        moves = ["DOWN", "DOWN", "DOWN", "DOWN"]

        for move in moves:
            check.stdout("> ")
            check.stdin(move, prompt=False)

        check.stdout(re.escape("The grate is locked and you don't have any keys."),
                     str_output="The grate is locked and you don't have any keys.")

        check = self.small_spawn()
        moves = ["IN", "TAKE keys", "OUT",
                 "DOWN", "DOWN", "DOWN", "DOWN"
                 ]

        for move in moves:
            check.stdout("> ")
            check.stdin(move, prompt=False)

        check.stdout(re.escape(room_8_description), str_output=room_8_description)
        for item in room_8_items:
            check.stdout(re.escape(item), str_output=item)


    @check("conditional_move")
    def forced_move(self):
        """Checking if FORCED immediately moves the player."""
        check = self.small_spawn()
        moves = ["DOWN", "DOWN", "DOWN", "DOWN"]

        for move in moves:
            check.stdout("> ")
            check.stdin(move, prompt=False)

        check.stdout(re.escape("The grate is locked and you don't have any keys."),
                     str_output="The grate is locked and you don't have any keys.")
        check.stdout(re.escape("Outside grate"), str_output="Outside grate")
