# Copyright (c) Meta Platforms, Inc. and affiliates.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

import unittest

import beanmachine.ppl as bm
import torch
import torch.distributions as dist


class SingleSiteUniformMetropolisHastingsTest(unittest.TestCase):
    class SampleBernoulliModel(object):
        @bm.random_variable
        def foo(self):
            return dist.Beta(torch.tensor(2.0), torch.tensor(2.0))

        @bm.random_variable
        def bar(self):
            return dist.Bernoulli(self.foo())

    class SampleCategoricalModel(object):
        @bm.random_variable
        def foo(self):
            return dist.Dirichlet(torch.tensor([0.5, 0.5]))

        @bm.random_variable
        def bar(self):
            return dist.Categorical(self.foo())

    def test_single_site_uniform_mh_with_bernoulli(self):
        model = self.SampleBernoulliModel()
        mh = bm.SingleSiteUniformMetropolisHastings()
        foo_key = model.foo()
        bar_key = model.bar()
        sampler = mh.sampler([foo_key], {bar_key: torch.tensor(0.0)}, num_samples=5)
        for world in sampler:
            self.assertTrue(foo_key in world)
            self.assertTrue(bar_key in world)
            self.assertTrue(foo_key in world.get_variable(bar_key).parents)
            self.assertTrue(bar_key in world.get_variable(foo_key).children)

    def test_single_site_uniform_mh_with_categorical(self):
        model = self.SampleCategoricalModel()
        mh = bm.SingleSiteUniformMetropolisHastings()
        foo_key = model.foo()
        bar_key = model.bar()
        sampler = mh.sampler([foo_key], {bar_key: torch.tensor(0.0)}, num_samples=5)
        for world in sampler:
            self.assertTrue(foo_key in world)
            self.assertTrue(bar_key in world)
            self.assertTrue(foo_key in world.get_variable(bar_key).parents)
            self.assertTrue(bar_key in world.get_variable(foo_key).children)
