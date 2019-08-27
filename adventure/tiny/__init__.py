import check50
import pkg_resources
import shutil
import os
if int(pkg_resources.get_distribution("check50").version[0]) < 3:
    raise ImportError("This check requires check50 version 3.0.0 or above.")

run_command = "python3 adventure.py"

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


def init(game):
    check50.include("../data")
    for other_game in {"Crowther", "Tiny", "Small"} - {game}:
        for items in ["Rooms", "Items"]:
            shutil.copyfile(f"data/{game}{items}.txt", f"data/{other_game}{items}.txt")


@check50.check()
def exists():
    """Checking if all files exist."""
    init("Tiny")
    check50.exists("adventure.py")
    check50.exists("room.py")


@check50.check(exists)
def move_once():
    """Starting Adventure then moving once to the WEST."""
    try:
        check50.run(run_command).stdout(room_1_description, regex=False)
    except check50.Failure as error:
        raise check50.Failure(f"Expected the description of initial "
                              f"room when Adventure starts.\n    {error}")
    check50.run(run_command).stdin("WEST").stdout(room_2_description,
                                                  regex=False)


@check50.check(move_once)
def move_invalid():
    """Attempt to move EAST into an unconnected room."""
    check50.run(run_command).stdin("EAST").stdout("Invalid command")


@check50.check(move_once)
def move_repeatedly():
    """Moving WEST, EAST, WEST in succession."""
    check = check50.run(run_command)
    check.stdin("WEST").stdout(room_2_description, regex=False)
    check.stdin("EAST").stdout(room_1_name, regex=False)
    check.stdin("WEST").stdout(room_2_name, regex=False)


@check50.check(move_repeatedly)
def move_mixed_case():
    """Move with mixed case command."""
    check50.run(run_command).stdin("west").stdout(room_2_description,
                                                  regex=False)
    check50.run(run_command).stdin("wESt").stdout(room_2_description,
                                                  regex=False)
    check50.run(run_command).stdin("west").stdin("EAST").stdout(room_1_name,
                                                                regex=False)


@check50.check(move_mixed_case)
def helper_commands():
    """Testing helper commands; HELP, LOOK, QUIT."""
    # Test HELP
    try:
        check = check50.run(run_command).stdin("HELP")
        for help in help_statement:
            check.stdout(help)
    except check50.Failure as error:
        raise check50.Failure(f"HELP did not print the expected message.\n"
                              f"    {error}")

    # Test LOOK command
    try:
        check50.run(run_command).stdin("LOOK").stdout(room_1_description,
                                                      regex=False)
        check50.run(run_command).stdin("look").stdout(room_1_description,
                                                      regex=False)
    except check50.Failure as error:
        raise check50.Failure(f"LOOK/look did not print the expected room"
                              f"description.\n    {error}")

    # Test QUIT
    try:
        check50.run(run_command).stdin("QUIT").stdout("Thanks for playing!",
                                                      regex=False).exit(0)
    except check50.Failure as error:
        raise check50.Failure(f"QUIT did not function as expected.\n"
                              f"    {error}")


@check50.check(helper_commands)
def commands():
    """Test if program handles invalid commands."""
    # Check invalid command
    check = check50.run(run_command).stdin("cs50")
    check.stdout("Invalid command", regex=False)


@check50.check(helper_commands)
def find_items():
    """Finds items in rooms."""
    check50.exists("item.py")
    # Check initial description
    try:
        check = check50.run(run_command).stdin("in")
        check.stdout(room_3_description, regex=False)

        for item in room_3_items:
            check.stdout(item, regex=False)
    except check50.Failure as error:
        raise check50.Failure(f"Could not find items upon first entering room.\n"
                              f"    Remember to seperate multiple items by a "
                              f"single newline.\n"
                              f"    {error}")

    # Check for look command
    try:
        check = check50.run(run_command)
        moves = ["IN", "OUT", "IN", "LOOK"]

        for move in moves:
            check.stdout("> ")
            check.stdin(move, prompt=False)

        for item in room_3_items:
            check.stdout(item, regex=False)
    except check50.Failure as error:
        raise check50.Failure(f"Could not find items when using LOOK.\n"
                              f"    {error}")


@check50.check(find_items)
def handle_items():
    """Take and drop items."""
    check50.exists("inventory.py")
    # Take keys check
    check = check50.run(run_command)
    moves = ["IN", "TAKE keys"]

    for move in moves:
        check.stdout("> ")
        check.stdin(move, prompt=False)

    check.stdout("KEYS taken", regex=False)

    # Drop keys check then look for dropped keys check
    check = check50.run(run_command)
    moves = ["IN", "TAKE keys", "OUT", "DROP keys"]

    for move in moves:
        check.stdout("> ")
        check.stdin(move, prompt=False)

    check.stdout("KEYS dropped", regex=False)
    check.stdin("look").stdout("KEYS", regex=False)
    check.stdout("a set of keys", regex=False)


@check50.check(handle_items)
def handle_invalid_items():
    """Take and drop nonexistent items."""
    # Take a non-existent item.
    check = check50.run(run_command).stdin("TAKE kes")
    check.stdout(no_item, regex=False)

    # Take an item twice.
    check = check50.run(run_command)
    moves = ["IN", "TAKE keys", "TAKE keys"]

    for move in moves:
        check.stdout("> ")
        check.stdin(move, prompt=False)
    check.stdout(no_item, regex=False)

    # Drop non-existent item.
    check = check50.run(run_command).stdin("DROP something")
    check.stdout(no_item, regex=False)


@check50.check(handle_items)
def inventory():
    """Using the INVENTORY command."""
    # Check empty inventory.
    try:
        check = check50.run(run_command).stdin("INVENTORY")
        check.stdout("Your inventory is empty", regex=False)
    except check50.Failure as error:
        raise check50.Failure(f"Let the player know they have no items.\n"
                              f"    {error}")

    # Check having keys.
    check = check50.run(run_command)
    moves = ["IN", "TAKE keys", "INVENTORY"]

    for move in moves:
        check.stdout("> ")
        check.stdin(move, prompt=False)

    check.stdout("KEYS", regex=False)
    check.stdout("a set of keys", regex=False)
