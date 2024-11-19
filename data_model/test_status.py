from enum import Enum


class Status(Enum):
    """
    用例状态，用例通过状态
    """
    AC = "AC"  # Accepted
    RE = "RE"  # Runtime Error
    TLE = "TLE"  # Time Limit Exceeded
    WA = "WA"  # Wrong Answer
