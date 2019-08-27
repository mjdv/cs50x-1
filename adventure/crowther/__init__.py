import check50
import pkg_resources
if int(pkg_resources.get_distribution("check50").version[0]) < 3:
    raise ImportError("This check requires check50 version 3.0.0 or above.")

small = check50.import_checks("../small")
from small import *


room_3_name = "Inside building"
room_3_description = ("You are inside a building, a well house for a large "
                      "spring. The exit door is to the south.  There is "
                      "another room to the north, but the door is barred by "
                      "a shimmering curtain.")
room_3_items = ["KEYS", "a set of keys", "\n", "WATER", "a bottle of water"]


@check50.check()
def exists():
    """Checking if all files exist."""
    init("Crowther")
    check50.exists("adventure.py")
    check50.exists("room.py")


@check50.check(conditional_move)
def multiple_conditional_move():
    """Check if holding multiple items affects conditional movement."""
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
                              "ROD or just ROD.\n"
                              f"    {error}")


@check50.check(move_repeatedly)
def special_move():
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


@check50.check(special_move)
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
                 "the Adventurer's Hall of Fame.  Congratulations!",
                 regex=False)
    check.stdout("\n")
    check.exit(0)
