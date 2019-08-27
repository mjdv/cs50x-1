import check50

tiny = check50.import_checks("../tiny")
from tiny import *


@check50.check()
def exists():
    """Checking if all files exist."""
    init("Small")
    check50.exists("adventure.py")
    check50.exists("room.py")


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
    for item in room_8_items:
        check.stdout(item, regex=False)


@check50.check(conditional_move)
def forced_move():
    """Checking if FORCED immediately moves the player."""
    check = check50.run(run_command)
    moves = ["DOWN", "DOWN", "DOWN", "DOWN"]

    for move in moves:
        check.stdout("> ")
        check.stdin(move, prompt=False)

    check.stdout("The grate is locked and you don't have any keys.",
                 regex=False)
    check.stdout("Outside grate", regex=False)