import check50

# Template for checks:
'''

@check50.check()
def test_name():
    """Test message."""
    check50.run(run_command)

'''

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
                      "spring. The exit door is to the south.  There is "
                      "another room to the north, but the door is barred by "
                      "a shimmering curtain.")
room_3_items = ["KEYS", "a set of keys", "WATER", "a bottle of water"]

room_8_name = "Beneath grate"
room_8_description = ("You are in a small chamber beneath a 3x3 steel "
                      "grate to the surface.  A low crawl over cobbles "
                      "leads inward to the west.")
room_8_items = "LAMP: a brightly shining brass lamp"

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


@check50.check()
def exists():
    """Checking if all files exist."""
    check50.include("data")
    check50.exists("adventure.py")
    check50.exists("room.py")
    check50.exists("inventory.py")
    check50.exists("item.py")


@check50.check(exists)
def move_once():
    """Starting Adventure then moving once to the WEST."""
    try:
        check50.run(run_command).stdout(room_1_description, regex=False)
    except check50.Failure as error:
        raise check50.Failure(f"Expected the description of initial "
                              "room when Adventure starts.\n    {error}")
    check50.run(run_command).stdin("WEST").stdout(room_2_description,
                                                  regex=False)


@check50.check(exists)
def move_invalid():
    """Attempt an invalid move."""
    check50.run(run_command).stdin("EAST").stdout("Invalid command.")


@check50.check(move_once)
def move_repeatedly():
    """Moving WEST then EAST in succession."""
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
                              "    {error}")

    # Test LOOK command
    try:
        check50.run(run_command).stdin("LOOK").stdout(room_1_description,
                                                      regex=False)
        check50.run(run_command).stdin("look").stdout(room_1_description,
                                                      regex=False)
    except check50.Failure as error:
        raise check50.Failure(f"LOOK/look did not print the expected room"
                              "description.\n    {error}")

    # Test QUIT
    try:
        check50.run(run_command).stdin("QUIT").stdout("Thanks for playing!",
                                                      regex=False).exit(0)
    except check50.Failure as error:
        raise check50.Failure(f"QUIT did not function as expected.\n"
                              "    {error}")


@check50.check(helper_commands)
def commands():
    """Test if program accepts user commands and abbreviations."""
    # Check invalid command
    check = check50.run(run_command).stdin("cs50")
    check.stdout("Invalid command.", regex=False)

    # Check for upper case abreviation
    try:
        check = check50.run(run_command).stdin("W")
        check.stdout(room_2_description, regex=False)
    except check50.Failure as error:
        raise check50.Failure(f"Could not use abbreviation 'w' to move")

    # Check for lower case abbreviation
    try:
        check = check50.run(run_command).stdin("w")
        check.stdout(room_2_description, regex=False)
    except check50.Failure as error:
        raise check50.Failure(f"Could not use abbreviation 'w' to move")


@check50.check(helper_commands)
def find_items():
    """Finds items in rooms."""
    # Check initial description
    try:
        check = check50.run(run_command).stdin("in")
        check.stdout(room_3_description, regex=False)

        for item in room_3_items:
            check.stdout(item, regex=False)
    except check50.Failure as error:
        raise check50.Failure("Could not find items upon first entering room.\n"
                              "    Remember to seperate multiple items by a "
                              "single newline\n"
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
        raise check50.Failure("Could not find items when using LOOK.\n"
                              f"    {error}")


@check50.check(find_items)
def handle_items():
    """Take and drop items."""
    # Take keys check
    check = check50.run(run_command)
    moves = ["IN", "TAKE keys"]

    for move in moves:
        check.stdout("> ")
        check.stdin(move, prompt=False)

    check.stdout("KEYS taken.")

    # Drop keys check then look for dropped keys check
    check = check50.run(run_command)
    moves = ["IN", "TAKE keys", "OUT", "DROP keys"]

    for move in moves:
        check.stdout("> ")
        check.stdin(move, prompt=False)

    check.stdout("KEYS dropped.", regex=False)
    check.stdin("look").stdout("KEYS: a set of keys\n")


@check50.check(handle_items)
def handle_invalid_items():
    """Take and drop nonexistand items."""
    check = check50.run(run_command).stdin("TAKE kes")
    check.stdout("No such item.", regex=False)

    check = check50.run(run_command)
    moves = ["IN", "TAKE keys", "TAKE keys"]

    for move in moves:
        check.stdout("> ")
        check.stdin(move, prompt=False)
    check.stdout("No such item.", regex=False)

    check = check50.run(run_command).stdin("DROP something")
    check.stdout("No such item.", regex=False)


@check50.check(handle_items)
def inventory():
    """Using the INVENTORY command."""
    try:
        check = check50.run(run_command).stdin("INVENTORY")
        check.stdout("Your inventory is empty.", regex=False)
    except check50.Failure as error:
        raise check50.Failure(f"Let the player know they have no items.\n"
                              "    {error}")

    check = check50.run(run_command)
    moves = ["IN", "TAKE keys", "INVENTORY"]

    for move in moves:
        check.stdout("> ")
        check.stdin(move, prompt=False)

    check.stdout("KEYS: a set of keys")


@check50.check(handle_items)
def conditional_move():
    """Check if holding an item affects conditional movement."""
    check = check50.run(run_command)
    moves = ["DOWN", "DOWN", "DOWN", "DOWN"]

    for move in moves:
        check.stdout("> ")
        check.stdin(move, prompt=False)

    check.stdout("The grate is locked and you don't have any keys.",
                 regex=False)

    check = check50.run(run_command)
    moves = ["IN", "TAKE keys", "OUT",
             "DOWN", "DOWN", "DOWN", "DOWN"
             ]

    for move in moves:
        check.stdout("> ")
        check.stdin(move, prompt=False)

    check.stdout(room_8_description, regex=False)
    check.stdout(room_8_items, regex=False)

    # Check for move with multiple conditions.
    try:
        check = check50.run(run_command)
        moves = ["IN", "TAKE KEYS", "OUT", "DOWN", "DOWN",
                 "DOWN", "DOWN", "TAKE LAMP", "IN", "WEST",
                 "WEST", "WEST", "TAKE BIRD", "WEST", "DOWN",
                 "SOUTH", "TAKE NUGGET", "OUT", "DROP NUGGET", "UP",
                 "EAST", "EAST", "EAST", "TAKE ROD", "WEST",
                 "WEST", "LOOK"
                 ]

        for move in moves:
            check.stdout("> ")
            check.stdin(move, prompt=False)
        check.stdout(room_14_description, regex=False)

        moves = ["EAST", "DROP BIRD", "WEST", "LOOK"]

        for move in moves:
            check.stdout("> ")
            check.stdin(move, prompt=False)
        check.stdout(room_15_description, regex=False)

    except check50.Failure as error:
        raise check50.Failure("Did not find correct room description when "
                              "going WEST from room 13 holding either BIRD & "
                              "ROD or just ROD.")


@check50.check(conditional_move)
def forced_move():
    """Checking if FORCED immediately moves the player."""
    check = check50.run(run_command)
    moves = ["DOWN", "DOWN", "DOWN", "DOWN"]

    for move in moves:
        check.stdout("> ")
        check.stdin(move, prompt=False)

    check.stdout("The grate is locked and you don't have any keys.")
    check.stdout("Outside grate")


@check50.check(conditional_move)
def exotic_move():
    """Performing special moves such as JUMP or XYZZY."""
    try:
        check = check50.run(run_command)
        moves = ["IN", "XYZZY"]

        for move in moves:
            check.stdout("> ")
            check.stdin(move, prompt=False)

        check.stdout("It is now pitch dark.  If you proceed you will "
                     "likely fall into a pit.", regex=False)
    except check50.Failure as error:
        raise check50.Failure("Could not perform XYZZY. Check "
                              "CrowtherRooms.txt for all the different"
                              "connections.")


@check50.check(exotic_move)
def won():
    """Testing Crowther Adventure win condition."""
    moves = ["IN", "TAKE KEYS", "OUT", "DOWN", "DOWN",
             "DOWN", "DOWN", "TAKE LAMP", "IN", "WEST",
             "WEST", "WEST", "TAKE BIRD", "WEST", "DOWN",
             "SOUTH", "TAKE NUGGET", "OUT", "DROP NUGGET", "UP",
             "EAST", "EAST", "EAST", "TAKE ROD", "WEST",
             "WEST", "WEST", "DOWN", "TAKE NUGGET", "WEST",
             "WAVE", "TAKE DIAMOND", "WEST", "SOUTH", "SOUTH",
             "EAST", "NORTH", "NORTH", "TAKE CHEST", "OUT",
             "WEST", "DOWN", "WEST", "DOWN", "NORTH",
             "EAST", "TAKE COINS", "OUT", "NORTH", "DOWN",
             "EAST", "DROP LAMP", "DROP BIRD", "DROP NUGGET", "DROP COINS",
             "NORTH", "TAKE EMERALD", "OUT", "TAKE LAMP", "TAKE BIRD",
             "TAKE NUGGET", "TAKE COINS", "WEST", "WEST", "WEST",
             "DOWN", "WATER", "TAKE EGGS", "NORTH", "DOWN",
             "OUT", "EAST", "EAST", "EAST", "UP",
             "SOUTH", "SOUTH", "WEST", "WAVE", "WEST",
             "SOUTH", "NORTH", "NORTH", "EAST", "DOWN",
             "EAST", "EAST", "XYZZY", "NORTH"
             ]
    check = check50.run(run_command)

    for move in moves:
        check.stdout("> ")
        check.stdin(move, prompt=False)

    check.stdout("You have collected all the treasures and are admitted to "
                 "the Adventurer's Hall of Fame.  Congratulations!").exit(0)
