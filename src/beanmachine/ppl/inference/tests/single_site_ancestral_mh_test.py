# Copyright (c) Facebook, Inc. and its affiliates.
import beanmachine.ppl as bm
import torch
import torch.distributions as dist
from beanmachine.ppl.experimental.global_inference.single_site_ancestral_mh import (
    SingleSiteAncestralMetropolisHastings,
)


class SampleModel:
    @bm.random_variable
    def foo(self):
        return dist.Normal(torch.tensor(0.0), torch.tensor(1.0))

    @bm.random_variable
    def bar(self):
        return dist.Normal(self.foo(), torch.tensor(1.0))


class ReproducibleModel:
    @bm.random_variable
    def K_minus_one(self):
        return dist.Poisson(rate=2.0)

    @bm.functional
    def K(self):
        return self.K_minus_one() + 1

    @bm.random_variable
    def mu(self):
        return dist.Normal(0, 1)


def test_single_site_ancestral_mh():
    model = SampleModel()
    mh = SingleSiteAncestralMetropolisHastings()
    foo_key = model.foo()
    bar_key = model.bar()
    sampler = mh.sampler(
        [model.foo()], {model.bar(): torch.tensor(0.0)}, num_samples=10
    )
    for world in sampler:
        assert foo_key in world
        assert bar_key in world
        assert foo_key in world.get_variable(bar_key).parents
        assert bar_key in world.get_variable(foo_key).children


def test_single_site_ancestral_mh_reproducible_results():
    model = ReproducibleModel()
    mh = SingleSiteAncestralMetropolisHastings()

    queries = [model.mu()]
    observations = {}

    torch.manual_seed(42)
    samples = mh.infer(queries, observations, num_samples=5, num_chains=1)
    run_1 = samples.get_variable(model.mu()).clone()

    torch.manual_seed(42)
    samples = mh.infer(queries, observations, num_samples=5, num_chains=1)
    run_2 = samples.get_variable(model.mu()).clone()
    assert run_1.allclose(run_2)

    torch.manual_seed(43)
    samples = mh.infer(queries, observations, num_samples=5, num_chains=1)
    run_3 = samples.get_variable(model.mu()).clone()
    assert not run_1.allclose(run_3)