"""Make passwords secure, and record how many operations that requires."""
import sys
import random
import string
from typing import Optional, List, Sequence, Dict
from collections import Counter, defaultdict


class PasswordEvaluator:
    """
    This class evaluates a password for security and
    makes any necessary changes to make it secure.
    """

    def __init__(
            self,
            password: str,
            avoid: Optional[List[str]] = None
    ) -> None:
        """
        Initialise a PasswordEvaluator.

        :param password: the password to evaluate
        :param avoid: a list of strings to avoid including in the
            suggested password
        :returns: None

        """
        self._original_password = password
        self._state = [*password]
        self._operation_count = 0
        self._valid_chars = (
            string.ascii_lowercase +
            string.ascii_uppercase +
            string.digits
        )
        self._make_secure(avoid=avoid)

    def __len__(self) -> int:
        """
        Return length of the password.

        :returns: int

        """
        return len(self._state)

    @property
    def _counts(self) -> Counter:
        """
        Get the frequency count of each item in state.

        :returns: Counter

        """
        return Counter(self._state)

    @property
    def _repeated_indices(self) -> Dict[str, List[int]]:
        """
        Get a mapping of a state item to
        its repeated indices. Does not include
        the first appearance.

        :returns: Dict[str, List[int]]

        """
        tracker = set()
        repeated_indices = defaultdict(list)
        for index, item in enumerate(self._state):
            if item not in tracker:
                tracker.add(item)
            else:
                repeated_indices[item].append(index)

        return repeated_indices

    def __repr__(self) -> str:
        """
        Display the PasswordEvaluator.

        :returns: str

        """
        return (
            f"Original password: {self._original_password}\n"
            f"Secure password: {self.representation}\n"
            f"Operations required: {self._operation_count}\n"
        )

    @property
    def representation(self) -> str:
        """
        Create a string representation of the password.

        :returns: str

        """
        return ''.join(self._state)

    @staticmethod
    def _has_at_least_one_char_from(source: Sequence, target: Sequence) -> set:
        """
        Return the intersection of self._state and source.

        :param source: a Sequence (set, list, string, etc)
        :returns: set

        """
        return set(source).intersection(set(target))

    def _make_secure(self, avoid: Optional[List] = None) -> None:
        """
        Make the supplied password secure, and record the number
        of operations required to do so.

        1: Pad right to 7 chars
        2: Trim left to 22 chars, because we may need to add
        3: Add at least one each of UPPER, lower, 0-9
        4: Replace repeated characters if more than 2 in a row
        5: Avoid including a bad password in the password string

        :param avoid: list of strings
        :returns: None

        """
        # TODO: Question: What if there are spaces? remove spaces?
        avoid = avoid or []

        while len(self._state) < 7:
            self._state.append(random.choice(self._valid_chars))
            self._operation_count += 1

        while len(self._state) > 22:
            self._state.pop(0)
            self._operation_count += 1

        while not self._has_at_least_one_char_from(
                string.ascii_lowercase,
                self._state
        ):
            self._state.append(random.choice(string.ascii_lowercase))
            self._operation_count += 1

        while not self._has_at_least_one_char_from(
                string.ascii_uppercase,
                self._state
        ):
            self._state.append(random.choice(string.ascii_uppercase))
            self._operation_count += 1

        while not self._has_at_least_one_char_from(
                string.digits,
                self._state
        ):
            self._state.append(random.choice(string.digits))
            self._operation_count += 1

        # fix repetitions > 2
        for char, indices in self._repeated_indices.items():
            if self._counts[char] > 2:
                for index in indices[:-1]:
                    self._state[index] = random.choice(self._valid_chars)
                    self._operation_count += 1

        # avoid including bad passwords
        for bad_password in avoid:
            if bad_password in self.representation:
                index = self.representation.index(bad_password)
                self._state[index] = random.choice(self._valid_chars)
                self._operation_count += 1


if __name__ == '__main__':

    try:
        with open(sys.argv[2]) as f:
            common_passwords = f.readlines()
            common_passwords = [i.strip('\n') for i in common_passwords]

            password = PasswordEvaluator(sys.argv[1], avoid=common_passwords)

            print(password)
    except IndexError:
        print(
            "\n"
            "Usage: `python -m password_evaluator [PASSWORD] [PATH]`\n"
            "- [PASSWORD] should be string password to evaluate\n"
            "- [PATH] should be a path to a newline delimited file of bad passwords to avoid"
        )
