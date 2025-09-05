
# This is used to make SwiftGUI compatible with python 3.10

import sys

if sys.version_info >= (3, 11):
    from typing import Self
else:
    from typing import TypeVar
    Self = TypeVar("Self", bound= "Any")

if sys.version_info >= (3, 12):
    from itertools import batched
else:
    # Implement it myself if it's not available...
    def batched(it, n: int):
        collected = list()
        it = list(it)

        num = 0
        for elem in it:
            if num == n:
                num = 0
                yield collected.copy()
                collected.clear()

            collected.append(elem)
            num += 1

        if collected:
            yield collected


