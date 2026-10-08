from typing import TypeVar

"""
This is a doc comment.
"""

#: CATVariant The CATVariant type allows both int and string.
CATVariant = int | str

list_str = TypeVar("list_str", list, str)
