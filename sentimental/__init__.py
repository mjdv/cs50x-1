import check50
import uva.check50.py
import re

@check50.check()
def hello_exists():
    """hello.py exists."""
    check50.exists("hello.py")

@check50.check(hello_exists)
def hello_compiles():
    """hello.py compiles."""
    uva.check50.py.compile("hello.py")

@check50.check(hello_compiles)
def prints_hello():
    """hello.py prints "hello, world\\n" """
    from re import match

    expected = "[Hh]ello, world!?\n"

    result = uva.check50.py.run("hello.py")

    if not re.search(expected, result.stdout):
        help = None
        if re.search(expected[:-1], result.stdout):
            help = r"did you forget a newline ('\n') at the end of your printf string?"
        raise check50.Mismatch("hello, world\n", result.stdout, help=help)

@check50.check()
def mario_exists():
    """mario.py exists."""
    check50.exists("mario.py")
    check50.include("1.txt", "2.txt", "23.txt")

@check50.check(mario_exists)
def mario_compiles():
    """mario.py compiles."""
    uva.check50.py.compile("mario.py")

@check50.check(mario_compiles)
def test_reject_negative():
    """mario.py rejects a height of -1"""
    result = uva.check50.py.run("mario.py", stdin=["-1", "2"])
    if result.stdin:
        raise check50.Failure("Expected stdin to be empty")

@check50.check(mario_compiles)
def test0():
    """mario.py handles a height of 0 correctly"""
    result = uva.check50.py.run("mario.py", stdin=["0"])
    if "#" in result.stdout:
        raise check50.Failure("Expected no # in stdout")

@check50.check(mario_compiles)
def test1():
    """mario.py handles a height of 1 correctly"""
    result = uva.check50.py.run("mario.py", stdin=["1"])
    check_pyramid(result.stdout, "Height: " + open("1.txt").read())

@check50.check(mario_compiles)
def test2():
    """mario.py handles a height of 2 correctly"""
    result = uva.check50.py.run("mario.py", stdin=["2"])
    check_pyramid(result.stdout, "Height: " + open("2.txt").read())

@check50.check(mario_compiles)
def test23():
    """mario.py handles a height of 23 correctly"""
    result = uva.check50.py.run("mario.py", stdin=["23"])
    check_pyramid(result.stdout, "Height: " + open("23.txt").read())

@check50.check(mario_compiles)
def test24():
    """mario.py rejects a height of 24, and then accepts a height of 2"""
    result = uva.check50.py.run("mario.py", stdin=["24", "2"])
    if result.stdin:
        raise check50.Failure("Expected stdin to be empty")
    check_pyramid(result.stdout, "Height: Height: " + open("2.txt").read())

def check_pyramid(output, correct):
    if output == correct:
        return

    output = output.splitlines()
    correct = correct.splitlines()

    help = None
    if len(output) == len(correct):
        if all(ol.rstrip() == cl for ol, cl in zip(output, correct)):
            help = "did you add too much trailing whitespace to the end of your pyramid?"
        elif all(ol[1:] == cl for ol, cl in zip(output, correct)):
            help = "are you printing an additional character at the beginning of each line?"

    raise check50.Mismatch(correct, output, help=help)

@check50.check()
def greedy_exists():
    """greedy.py exists"""
    check50.exists("greedy.py")


@check50.check(greedy_exists)
def greedy_compiles():
    """greedy.py compiles"""
    uva.check50.py.compile("greedy.py")


@check50.check(greedy_compiles)
def test041():
    """greedy.py input of 0.41 yields output of 4"""
    result = uva.check50.py.run("greedy.py", stdin=["0.41"])
    if not coins(4).match(result.stdout):
        raise check50.Mismatch("4\n", result.stdout)


@check50.check(greedy_compiles)
def test001():
    """greedy.py input of 0.01 yields output of 1"""
    result = uva.check50.py.run("greedy.py", stdin=["0.01"])
    if not coins(1).match(result.stdout):
        raise check50.Mismatch("1\n", result.stdout)


@check50.check(greedy_compiles)
def test015():
    """greedy.py input of 0.15 yields output of 2"""
    result = uva.check50.py.run("greedy.py", stdin=["0.15"])
    if not coins(2).match(result.stdout):
        raise check50.Mismatch("2\n", result.stdout)


@check50.check(greedy_compiles)
def test160():
    """greedy.py input of 1.6 yields output of 7"""
    result = uva.check50.py.run("greedy.py", stdin=["1.6"])
    if not coins(7).match(result.stdout):
        raise check50.Mismatch("7\n", result.stdout)


@check50.check(greedy_compiles)
def test230():
    """greedy.py input of 23 yields output of 92"""
    result = uva.check50.py.run("greedy.py", stdin=["23"])
    if not coins(92).match(result.stdout):
        raise check50.Mismatch("92\n", result.stdout)


@check50.check(greedy_compiles)
def test420():
    """greedy.py input of 4.2 yields output of 18"""
    result = uva.check50.py.run("greedy.py", stdin=["4.2"])
    if not coins(18).match(result.stdout):
        help = None
        if coins(22).match(result.stdout):
            help = "did you forget to round your input to the nearest cent?"
        raise check50.Mismatch("18\n", actual, help=help)


@check50.check(greedy_compiles)
def test_reject_negative():
    """greedy.py rejects a negative input like -1"""
    result = uva.check50.py.run("greedy.py", stdin=["-1", "2"])
    if result.stdin:
        raise check50.Failure("expected stdin to be empty!")


def coins(num):
    # regex that matches `num` not surrounded by any other numbers (so coins(2) won't match e.g. 123)
    return re.compile(fr".*(?<![\d]){num}(?![\d]).*", re.MULTILINE)

@check50.check()
def vigenere_exists():
    """vigenere.py exists."""
    check50.exists("vigenere.py")


@check50.check(vigenere_exists)
def vigenere_compiles():
    """vigenere.py compiles."""
    uva.check50.py.compile("vigenere.py")


@check50.check(vigenere_compiles)
def aa():
    """vigenere.py encrypts "a" as "a" using "a" as keyword"""
    result = uva.check50.py.run("vigenere.py", argv=["vigenere.py", "a"], stdin=["a"])
    if not re.match(".*ciphertext:\s*a\n", result.stdout):
        raise check50.Mismatch("ciphertext: a\n", result.stdout)


@check50.check(vigenere_compiles)
def bazbarfoo_caqgon():
    """vigenere.py encrypts "barfoo" as "caqgon" using "baz" as keyword"""
    result = uva.check50.py.run("vigenere.py", argv=["vigenere.py", "baz"], stdin=["barfoo"])
    if not re.match(".*ciphertext:\s*caqgon\n", result.stdout):
        raise check50.Mismatch("ciphertext: caqgon\n", result.stdout)


@check50.check(vigenere_compiles)
def mixedBaZBARFOO():
    """vigenere.py encrypts "BaRFoo" as "CaQGon" using "BaZ" as keyword"""
    result = uva.check50.py.run("vigenere.py", argv=["vigenere.py", "BaZ"], stdin=["BaRFoo"])
    if not re.match(".*ciphertext:\s*CaQGon\n", result.stdout):
        raise check50.Mismatch("ciphertext: CaQGon\n", result.stdout)


@check50.check(vigenere_compiles)
def allcapsBAZBARFOO():
    """vigenere.py encrypts "BARFOO" as "CAQGON" using "BAZ" as keyword"""
    result = uva.check50.py.run("vigenere.py", argv=["vigenere.py", "BAZ"], stdin=["BARFOO"])
    if not re.match(".*ciphertext:\s*CAQGON\n", result.stdout):
        raise check50.Mismatch("ciphertext: CAQGON\n", result.stdout)


@check50.check(vigenere_compiles)
def bazworld():
    """vigenere.py encrypts "world!$?" as "xoqmd!$?" using "baz" as keyword"""
    result = uva.check50.py.run("vigenere.py", argv=["vigenere.py", "baz"], stdin=["world!$?"])
    if not re.match(".*ciphertext:\s*xoqmd!\$\?\n", result.stdout):
        raise check50.Mismatch("ciphertext: xoqmd!$?\n", result.stdout)


@check50.check(vigenere_compiles)
def withspaces():
    """vigenere.py encrypts "hello, world!" as "iekmo, vprke!" using "baz" as keyword"""
    result = uva.check50.py.run("vigenere.py", argv=["vigenere.py", "baz"], stdin=["hello, world!"])
    if not re.match(".*ciphertext:\s*iekmo, vprke\!\n", result.stdout):
        raise check50.Mismatch("ciphertext: iekmo, vprke!\n", result.stdout)


@check50.check(vigenere_compiles)
def noarg():
    """vigenere.py handles lack of argv[1]"""
    try:
        result = uva.check50.py.run("vigenere.py", argv=["vigenere.py"])
    except uva.check50.py.PythonException as e:
        if not isinstance(e.exception, SystemExit):
            raise e
    else:
        if not "usage: python vigenere.py key" in result.stdout:
            raise check50.Mismatch("usage: python vigenere.py key", result.stdout)


@check50.check(vigenere_compiles)
def toomanyargs():
    """vigenere.py handles argc > 2"""
    try:
        result = uva.check50.py.run("vigenere.py", argv=["vigenere.py", "1", "2", "3"])
    except uva.check50.py.PythonException as e:
        if not isinstance(e.exception, SystemExit):
            raise e
    else:
        if not "usage: python vigenere.py key" in result.stdout:
            raise check50.Mismatch("usage: python vigenere.py key", result.stdout)
