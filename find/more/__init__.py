less = __import__("check50").import_checks("../less")
from less import *
import random

# find/more checks include the find/less checks, we just add a check for the speed/
# complexity of the sorting method.

@check50.check(compiles, timeout=10)
def sort_big():
    """sorts a big array"""
    items = [random.randint(0, 10**9) for _ in range(10**5)]
    check = check50.run("./sort")
    check.stdin("\n".join(str(i) for i in items), prompt=False)
    check.stdin(check50.EOF)
    check.stdout("\n".join(str(i) for i in sorted(items)))
    check.exit(0)
