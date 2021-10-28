import math
from abc import abstractmethod

import torch
import torch.distributions as dist
from beanmachine.ppl.experimental.global_inference.proposer.base_proposer import (
    BaseProposer,
)
from beanmachine.ppl.experimental.global_inference.simple_world import SimpleWorld
from beanmachine.ppl.model.rv_identifier import RVIdentifier


class BaseSingleSiteMHProposer(BaseProposer):
    def __init__(self, target_rv: RVIdentifier):
        self.node = target_rv

    def propose(self, world: SimpleWorld):
        """Propose a new value for self.node with Metropolis-Hasting algorithm
        https://en.wikipedia.org/wiki/Metropolis%E2%80%93Hastings_algorithm#Formal_derivation
        Classes that inherit this proposer should override `get_proposal_distribution`
        to define the algorithm-specific way to sample the next state.
        """
        proposal_dist = forward_dist = self.get_proposal_distribution(world)
        old_value = world[self.node]
        # pyre-ignore[20]
        proposed_value = proposal_dist.sample()
        new_world = world.replace({self.node: proposed_value})
        backward_dist = self.get_proposal_distribution(new_world)

        # calculate MH acceptance probability
        # log P(x, y)
        old_log_prob = world.log_prob()
        # log P(x', y)
        new_log_prob = new_world.log_prob()
        # log g(x'|x)
        forward_log_prob = forward_dist.log_prob(proposed_value).sum()
        # log g(x|x')
        backward_log_prob = backward_dist.log_prob(old_value).sum()

        # log [(P(x', y) * g(x|x')) / (P(x, y) * g(x'|x))]
        accept_log_prob = (
            new_log_prob + backward_log_prob - old_log_prob - forward_log_prob
        )
        # model size adjustment log (n/n')
        accept_log_prob += math.log(len(world)) - math.log(len(new_world))

        if torch.rand_like(accept_log_prob).log() < accept_log_prob:
            world = new_world
        return world

    @abstractmethod
    def get_proposal_distribution(self, world: SimpleWorld) -> dist.Distribution:
        """Return a probability distribution of moving self.node to a new value
        conditioned on its current value in world.
        """
        raise NotImplementedError