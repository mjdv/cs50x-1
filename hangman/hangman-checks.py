import check50
import os
import sys
import random
import string

def raise_timeout():
    raise Exception("Timeout")

@check50.check()
def exists():
    """hangman.py and dictionary.txt both exist."""
    check50.exists("hangman.py")
    check50.include("dictionary.txt")

@check50.check(exists, timeout=3)
def can_import():
    """
    You can import hangman.py without it hanging, or producing output.
    """
    res = check50.run('python3 -c "import hangman"').stdout(timeout=2)
    if res != "":
        raise check50.Failure("Code produced output when imported.", 
            help='Did you wrap all code except the classes in ' \
                    '"if __name__ == \'__main__\'"?')

@check50.check(can_import)
def load_lexicon():
    """
    You can create a Lexicon object.
    """
    sys.path.append(os.getcwd())
    import hangman
    try:
        Lexicon = hangman.Lexicon
        lex = Lexicon()
    except Exception as e:
        error='Was unable to create a lexicon object with "Lexicon()"'
        help=f"Got exception {str(e)}."
        raise check50.Failure(error, help=help)

@check50.check(load_lexicon)
def test_lexicon():
    """
    Lexicon object returns the 4-letter words from dictionary.txt.
    """
    sys.path.append(os.getcwd())
    import hangman
    Lexicon = hangman.Lexicon
    lex = Lexicon()

    try:
        words = lex.get_words(4)
    except Exception as e:
        raise check50.Failure('Was unable to get words of length 4 from lexicon '\
            'object with "lex.get_words(4)".')

    if len(words) != 4128:
        raise check50.Failure("Did not succesfully load all 4-letter words.",
                help=f"Expected 4128 words, got {len(words)}.")

@check50.check(can_import)
def load_hangman():
    """
    You can create a Hangman object (with the right parameters).
    """
    sys.path.append(os.getcwd())
    import hangman
    try:
        Hangman = hangman.Hangman
    except Exception as e:
        raise check50.Failure("Cannot find the class Hangman.")

    try:
        game = Hangman(4, 5)
    except Exception as e:
        raise check50.Failure("Failed to create a Hangman object for a " \
                "length 4 word and 5 guesses.",
                help=f"Got the exception {e}.")

@check50.check(load_hangman)
def wrong_hangman():
    """
    Trying to create a Hangman object with incorrect parameters causes an
    exception to be raised.
    """
    params = [(-2, 3), (27, 5), (5, 0), (5, -1)]
    messages = ["-2 letter word, which does not exist.",
                "27 letter word, which does not exist.",
                "game with 0 guesses, which is too few.",
                "game with -1 guesses, which is too few."]

    for par_pair, message in zip(params, messages):
        game = None
        try:
            game = Hangman(*par_pair)
        except Exception as e:
            pass

        if game is not None:
            raise check50.Failure("Created a Hangman object for a " + message)

@check50.check(wrong_hangman)
def wrong_guesses():
    """
    Wrong input into game.guess() gives an exception.
    """
    sys.path.append(os.getcwd())
    import hangman
    Hangman = hangman.Hangman
    game = Hangman(4, 5)

    inputs = ["word", " ", "6", 25, True, False, None]
    for wrong_input in inputs:
        accepted = True
        try:
            game.guess(wrong_input)
        except Exception:
            accepted = False

        if accepted:
            raise check50.Failure("A guess of {str(wrong_input)} was accepted, " \
                    "but any input other than a single letter should give an " \
                    "exception.")

    game.guess('A')
    accepted = True
    try:
        game.guess('A')
    except Exception:
        accepted = False

    if accepted:
        raise check50.Failure("Guessing an already guessed letter should give " \
                "an exception.")
        
@check50.check(load_hangman)
def empty_game():
    """
    A new game starts unfinished and without any guessed letters.
    """
    sys.path.append(os.getcwd())
    import hangman
    Hangman = hangman.Hangman
    game = Hangman(4, 5)
    try:
        pattern = game.pattern()
        guessed_string = game.guessed_string()
        finished = game.finished()
        won = game.won()
        lost = game.lost()
    except Exception as e:
        raise check50.Failure("Was unable to call pattern, guessed_string, " \
                "won, lost, or finished on Hangman object.",
                help=f"Got the exception {e}")

    for expected, actual in [("____", pattern), ("", guessed_string), 
            (False, finished), (False, won), (False, lost)]:
        if expected != actual:
            raise check50.Mismatch(str(expected), str(actual))

@check50.check(empty_game)
def win_games():
    """
    Succesfully play five winning games.
    """
    for _ in range(5):
        play_game(win=True)

@check50.check(empty_game)
def lose_games():
    """
    Play five losing games, each time returning "False".
    """
    for _ in range(5):
        play_game(win=False)


def play_game(win):
    """
    Win a game (given enough guesses).
    """
    sys.path.append(os.getcwd())
    import hangman
    Hangman = hangman.Hangman
    if win:
        game = Hangman(5, 26)
    else:
        game = Hangman(12, 5)
    
    alphabet = list(string.ascii_lowercase)
    random.shuffle(alphabet)
    guesses = []
    num_wrong_guesses = 0

    for letter in alphabet:
        guesses.append(letter)
        correct = game.guess(letter)
        if not correct:
            num_wrong_guesses += 1

        if not letter in game.guessed_string():
            error = "A guessed letter does not appear in the game's guessed_string."
            help = f'I guessed "{letter}" but afterwards the guessed string is ' \
                   f'{game.guessed_string()}.'
            raise check50.Failure(error, help=help)

        if correct != (letter in game.pattern()):
            error = "The return value of game.guess(letter) should be True if " \
                    "the guess was correct, and False otherwise."
            help = f'Got the return value {correct}.'
            raise check50.Failure(error, help=help)

        if not all(x in guesses for x in game.pattern() if x != "_"):
            error = "The game pattern contains characters other than guessed " \
                    "letters and underscores."
            help = f"I found pattern {game.pattern()} with guesses " \
                   f"{''.join(guesses)}."
            raise check50.Failure(error, help=help)
        
        word = game.consistent_word()
        if not all(a == b or b == "_" for a, b in zip(word, game.pattern())):
            error = "Consistent word is not consistent with pattern."
            help = f'Consistent word is {word} and pattern is {game.pattern()}'
            raise check50.Failure(error, help=help)

        if game.finished():
            break
        
        if not win and num_wrong_guesses >= 5:
            error = "The game is not finished, but I should have run out of " \
                    "guesses."
            help = "I started a game with 5 guesses, and after 5 wrong guesses " \
                   "I am still playing."
            raise check50.Failure(error, help=help)
    else:
        error = "The game is not finished, but I guessed every letter in the " \
                "alphabet."
        help = "Did you implement game.finished() correctly?"
        raise check50.Failure(error, help=help)
    
    if win: 
        if game.won() != True:
            error = "I did not win the game, even while guessing all 26 letters " \
                    "in the alphabet."
            help = "Did you implement game.won() correctly?"
            raise check50.Failure(error, help=help)

        if game.lost() != False:
            error = "I lost the game, even while guessing all 26 letters."
            help = "Did you implement game.lost() correctly?"
            raise check50.Failure(error, help=help)

        if "_" in game.pattern():
            error = "Blanks in pattern after victorious game."
            help = f"Expected a full word, but the pattern is {game.pattern()}."
            raise check50.Failure(error, help=help)

        word = game.consistent_word()
        if word != game.pattern():
            error = "After victorious game, only consistent word should be pattern."
            help = f'Got consistent word {word} ' \
                   f'but pattern {game.pattern()}.'
            raise check50.Failure(error, help=help)
    else:
        if game.won() != False:
            error = "Won the game with 5 random guesses for a " \
                    "12-letter word."
            help = "Did you implement game.won() correctly?"
            raise check50.Failure(error, help=help)

        if game.lost() != True:
            error = "Did not lose the game with 5 random guesses for a " \
                    "12-letter word."
            help = "Did you implement game.lost() correctly?"
            raise check50.Failure(error, help=help)

        if not "_" in game.pattern():
            error = "The game's pattern is filled in, even though I lost."
            help = f"Got pattern {game.pattern()}, expected a pattern with "\
                    "underscores."
            raise check50.Failure(error, help=help)
