import check50

# Template for checks:
'''

@check50.check()
def test_name():
    """Test message."""
    check50.run(run_command)

'''

run_command = "python3 adventure.py"

room_1_name = "Outside building\n"
room_1_description = "You are standing at the end of a road before a small brick building.  A small stream flows out of the building and down a gully to the south.  A road runs up a small hill to the west.\n"

room_2_name = "End of road\n"
room_2_description = "You are at the end of a road at the top of a small hill. You can see a small building in the valley to the east.\n"

room_3_name = "Inside building\n"
room_3_description = "You are inside a building, a well house for a large spring. The exit door is to the south.  There is another room to the north, but the door is barred by a shimmering curtain.\n"
room_3_items = "KEYS: a set of keys\nWATER: a bottle of water"

room_8_name = "Beneath grate\n"
room_8_description = "You are in a small chamber beneath a 3x3 steel grate to the surface.  A low crawl over cobbles leads inward to the west.\n"
room_8_items = "LAMP: a brightly shining brass lamp"

room_14_description = "You are in a splendid chamber thirty feet high.  The walls are frozen rivers of orange stone.  A narrow canyon and a good passage exit from east and west sides of the chamber.\n"
room_15_description = "You are in a splendid chamber thirty feet high.  The walls are frozen rivers of orange stone.  A narrow canyon and a good passage exit from east and west sides of the chamber. High in the cavern, you see a little bird flying around the rocks.  It takes one look at the black rod and quickly flies out of sight.\n"

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
    """Move once to the west."""
    try:
        check50.run(run_command).stdout(room_1_description)
    except check50.Failure as error:
        raise check50.Failure(f"Expected the description of initial room when Adventure starts.\n    {error}")
    check50.run(run_command).stdin("WEST").stdout(room_2_description)

@check50.check(exists)
def move_invalid():
    """Attempt an invalid move."""
    check50.run(run_command).stdin("EAST").stdout("Invalid command.")

@check50.check(move_once)
def move_repeatedly():
    """Moving west then east in succession."""
    check50.run(run_command).stdin("west").stdout(room_2_description).stdin("east").stdout(room_1_name).stdin("west").stdout(room_2_name)

@check50.check(move_repeatedly)
def move_mixed_case():
    """Move with mixed case command."""
    check50.run(run_command).stdin("west").stdout(room_2_description)
    check50.run(run_command).stdin("wESt").stdout(room_2_description)
    check50.run(run_command).stdin("west").stdin("EAST").stdout(room_1_name)

@check50.check(move_mixed_case)
def helper_commands():
    """Testing helper commands; HELP, LOOK, QUIT."""
    try:
        check50.run(run_command).stdin("HELP").stdout(
            "You can move by typing directions such as EAST/WEST/IN/OUT\n" +
            "QUIT quits the game.\n" +
            "HELP prints instructions for the game.\n" +
            "INVENTORY lists the item in your inventory.\n" +
            "LOOK lists the complete description of the room and its contents.\n" +
            "TAKE <item> take item from the room.\n" +
            "DROP <item> drop item from your inventory.\n"
            )
    except check50.Failure as error:
        raise check50.Failure(f"HELP did not print the expected message.\n    {error}")
    try:
        check50.run(run_command).stdin("LOOK").stdout(room_1_description)
        check50.run(run_command).stdin("look").stdout(room_1_description)
    except check50.Failure as error:
        raise check50.Failure(f"LOOK/look did not print the expected room description.\n    {error}")
    try:
        check50.run(run_command).stdin("QUIT").stdout("Thanks for playing!").exit(0)
    except check50.Failure as error:
        raise check50.Failure(f"QUIT did not print the expected message.\n    {error}")

@check50.check(helper_commands)
def commands():
    """Test if program accepts user commands and abbreviations."""
    check50.run(run_command).stdin("cs50").stdout("Invalid command.")
    try:
        check50.run(run_command).stdin("W").stdout(room_2_description)
    except check50.Failure as error:
        raise check50.Failure(f"Could not use abbreviation 'w' to move")
    try:
        check50.run(run_command).stdin("w").stdout(room_2_description)
    except check50.Failure as error:
        raise check50.Failure(f"Could not use abbreviation 'w' to move")

@check50.check(helper_commands)
def find_items():
    """Finds items in rooms."""
    try:
        check50.run(run_command).stdin("in").stdout(room_3_description + room_3_items)
    except check50.Failure as error:
        raise check50.Failure(f"Could not find items upon first entering room.\n    {error}")
    try:
        check50.run(run_command).stdin("in").stdin("out").stdin("in").stdin("look").stdout("KEYS: a set of keys\nWATER: a bottle of water")
    except check50.Failure as error:
        raise check50.Failure(f"Could not find items when using LOOK.\n    {error}")

@check50.check(find_items)
def handle_items():
    """Take and drop items."""
    check50.run(run_command).stdin("in").stdin("TAKE keys").stdout("KEYS taken.")
    check50.run(run_command).stdin("in").stdin("TAKE keys").stdin("out").stdin("DROP keys").stdout("KEYS dropped.").stdin("look").stdout("KEYS: a set of keys\n")

@check50.check(handle_items)
def handle_invalid_items():
    """Take and drop nonexistand items."""
    check50.run(run_command).stdin("in").stdin("TAKE kes").stdout("No such item.")
    check50.run(run_command).stdin("in").stdin("TAKE keys").stdin("TAKE keys").stdout("No such item.")
    check50.run(run_command).stdin("in").stdin("DROP something").stdout("No such item.")

@check50.check(handle_items)
def inventory():
    """Using the INVENTORY command."""
    try:
        check50.run(run_command).stdin("INVENTORY").stdout("Your inventory is empty.")
    except check50.Failure as error:
        raise check50.Failure(f"Let the player know they have no items.\n    {error}")

@check50.check(handle_items)
def conditional_move():
    """Check if holding an item affects conditional movement."""
    check50.run(run_command).stdin("in").stdin("out").stdin("down\ndown\ndown\ndown").stdout("The grate is locked and you don't have any keys.")

    check50.run(run_command).stdin("in").stdin("TAKE keys").stdin("out").stdin("down\ndown\ndown\ndown").stdout(room_8_description + room_8_items)
    # Check for move with multiple conditions.
    try:
        check50.run(run_command).stdin("IN\nTAKE KEYS\nOUT\nDOWN\nDOWN\nDOWN\nDOWN\nTAKE LAMP\nIN\nWEST\nWEST\nWEST\nTAKE BIRD\nWEST\nDOWN\nSOUTH\nTAKE NUGGET\nOUT\nDROP NUGGET\nUP\nEAST\nEAST\nEAST\nTAKE ROD\nWEST\nWEST\nLOOK\n").stdout(room_14_description).stdin("EAST\nDROP BIRD\nWEST\nLOOK\n").stdout(room_15_description)
    except check50.Failure as error:
        raise check50.Failure("Did not find correct room description when going WEST from room 13 holding either BIRD & ROD or just ROD.")

@check50.check(conditional_move)
def forced_move():
    """Checking if forced movements prevent the player from passing the grate."""
    check50.run(run_command).stdin("down\ndown\ndown\ndown").stdout("The grate is locked and you don't have any keys.\nOutside grate")

@check50.check(conditional_move)
def exotic_move():
    """Performing special moves such as JUMP or XYZZY."""
    try:
        check50.run(run_command).stdin("IN").stdin("XYZZY").stdout("It is now pitch dark.  If you proceed you will likely fall into a pit.")
    except check50.Failure as error:
        raise check50.Failure("Could not perform XYZZY. Check CrowtherRooms.txt for all the different connections.")

@check50.check(exotic_move)
def won():
    """Testing Crowther Adventure win condition."""
    check50.run(run_command).stdin("IN\nTAKE KEYS\nOUT\nDOWN\nDOWN\nDOWN\nDOWN\nTAKE LAMP\nIN\nWEST\nWEST\nWEST\nTAKE BIRD\nWEST\nDOWN\nSOUTH\nTAKE NUGGET\nOUT\nDROP NUGGET\nUP\nEAST\nEAST\nEAST\nTAKE ROD\nWEST\nWEST\nWEST\nDOWN\nTAKE NUGGET\nWEST\nWAVE\nTAKE DIAMOND\nWEST\nSOUTH\nSOUTH\nEAST\nNORTH\nNORTH\nTAKE CHEST\nOUT\nWEST\nDOWN\nWEST\nDOWN\nNORTH\nEAST\nTAKE COINS\nOUT\nNORTH\nDOWN\nEAST\nDROP LAMP\nDROP BIRD\nDROP NUGGET\nDROP COINS\nNORTH\nTAKE EMERALD\nOUT\nTAKE LAMP\nTAKE BIRD\nTAKE NUGGET\nTAKE COINS\nWEST\nWEST\nWEST\nDOWN\nWATER\nTAKE EGGS\nNORTH\nDOWN\nOUT\nEAST\nEAST\nEAST\nUP\nSOUTH\nSOUTH\nWEST\nWAVE\nWEST\nSOUTH\nNORTH\nNORTH\nEAST\nDOWN\nEAST\nEAST\nXYZZY\nNORTH\n").stdout("You have collected all the treasures and are admitted to the Adventurer's Hall of Fame.  Congratulations!").exit(0)
