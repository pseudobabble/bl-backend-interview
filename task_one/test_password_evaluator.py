import string
import random

import pytest

from task_one.password_evaluator import PasswordEvaluator


class TestPasswordEvaluator:

    def test_init(self):
        p = PasswordEvaluator('abc')

        assert p._original_password == 'abc'
        assert p._valid_chars == (
            string.ascii_lowercase +
            string.ascii_uppercase +
            string.digits
        )
        # the other attrs are modified on init

    @pytest.mark.parametrize(
        'input_string',
        [
            'abcc',
            'abccc',
            'abcccc',
            'abccccccccccccccccccccc'
        ]
    )
    def test_repeated_indices(self, input_string):
        p = PasswordEvaluator(input_string)

        assert 'ccc' not in p.representation

    @pytest.mark.parametrize(
        'input_string, source, intersect',
        [
            ['abc', 'apq', True],
            ['abc', 'xyz', False],
        ]
    )
    def test_has_at_least_one_char_from(self, input_string, source, intersect):
        assert bool(
            PasswordEvaluator._has_at_least_one_char_from(source, input_string)
        ) == intersect

    @pytest.mark.parametrize(
        'input_string',
        [
            'abc',
            'abcc',
            'abccc',
            'abcccc',
            'abccccc',
            'abcccccc'
            'abccccccc'
        ]
    )
    def test_make_secure_pads(self, input_string):
        p = PasswordEvaluator(input_string)

        assert len(p) >= 7

    @pytest.mark.parametrize(
        'input_string',
        [
            random.choice(
                string.ascii_letters + string.digits
            )*random.randint(25, 100)
        ]*5
    )
    def test_make_secure_trims(self, input_string):
        p = PasswordEvaluator(input_string)

        assert len(p) <= 25

    def test_make_secure_adds_upper(self):
        p = PasswordEvaluator('abc')

        assert any(s.isupper() for s in p.representation)

    def test_make_secure_adds_lower(self):
        p = PasswordEvaluator('ABC')

        assert any(s.islower() for s in p.representation)

    def test_make_secure_adds_digit(self):
        p = PasswordEvaluator('ABCabc')

        assert any(s.isdigit() for s in p.representation)

    @pytest.mark.parametrize(
        'input_string',
        [
            'abc',
            'abcc',
            'abccc',
            'abcccc',
            'abccccc',
            'abcccccc'
            'abccccccc'
        ]
    )
    def test_make_secure_replaces_repetitions(self, input_string):
        p = PasswordEvaluator(input_string)

        assert 'ccc' not in p.representation

    def test_make_secure_avoids_inclusions(self):
        p = PasswordEvaluator('abc', avoid=['a'])

        assert 'a' not in p.representation
