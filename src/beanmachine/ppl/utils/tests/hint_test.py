# Copyright (c) Facebook, Inc. and its affiliates.
"""Tests for hint.py"""

import unittest

import torch
from beanmachine.ppl.utils.hint import log1mexp, math_log1mexp


class HintTest(unittest.TestCase):
    """Tests for beanmachine/utils/hint.py."""

    def test_hint_math(self) -> None:
        """Smoke test for math_log1mexp"""
        math_observed = math_log1mexp(-15)
        math_expected = -2.9802e-07
        self.assertAlmostEqual(
            math_observed,
            math_expected,
            delta=1e-8,
            msg="Unexpected result for hint.math_log1mexp",
        )

    def test_hint_torch(self) -> None:
        """Smoke test for log1mexp"""
        observed = log1mexp(torch.tensor(-15))
        expected = torch.tensor(-2.9802e-07)
        self.assertAlmostEqual(
            observed,
            expected,
            delta=torch.tensor(1e-8),
            msg="Unexpected result for hint.log1mexp",
        )
