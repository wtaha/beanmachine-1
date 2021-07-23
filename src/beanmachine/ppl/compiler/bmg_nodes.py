# Copyright (c) Facebook, Inc. and its affiliates.

import collections
import functools
import itertools
import operator
from abc import ABC, ABCMeta
from typing import Any, Iterable, List

import beanmachine.ppl.compiler.bmg_types as bt
import torch
from beanmachine.ppl.utils.item_counter import ItemCounter
from torch import Tensor, tensor
from torch.distributions import Normal
from torch.distributions.utils import broadcast_all


def prod(x):
    """Compute the product of a sequence of values of arbitrary length"""
    return functools.reduce(operator.mul, x, 1)


positive_infinity = float("inf")


# Note that we're not going to subclass list or UserList here because we
# only need to use the most basic list operations: initialization, getting
# an item, and setting an item. We never want to delete items, append to
# the end, and so on.


class InputList:
    node: "BMGNode"
    inputs: List["BMGNode"]

    def __init__(self, node: "BMGNode", inputs: List["BMGNode"]) -> None:
        assert isinstance(inputs, list)
        self.node = node
        self.inputs = inputs
        for i in inputs:
            i.outputs.add_item(node)

    def __setitem__(self, index: int, value: "BMGNode") -> None:
        # If this is a no-op, do nothing.
        old_value = self.inputs[index]
        if old_value is value:
            return

        # Start by maintaining correctness of the input/output relationships.
        #
        # (1) The node is no longer an output of the current input at the index.
        # (2) The node is now an output of the new input at the index.
        #
        old_value.outputs.remove_item(self.node)
        self.inputs[index] = value
        value.outputs.add_item(self.node)

    def __getitem__(self, index: int) -> "BMGNode":
        return self.inputs[index]

    def __iter__(self):
        return iter(self.inputs)

    def __len__(self) -> int:
        return len(self.inputs)


class BMGNode(ABC):
    """The base class for all graph nodes."""

    # A Bayesian network is a acyclic graph in which each node represents
    # a value or operation; directed edges represent the inputs and
    # outputs of each node.
    #
    # We have a small nomenclature problem here; when describing the shape
    # of, say, a multiplication in an abstract syntax tree we would say that
    # the multiplication operator is the "parent" and the pair of operands
    # are the left and right "children".  However, in Bayesian networks
    # the tradition is to consider the input values as "parents" of the
    # multiplication, and nodes which consume the product are its "children".
    #
    # To avoid this confusion, in this class we will explicitly call out
    # that the edges represent inputs.

    inputs: InputList
    outputs: ItemCounter

    def __init__(self, inputs: List["BMGNode"]):
        assert isinstance(inputs, list)
        self.inputs = InputList(self, inputs)
        self.outputs = ItemCounter()

    @property
    def size(self) -> torch.Size:
        """The tensor size associated with this node.
        If the node represents a scalar value then produce Size([])."""
        raise NotImplementedError("size")

    def support(self) -> Iterable[Any]:
        """To build the graph of all possible control flows through
        the model we need to know for any given node what are
        all the possible values it could attain; we require that
        the set be finite and will throw an exception if it is not."""
        raise NotImplementedError("support")

    def support_size(self) -> float:
        # It can be expensive to construct the support if it is large
        # and we might wish to merely know how big it is.  By default
        # assume that every node has infinite support and override this
        # in nodes which have smaller support.
        #
        # Note that this is the *approximate* support size. For example,
        # if we have a Boolean node then its support size is two. If we
        # have the sum of two distinct Boolean nodes then the true size
        # of the support of the sum node is 3 because the result will be
        # 0, 1 or 2.  But we assume that there are two possibilities on
        # the left, two on the right, so four possible outcomes. We can
        # therefore over-estimate; we should however not under-estimate.
        return positive_infinity

    @property
    def is_leaf(self) -> bool:
        return len(self.outputs.items) == 0


# When constructing the support of various nodes we are often
# having to remove duplicates from a set of possible values.
# Unfortunately, it is not easy to do so with torch tensors.
# This helper class implements a set of tensors.

# TODO: Move this to its own module.


class SetOfTensors(collections.abc.Set):
    """Tensors cannot be put into a normal set because tensors that compare as
    equal do not hash to equal hashes. This is a linear-time set implementation.
    Most of the time the sets will be very small."""

    elements: List[Tensor]

    def __init__(self, iterable):
        self.elements = []
        for value in iterable:
            t = value if isinstance(value, Tensor) else tensor(value)
            if t not in self.elements:
                self.elements.append(t)

    def __iter__(self):
        return iter(self.elements)

    def __contains__(self, value):
        return value in self.elements

    def __len__(self):
        return len(self.elements)


# ####
# #### Nodes representing constant values
# ####


class ConstantNode(BMGNode, metaclass=ABCMeta):
    """This is the base type for all nodes representing constants.
    Note that every constant node has an associated type in the
    BMG type system; nodes that represent the "real" 1.0,
    the "positive real" 1.0, the "probability" 1.0 and the
    "natural" 1 are all different nodes and are NOT deduplicated."""

    value: Any

    def __init__(self):
        BMGNode.__init__(self, [])

    # The support of a constant is just the value.
    def support(self) -> Iterable[Any]:
        yield self.value

    def support_size(self) -> float:
        return 1.0


class UntypedConstantNode(ConstantNode):
    def __init__(self, value: Any) -> None:
        self.value = value
        ConstantNode.__init__(self)

    def __str__(self) -> str:
        return str(self.value)

    @property
    def size(self) -> torch.Size:
        if isinstance(self.value, torch.Tensor):
            return self.value.size()
        return torch.Size([])


class BooleanNode(ConstantNode):
    """A Boolean constant"""

    value: bool

    def __init__(self, value: bool):
        self.value = value
        ConstantNode.__init__(self)

    def __str__(self) -> str:
        return str(self.value)

    @property
    def size(self) -> torch.Size:
        return torch.Size([])


class NaturalNode(ConstantNode):
    """An integer constant restricted to non-negative values"""

    value: int

    def __init__(self, value: int):
        self.value = value
        ConstantNode.__init__(self)

    def __str__(self) -> str:
        return str(self.value)

    @property
    def size(self) -> torch.Size:
        return torch.Size([])


class PositiveRealNode(ConstantNode):
    """A real constant restricted to non-negative values"""

    value: float

    def __init__(self, value: float):
        self.value = value
        ConstantNode.__init__(self)

    def __str__(self) -> str:
        return str(self.value)

    @property
    def size(self) -> torch.Size:
        return torch.Size([])


class NegativeRealNode(ConstantNode):
    """A real constant restricted to non-positive values"""

    value: float

    def __init__(self, value: float):
        self.value = value
        ConstantNode.__init__(self)

    def __str__(self) -> str:
        return str(self.value)

    @property
    def size(self) -> torch.Size:
        return torch.Size([])


class ProbabilityNode(ConstantNode):
    """A real constant restricted to values from 0.0 to 1.0"""

    value: float

    def __init__(self, value: float):
        self.value = value
        ConstantNode.__init__(self)

    def __str__(self) -> str:
        return str(self.value)

    @property
    def size(self) -> torch.Size:
        return torch.Size([])


class RealNode(ConstantNode):
    """An unrestricted real constant"""

    value: float

    def __init__(self, value: float):
        self.value = value
        ConstantNode.__init__(self)

    def __str__(self) -> str:
        return str(self.value)

    @property
    def size(self) -> torch.Size:
        return torch.Size([])


class ConstantTensorNode(ConstantNode):
    """A tensor constant"""

    value: Tensor

    def __init__(self, value: Tensor):
        self.value = value
        ConstantNode.__init__(self)

    def __str__(self) -> str:
        return str(self.value)

    @property
    def size(self) -> torch.Size:
        return self.value.size()


class ConstantPositiveRealMatrixNode(ConstantTensorNode):
    def __init__(self, value: Tensor):
        assert len(value.size()) <= 2
        ConstantTensorNode.__init__(self, value)


class ConstantRealMatrixNode(ConstantTensorNode):
    def __init__(self, value: Tensor):
        assert len(value.size()) <= 2
        ConstantTensorNode.__init__(self, value)


class ConstantNegativeRealMatrixNode(ConstantTensorNode):
    def __init__(self, value: Tensor):
        assert len(value.size()) <= 2
        ConstantTensorNode.__init__(self, value)


class ConstantProbabilityMatrixNode(ConstantTensorNode):
    def __init__(self, value: Tensor):
        assert len(value.size()) <= 2
        ConstantTensorNode.__init__(self, value)


class ConstantNaturalMatrixNode(ConstantTensorNode):
    def __init__(self, value: Tensor):
        assert len(value.size()) <= 2
        ConstantTensorNode.__init__(self, value)


class ConstantBooleanMatrixNode(ConstantTensorNode):
    def __init__(self, value: Tensor):
        assert len(value.size()) <= 2
        ConstantTensorNode.__init__(self, value)


class TensorNode(BMGNode):
    """A tensor whose elements are graph nodes."""

    _size: torch.Size

    def __init__(self, items: List[BMGNode], size: torch.Size):
        assert isinstance(items, list)
        self._size = size
        BMGNode.__init__(self, items)

    def __str__(self) -> str:
        return "TensorNode"

    @property
    def size(self) -> torch.Size:
        return self._size

    def support(self) -> Iterable[Any]:
        s = self.size
        return (
            tensor(c).view(s)
            for c in itertools.product(*(i.support() for i in self.inputs))
        )

    def support_size(self) -> float:
        return prod(i.support_size() for i in self.inputs)


# ####
# #### Nodes representing distributions
# ####


class DistributionNode(BMGNode, metaclass=ABCMeta):
    """This is the base class for all nodes that represent
    probability distributions."""

    def __init__(self, inputs: List[BMGNode]):
        BMGNode.__init__(self, inputs)


class BernoulliBase(DistributionNode):
    def __init__(self, probability: BMGNode):
        DistributionNode.__init__(self, [probability])

    @property
    def probability(self) -> BMGNode:
        return self.inputs[0]

    @property
    def size(self) -> torch.Size:
        return self.probability.size

    def support(self) -> Iterable[Any]:
        s = self.size
        return (tensor(i).view(s) for i in itertools.product(*([[0.0, 1.0]] * prod(s))))

    def support_size(self) -> float:
        return 2.0 ** prod(self.size)


class BernoulliNode(BernoulliBase):
    """The Bernoulli distribution is a coin flip; it takes
    a probability and each sample is either 0.0 or 1.0."""

    def __init__(self, probability: BMGNode):
        BernoulliBase.__init__(self, probability)

    def __str__(self) -> str:
        return "Bernoulli(" + str(self.probability) + ")"


class BernoulliLogitNode(BernoulliBase):
    """The Bernoulli distribution is a coin flip; it takes
    a probability and each sample is either 0.0 or 1.0."""

    def __init__(self, probability: BMGNode):
        BernoulliBase.__init__(self, probability)

    def __str__(self) -> str:
        return "Bernoulli(" + str(self.probability) + ")"


class BetaNode(DistributionNode):
    """The beta distribution samples are values between 0.0 and 1.0, and
    so is useful for creating probabilities."""

    def __init__(self, alpha: BMGNode, beta: BMGNode):
        DistributionNode.__init__(self, [alpha, beta])

    @property
    def alpha(self) -> BMGNode:
        return self.inputs[0]

    @property
    def beta(self) -> BMGNode:
        return self.inputs[1]

    @property
    def size(self) -> torch.Size:
        return self.alpha.size

    def __str__(self) -> str:
        return f"Beta({str(self.alpha)},{str(self.beta)})"

    def support(self) -> Iterable[Any]:
        # TODO: Make a better exception type.
        # TODO: Catch this error during graph generation and produce a better
        # TODO: error message that diagnoses the problem more exactly for
        # TODO: the user.  This would happen if we did something like
        # TODO: x(n()) where x() is a sample that takes a finite index but
        # TODO: n() is a sample that returns a beta.
        raise ValueError("Beta distribution does not have finite support.")


class PoissonNode(DistributionNode):
    """The Poisson distribution samples are non-negative integer valued."""

    def __init__(self, rate: BMGNode):
        DistributionNode.__init__(self, [rate])

    @property
    def rate(self) -> BMGNode:
        return self.inputs[0]

    @property
    def size(self) -> torch.Size:
        return self.rate.size

    def __str__(self) -> str:
        return f"Poisson({str(self.rate)})"

    def support(self) -> Iterable[Any]:
        # TODO: Make a better exception type.
        # TODO: Catch this error during graph generation and produce a better
        # TODO: error message that diagnoses the problem more exactly for
        # TODO: the user.  This would happen if we did something like
        # TODO: x(n()) where x() is a sample that takes a finite index but
        # TODO: n() is a sample that returns a Poisson.
        raise ValueError("Poisson distribution does not have finite support.")


class BinomialNodeBase(DistributionNode):
    def __init__(self, count: BMGNode, probability: BMGNode):
        DistributionNode.__init__(self, [count, probability])

    @property
    def count(self) -> BMGNode:
        return self.inputs[0]

    @property
    def probability(self) -> BMGNode:
        return self.inputs[1]

    @property
    def size(self) -> torch.Size:
        return broadcast_all(
            torch.zeros(self.count.size), torch.zeros(self.probability.size)
        ).size()

    def __str__(self) -> str:
        return f"Binomial({self.count}, {self.probability})"

    # TODO: We will need to implement computation of the support
    # of an arbitrary binomial distribution because samples are
    # discrete values between 0 and count, which is typically small.
    # Though implementing support computation if count is non-stochastic
    # is straightforward, we do not yet have the gear to implement
    # this for stochastic counts. Consider this contrived case:
    #
    # @bm.random_variable def a(): return Binomial(2, 0.5)
    # @bm.random_variable def b(): return Binomial(a() + 1, 0.4)
    # @bm.random_variable def c(i): return Normal(0.0, 2.0)
    # @bm.random_variable def d(): return Normal(c(b()), 3.0)
    #
    # The support of a() is 0, 1, 2 -- easy.
    #
    # We need to know the support of b() in order to build the
    # graph for d(). But how do we know the support of b()?
    #
    # What we must do is compute that the maximum possible value
    # for a() + 1 is 3, and so the support of b() is 0, 1, 2, 3,
    # and therefore there are four samples of c(i) generated.
    #
    # There are two basic ways to do this that immediately come to
    # mind.
    #
    # The first is to simply ask the graph for the support of
    # a() + 1, which we can generate, and then take the maximum
    # value thus generated.
    #
    # If that turns out to be too expensive for some reason then
    # we can write a bit of code that answers the question
    # "what is the maximum value of your support?" and have each
    # node implement that. However, that then introduces new
    # problems; to compute the maximum value of a negation, for
    # instance, we then would also need to answer the question
    # "what is the minimum value you support?" and so on.
    def support(self) -> Iterable[Any]:
        raise ValueError("Support of binomial is not yet implemented.")


class BinomialNode(BinomialNodeBase):
    """The Binomial distribution is the extension of the
    Bernoulli distribution to multiple flips. The input
    is the count of flips and the probability of each
    coming up heads; each sample is the number of heads
    after "count" flips."""

    def __init__(self, count: BMGNode, probability: BMGNode, is_logits: bool = False):
        BinomialNodeBase.__init__(self, count, probability)


class BinomialLogitNode(BinomialNodeBase):
    """The Binomial distribution is the extension of the
    Bernoulli distribution to multiple flips. The input
    is the count of flips and the probability of each
    coming up heads; each sample is the number of heads
    after "count" flips."""

    # TODO: We do not yet have a BMG node for Binomial
    # with logits. When we do, add support for it.

    def __init__(self, count: BMGNode, probability: BMGNode):
        BinomialNodeBase.__init__(self, count, probability)


class CategoricalNodeBase(DistributionNode):
    """The categorical distribution is the extension of the
    Bernoulli distribution to multiple outcomes; rather
    than flipping an unfair coin, this is rolling an unfair
    n-sided die.

    The input is the probability of each of n possible outcomes,
    and each sample is drawn from 0, 1, 2, ... n-1."""

    # TODO: we may wish to add bounded integers to the BMG type system.

    def __init__(self, probability: BMGNode):
        DistributionNode.__init__(self, [probability])

    @property
    def probability(self) -> BMGNode:
        return self.inputs[0]

    def __str__(self) -> str:
        return "Categorical(" + str(self.probability) + ")"

    def support(self) -> Iterable[Any]:
        # TODO: Raise an exception if probability is not one-dimensional.
        s = self.probability.size
        r = list(range(s[-1]))
        sr = s[:-1]
        return (tensor(i).view(sr) for i in itertools.product(*([r] * prod(sr))))

    def support_size(self) -> float:
        # TODO: Raise an exception if probability is not one-dimensional.
        s = self.probability.size
        return s[-1] ** prod(s[:-1])


class CategoricalNode(CategoricalNodeBase):
    def __init__(self, probability: BMGNode):
        DistributionNode.__init__(self, [probability])


class CategoricalLogitNode(CategoricalNodeBase):
    def __init__(self, probability: BMGNode):
        DistributionNode.__init__(self, [probability])


class Chi2Node(DistributionNode):
    """The chi2 distribution is a distribution of positive
    real numbers; it is a special case of the gamma distribution."""

    def __init__(self, df: BMGNode):
        DistributionNode.__init__(self, [df])

    @property
    def df(self) -> BMGNode:
        return self.inputs[0]

    @property
    def size(self) -> torch.Size:
        return self.df.size

    def __str__(self) -> str:
        return f"Chi2({str(self.df)})"

    def support(self) -> Iterable[Any]:
        # TODO: Make a better exception type.
        # TODO: Catch this error during graph generation and produce a better
        # TODO: error message that diagnoses the problem more exactly for
        # TODO: the user.  This would happen if we did something like
        # TODO: x(n()) where x() is a sample that takes a finite index but
        # TODO: n() is a sample that returns a Chi2.
        raise ValueError("Chi2 distribution does not have finite support.")


class DirichletNode(DistributionNode):
    """The Dirichlet distribution generates simplexs -- vectors
    whose members are probabilities that add to 1.0, and
    so it is useful for generating inputs to the categorical
    distribution."""

    def __init__(self, concentration: BMGNode):
        DistributionNode.__init__(self, [concentration])

    @property
    def concentration(self) -> BMGNode:
        return self.inputs[0]

    # TODO: Rename this required_rows or required_length
    @property
    def _required_columns(self) -> int:
        # The "max" is needed to handle the degenerate case of
        # Dirichlet(tensor([])) -- in this case we will say that we require
        # a single positive real and that the requirement cannot be met.
        size = self.size
        dimensions = len(size)
        return max(1, size[dimensions - 1]) if dimensions > 0 else 1

    @property
    def size(self) -> torch.Size:
        return self.concentration.size

    def __str__(self) -> str:
        return f"Dirichlet({str(self.concentration)})"

    def support(self) -> Iterable[Any]:
        # TODO: Make a better exception type.
        # TODO: Catch this error during graph generation and produce a better
        # TODO: error message that diagnoses the problem more exactly for
        # TODO: the user.  This would happen if we did something like
        # TODO: x(n()) where x() is a sample that takes a finite index but
        # TODO: n() is a sample that returns a Dirichlet.
        raise ValueError("Dirichlet distribution does not have finite support.")


class FlatNode(DistributionNode):

    """The Flat distribution the standard uniform distribution from 0.0 to 1.0."""

    def __init__(self):
        DistributionNode.__init__(self, [])

    @property
    def size(self) -> torch.Size:
        return torch.Size([])

    def __str__(self) -> str:
        return "Flat()"

    def support(self) -> Iterable[Any]:
        raise ValueError("Flat distribution does not have finite support.")


class GammaNode(DistributionNode):
    """The gamma distribution is a distribution of positive
    real numbers characterized by positive real concentration and rate
    parameters."""

    def __init__(self, concentration: BMGNode, rate: BMGNode):
        DistributionNode.__init__(self, [concentration, rate])

    @property
    def concentration(self) -> BMGNode:
        return self.inputs[0]

    @property
    def rate(self) -> BMGNode:
        return self.inputs[1]

    @property
    def size(self) -> torch.Size:
        return self.concentration.size

    def __str__(self) -> str:
        return f"Gamma({str(self.concentration)}, {str(self.rate)})"

    def support(self) -> Iterable[Any]:
        # TODO: Make a better exception type.
        # TODO: Catch this error during graph generation and produce a better
        # TODO: error message that diagnoses the problem more exactly for
        # TODO: the user.  This would happen if we did something like
        # TODO: x(n()) where x() is a sample that takes a finite index but
        # TODO: n() is a sample that returns a Gamma.
        raise ValueError("Gamma distribution does not have finite support.")


class HalfCauchyNode(DistributionNode):
    """The Cauchy distribution is a bell curve with zero mean
    and a heavier tail than the normal distribution; it is useful
    for generating samples that are not as clustered around
    the mean as a normal.

    The half Cauchy distribution is just the distribution you
    get when you take the absolute value of the samples from
    a Cauchy distribution. The input is a positive scale factor
    and a sample is a positive real number."""

    # TODO: Add support for the Cauchy distribution as well.

    def __init__(self, scale: BMGNode):
        DistributionNode.__init__(self, [scale])

    @property
    def scale(self) -> BMGNode:
        return self.inputs[0]

    @property
    def size(self) -> torch.Size:
        return self.scale.size

    def __str__(self) -> str:
        return f"HalfCauchy({str(self.scale)})"

    def support(self) -> Iterable[Any]:
        # TODO: Make a better exception type.
        # TODO: Catch this error during graph generation and produce a better
        # TODO: error message that diagnoses the problem more exactly for
        # TODO: the user.  This would happen if we did something like
        # TODO: x(n()) where x() is a sample that takes a finite index but
        # TODO: n() is a sample that returns a half Cauchy.
        raise ValueError("HalfCauchy distribution does not have finite support.")


class NormalNode(DistributionNode):

    """The normal (or "Gaussian") distribution is a bell curve with
    a given mean and standard deviation."""

    def __init__(self, mu: BMGNode, sigma: BMGNode):
        DistributionNode.__init__(self, [mu, sigma])

    @property
    def mu(self) -> BMGNode:
        return self.inputs[0]

    @property
    def sigma(self) -> BMGNode:
        return self.inputs[1]

    @property
    def size(self) -> torch.Size:
        return self.mu.size

    def __str__(self) -> str:
        return f"Normal({str(self.mu)},{str(self.sigma)})"

    def support(self) -> Iterable[Any]:
        # TODO: Make a better exception type.
        # TODO: Catch this error during graph generation and produce a better
        # TODO: error message that diagnoses the problem more exactly for
        # TODO: the user.  This would happen if we did something like
        # TODO: x(n()) where x() is a sample that takes a finite index but
        # TODO: n() is a sample that returns a normal.
        raise ValueError("Normal distribution does not have finite support.")


class HalfNormalNode(DistributionNode):

    """The half-normal distribution is a half bell curve with
    a given standard deviation. Mean (for the underlying normal)
    is taken to be zero."""

    def __init__(self, sigma: BMGNode):
        DistributionNode.__init__(self, [sigma])

    @property
    def sigma(self) -> BMGNode:
        return self.inputs[0]

    @property
    def size(self) -> torch.Size:
        return self.sigma.size

    def __str__(self) -> str:
        return f"HalfNormal({str(self.sigma)})"

    def support(self) -> Iterable[Any]:
        # TODO: Make a better exception type.
        # TODO: Catch this error during graph generation and produce a better
        # TODO: error message that diagnoses the problem more exactly for
        # TODO: the user.  This would happen if we did something like
        # TODO: x(n()) where x() is a sample that takes a finite index but
        # TODO: n() is a sample that returns a half normal.
        raise ValueError("HalfNormal distribution does not have finite support.")


class StudentTNode(DistributionNode):
    """The Student T distribution is a bell curve with zero mean
    and a heavier tail than the normal distribution. It is
    useful in statistical analysis because a common situation
    is to have observations of a normal process but to not
    know the true mean. Samples from the T distribution can
    be used to represent the difference between an observed mean
    and the true mean."""

    def __init__(self, df: BMGNode, loc: BMGNode, scale: BMGNode):
        DistributionNode.__init__(self, [df, loc, scale])

    @property
    def df(self) -> BMGNode:
        return self.inputs[0]

    @property
    def loc(self) -> BMGNode:
        return self.inputs[1]

    @property
    def scale(self) -> BMGNode:
        return self.inputs[2]

    @property
    def size(self) -> torch.Size:
        return self.df.size

    def __str__(self) -> str:
        return f"StudentT({str(self.df)},{str(self.loc)},{str(self.scale)})"

    def support(self) -> Iterable[Any]:
        # TODO: Make a better exception type.
        # TODO: Catch this error during graph generation and produce a better
        # TODO: error message that diagnoses the problem more exactly for
        # TODO: the user.  This would happen if we did something like
        # TODO: x(n()) where x() is a sample that takes a finite index but
        # TODO: n() is a sample that returns a student t.
        raise ValueError("StudentT distribution does not have finite support.")


class UniformNode(DistributionNode):

    """The Uniform distribution is a "flat" distribution of values
    between 0.0 and 1.0."""

    # TODO: We do not yet have an implementation of the uniform
    # distribution as a BMG node. When we do, implement the
    # feature here.

    def __init__(self, low: BMGNode, high: BMGNode):
        DistributionNode.__init__(self, [low, high])

    @property
    def low(self) -> BMGNode:
        return self.inputs[0]

    @property
    def high(self) -> BMGNode:
        return self.inputs[1]

    @property
    def size(self) -> torch.Size:
        return self.low.size

    def __str__(self) -> str:
        return f"Uniform({str(self.low)},{str(self.high)})"

    def support(self) -> Iterable[Any]:
        # TODO: Make a better exception type.
        # TODO: Catch this error during graph generation and produce a better
        # TODO: error message that diagnoses the problem more exactly for
        # TODO: the user.  This would happen if we did something like
        # TODO: x(n()) where x() is a sample that takes a finite index but
        # TODO: n() is a sample that returns a uniform.
        raise ValueError("Uniform distribution does not have finite support.")


# ####
# #### Operators
# ####


class OperatorNode(BMGNode, metaclass=ABCMeta):
    """This is the base class for all operators.
    The inputs are the operands of each operator."""

    def __init__(self, inputs: List[BMGNode]):
        assert isinstance(inputs, list)
        BMGNode.__init__(self, inputs)


# ####
# #### Multiary operators
# ####


class MultiAdditionNode(OperatorNode):
    """This represents an addition of values."""

    # TODO: Consider a base class for multi add, logsumexp, and so on.

    def __init__(self, inputs: List[BMGNode]):
        assert isinstance(inputs, list)
        OperatorNode.__init__(self, inputs)

    @property
    def size(self) -> torch.Size:
        return self.inputs[0].size

    def support(self) -> Iterable[Any]:
        raise ValueError("support of multiary addition not yet implemented")

    def __str__(self) -> str:
        return "MultiAdd"


class MultiMultiplicationNode(OperatorNode):
    """This represents multiplication of values."""

    # TODO: Consider a base class for multi add, logsumexp, and so on.

    def __init__(self, inputs: List[BMGNode]):
        assert isinstance(inputs, list)
        OperatorNode.__init__(self, inputs)

    @property
    def size(self) -> torch.Size:
        return self.inputs[0].size

    def support(self) -> Iterable[Any]:
        raise ValueError("support of multiary multiplication not yet implemented")

    def __str__(self) -> str:
        return "MultiMultiplication"


# We have three kinds of logsumexp nodes.
#
# * LogSumExpTorchNode represents a call to logsumexp in the original
#   Python model. It has three operands: the tensor being summed,
#   the dimension along which it is summed, and a flag giving the shape.
#
# * LogSumExpNode represents a BMG LOGSUMEXP node. It is an n-ary operator
#   and produces a real; each of the inputs is one of the summands.
#
# * LogSumExpVectorNode represents a BMG LOGSUMEXP_VECTOR node. It is a unary
#   operator that takes a single-column matrix.
#
# We transform LogSumExpTorchNode into LogSumExpNode or LogSumExpVectorNode
# as appropriate.


class LogSumExpTorchNode(OperatorNode):
    def __init__(self, operand: BMGNode, dim: BMGNode, keepdim: BMGNode):
        OperatorNode.__init__(self, [operand, dim, keepdim])

    @property
    def size(self) -> torch.Size:
        # TODO
        raise NotImplementedError("LogSumExpTorchNode.size")

    def __str__(self) -> str:
        return "LogSumExp"

    def support(self) -> Iterable[Any]:
        raise NotImplementedError("support of LogSumExp not yet implemented")


class LogSumExpNode(OperatorNode):
    """This class represents the LogSumExp operation: for values v_1, ..., v_n
    we compute log(exp(v_1) + ... + exp(v_n))"""

    def __init__(self, inputs: List[BMGNode]):
        assert isinstance(inputs, list)
        OperatorNode.__init__(self, inputs)

    @property
    def size(self) -> torch.Size:
        raise NotImplementedError("LogSumExpTorchNode.size")

    def __str__(self) -> str:
        return "LogSumExp"

    def support(self) -> Iterable[Any]:
        raise NotImplementedError("support of LogSumExp not yet implemented")


class ToMatrixNode(OperatorNode):
    """A 2-d tensor whose elements are graph nodes."""

    def __init__(self, rows: NaturalNode, columns: NaturalNode, items: List[BMGNode]):
        # The first two elements are the row and column counts; they must
        # be constant naturals.
        assert isinstance(items, list)
        assert len(items) >= 1
        rc: List[BMGNode] = [rows, columns]
        BMGNode.__init__(self, rc + items)

    def __str__(self) -> str:
        return "ToMatrix"

    @property
    def size(self) -> torch.Size:
        rows = self.inputs[0]
        assert isinstance(rows, NaturalNode)
        columns = self.inputs[1]
        assert isinstance(columns, NaturalNode)
        return torch.Size([rows.value, columns.value])

    def support(self) -> Iterable[Any]:
        raise NotImplementedError()

    def support_size(self) -> float:
        raise NotImplementedError()


# ####
# #### Ternary operators
# ####


class IfThenElseNode(OperatorNode):
    """This class represents a stochastic choice between two options, where
    the condition is a Boolean."""

    # This node will only be generated when tranforming the Python version of
    # the graph into the BMG format; for instance, if we have a multiplication
    # of a Bernoulli sample node by 2.0, in the Python form we'll have a scalar
    # multiplied by a sample of type tensor. In the BMG form the sample will be
    # of type Boolean and we cannot multiply a Boolean by a Real. Instead we'll
    # generate "if_then_else(sample, 0.0, 1.0) * 2.0" which typechecks in the
    # BMG type system.
    #
    # Eventually we will probably use this node to represent Python's
    # "consequence if condition else alternative" syntax, and possibly
    # other conditional stochastic control flows.

    def __init__(self, condition: BMGNode, consequence: BMGNode, alternative: BMGNode):
        OperatorNode.__init__(self, [condition, consequence, alternative])

    @property
    def condition(self) -> BMGNode:
        return self.inputs[0]

    @property
    def consequence(self) -> BMGNode:
        return self.inputs[1]

    @property
    def alternative(self) -> BMGNode:
        return self.inputs[2]

    @property
    def size(self) -> torch.Size:
        return torch.Size([])

    def __str__(self) -> str:
        i = str(self.condition)
        t = str(self.consequence)
        e = str(self.alternative)
        return f"(if {i} then {t} else {e})"

    def support(self) -> Iterable[Any]:
        raise ValueError("support of IfThenElseNode not yet implemented")


# ####
# #### Binary operators
# ####


class BinaryOperatorNode(OperatorNode, metaclass=ABCMeta):
    """This is the base class for all binary operators."""

    def __init__(self, left: BMGNode, right: BMGNode):
        OperatorNode.__init__(self, [left, right])

    @property
    def left(self) -> BMGNode:
        return self.inputs[0]

    @property
    def right(self) -> BMGNode:
        return self.inputs[1]

    def support_size(self) -> float:
        return self.left.support_size() * self.right.support_size()


class ComparisonNode(BinaryOperatorNode, metaclass=ABCMeta):
    """This is the base class for all comparison operators."""

    def __init__(self, left: BMGNode, right: BMGNode):
        BinaryOperatorNode.__init__(self, left, right)

    @property
    def size(self) -> torch.Size:
        return (torch.zeros(self.left.size) < torch.zeros(self.right.size)).size()

    def support_size(self) -> float:
        return 2.0 ** prod(self.size)


class GreaterThanNode(ComparisonNode):
    def __init__(self, left: BMGNode, right: BMGNode):
        ComparisonNode.__init__(self, left, right)

    def support(self) -> Iterable[Any]:
        return SetOfTensors(
            el > ar for el in self.left.support() for ar in self.right.support()
        )

    def __str__(self) -> str:
        return f"({str(self.left)}>{str(self.right)})"


class GreaterThanEqualNode(ComparisonNode):
    def __init__(self, left: BMGNode, right: BMGNode):
        ComparisonNode.__init__(self, left, right)

    def support(self) -> Iterable[Any]:
        return SetOfTensors(
            el >= ar for el in self.left.support() for ar in self.right.support()
        )

    def __str__(self) -> str:
        return f"({str(self.left)}>={str(self.right)})"


class LessThanNode(ComparisonNode):
    def __init__(self, left: BMGNode, right: BMGNode):
        ComparisonNode.__init__(self, left, right)

    def support(self) -> Iterable[Any]:
        return SetOfTensors(
            el < ar for el in self.left.support() for ar in self.right.support()
        )

    def __str__(self) -> str:
        return f"({str(self.left)}<{str(self.right)})"


class LessThanEqualNode(ComparisonNode):
    def __init__(self, left: BMGNode, right: BMGNode):
        ComparisonNode.__init__(self, left, right)

    def support(self) -> Iterable[Any]:
        return SetOfTensors(
            el <= ar for el in self.left.support() for ar in self.right.support()
        )

    def __str__(self) -> str:
        return f"({str(self.left)}<={str(self.right)})"


class EqualNode(ComparisonNode):
    def __init__(self, left: BMGNode, right: BMGNode):
        ComparisonNode.__init__(self, left, right)

    def support(self) -> Iterable[Any]:
        return SetOfTensors(
            el == ar for el in self.left.support() for ar in self.right.support()
        )

    def __str__(self) -> str:
        return f"({str(self.left)}=={str(self.right)})"


class NotEqualNode(ComparisonNode):
    def __init__(self, left: BMGNode, right: BMGNode):
        ComparisonNode.__init__(self, left, right)

    def support(self) -> Iterable[Any]:
        return SetOfTensors(
            el != ar for el in self.left.support() for ar in self.right.support()
        )

    def __str__(self) -> str:
        return f"({str(self.left)}!={str(self.right)})"


class IsNode(ComparisonNode):
    def __init__(self, left: BMGNode, right: BMGNode):
        ComparisonNode.__init__(self, left, right)


class IsNotNode(ComparisonNode):
    def __init__(self, left: BMGNode, right: BMGNode):
        ComparisonNode.__init__(self, left, right)


class InNode(ComparisonNode):
    def __init__(self, left: BMGNode, right: BMGNode):
        ComparisonNode.__init__(self, left, right)


class NotInNode(ComparisonNode):
    def __init__(self, left: BMGNode, right: BMGNode):
        ComparisonNode.__init__(self, left, right)


class AdditionNode(BinaryOperatorNode):
    """This represents an addition of values."""

    def __init__(self, left: BMGNode, right: BMGNode):
        BinaryOperatorNode.__init__(self, left, right)

    @property
    def size(self) -> torch.Size:
        return (torch.zeros(self.left.size) + torch.zeros(self.right.size)).size()

    def __str__(self) -> str:
        return "(" + str(self.left) + "+" + str(self.right) + ")"

    def support(self) -> Iterable[Any]:
        return SetOfTensors(
            el + ar for el in self.left.support() for ar in self.right.support()
        )


class BitAndNode(BinaryOperatorNode):
    def __init__(self, left: BMGNode, right: BMGNode):
        BinaryOperatorNode.__init__(self, left, right)


class BitOrNode(BinaryOperatorNode):
    def __init__(self, left: BMGNode, right: BMGNode):
        BinaryOperatorNode.__init__(self, left, right)


class BitXorNode(BinaryOperatorNode):
    def __init__(self, left: BMGNode, right: BMGNode):
        BinaryOperatorNode.__init__(self, left, right)


class DivisionNode(BinaryOperatorNode):
    """This represents a division."""

    # There is no division node in BMG; we will replace
    # x / y with x * (y ** (-1)) during the "fix problems"
    # phase.

    def __init__(self, left: BMGNode, right: BMGNode):
        BinaryOperatorNode.__init__(self, left, right)

    @property
    def size(self) -> torch.Size:
        return (torch.zeros(self.left.size) / torch.zeros(self.right.size)).size()

    def __str__(self) -> str:
        return "(" + str(self.left) + "/" + str(self.right) + ")"

    def support(self) -> Iterable[Any]:
        # TODO: Filter out division by zero?
        return SetOfTensors(
            el / ar for el in self.left.support() for ar in self.right.support()
        )


class FloorDivNode(BinaryOperatorNode):
    def __init__(self, left: BMGNode, right: BMGNode):
        BinaryOperatorNode.__init__(self, left, right)


class LShiftNode(BinaryOperatorNode):
    def __init__(self, left: BMGNode, right: BMGNode):
        BinaryOperatorNode.__init__(self, left, right)


class ModNode(BinaryOperatorNode):
    def __init__(self, left: BMGNode, right: BMGNode):
        BinaryOperatorNode.__init__(self, left, right)


class RShiftNode(BinaryOperatorNode):
    def __init__(self, left: BMGNode, right: BMGNode):
        BinaryOperatorNode.__init__(self, left, right)


class MapNode(BMGNode):

    """This class represents a point in a program where there are
    multiple control flows based on the value of a stochastic node."""

    # For example, suppose we have this contrived model:
    #
    #   @bm.random_variable def weird(i):
    #     if i == 0:
    #       return Normal(0.0, 1.0)
    #     return Normal(1.0, 1.0)
    #
    #   @bm.random_variable def flips():
    #     return Binomial(2, 0.5)
    #
    #   @bm.random_variable def really_weird():
    #     return Normal(weird(flips()), 1.0)
    #
    # There are three possibilities for weird(flips()) on the last line;
    # what we need to represent in the graph is:
    #
    # * sample once from Normal(0.0, 1.0), call this weird(0)
    # * sample twice from Normal(1.0, 1.0), call these weird(1) and weird(2)
    # * sample once from flips()
    # * choose one of weird(i) based on the sample from flips().
    #
    # We represent this with two nodes: a map and an index:
    #
    # sample --- Normal(_, 1.0)        ---0--- sample --- Normal(0.0, 1.0)
    #                    \           /
    #                   index ---> map----1--- sample --- Normal(1.0, 1.0)
    #                        \       \                   /
    #                         \        ---2--- sample --
    #                          \
    #                            --- sample -- Binomial(2, 0.5)
    #
    # As an implementation detail, we represent the key-value pairs in the
    # map by a convention:
    #
    # * Even numbered inputs are keys
    # * All keys are constant nodes
    # * Odd numbered inputs are values associated with the previous
    #   sibling as the key.

    # TODO: We do not yet have this choice node in BMG, and the design
    # is not yet settled.
    #
    # The accumulator creates the map based on the actual values seen
    # as indices in the execution of the model; in the contrived example
    # above the indices are 0, 1, 2 but there is no reason why they could
    # not have been 1, 10, 100 instead; all that matters is that there
    # were three of them and so three code paths were explored.
    #
    # That's why this is implemented as (and named) "map"; it is an arbitrary
    # collection of key-value pairs where the keys are drawn from the support
    # of a distribution.
    #
    # The design decision to be made here is whether we need an arbitrary map
    # node in BMG, as we accumulate here, or if we need the more restricted
    # case of an "array" or "list", where we are mapping 0, 1, 2, ... n-1
    # to n graph nodes, and the indexed sample is drawn from a distribution
    # whose support is exactly 0 to n-1.

    def __init__(self, inputs: List[BMGNode]):
        # TODO: Check that keys are all constant nodes.
        # TODO: Check that there is one value for each key.
        # TODO: Verify that there is at least one pair.
        BMGNode.__init__(self, inputs)

    @property
    def size(self) -> torch.Size:
        return self.inputs[1].size

    def support(self) -> Iterable[Any]:
        return []

    # TODO: The original plan was to represent Python values such as
    # lists, tuples and dictionaries as one of these map nodes,
    # and it was convenient during prototyping that a map node
    # have an indexer that behaved like the Python indexer it was
    # emulating. This idea has been abandoned, so this code can
    # be deleted in a cleanup pass.

    def __getitem__(self, key) -> BMGNode:
        if isinstance(key, BMGNode) and not isinstance(key, ConstantNode):
            raise ValueError("BeanMachine map must be indexed with a constant value")
        # Linear search is fine.  We're not going to do this a lot, and the
        # maps will be small.
        k = key.value if isinstance(key, ConstantNode) else key
        for i in range(len(self.inputs) // 2):
            c = self.inputs[i * 2]
            assert isinstance(c, ConstantNode)
            if c.value == k:
                return self.inputs[i * 2 + 1]
        raise ValueError("Key not found in map")


class IndexNodeDeprecated(BinaryOperatorNode):

    # TODO: The index / map node combination that we originally envisioned
    # does not work well with BMGs indexing operator; we will eventually
    # remove it. Until then, just mark it as deprecated to minimize
    # disruption while we get indexing support working.

    """This represents a stochastic choice of multiple options; the left
    operand must be a map, and the right is the stochastic value used to
    choose an element from the map."""

    # See notes on MapNode for an explanation of this code.

    def __init__(self, left: MapNode, right: BMGNode):
        BinaryOperatorNode.__init__(self, left, right)

    @property
    def size(self) -> torch.Size:
        return self.left.size

    def __str__(self) -> str:
        return str(self.left) + "[" + str(self.right) + "]"

    def support(self) -> Iterable[Any]:
        raise NotImplementedError()


# This represents an indexing operation in the original source code.
# It will be replaced by a VectorIndexNode or ColumnIndexNode in the
# problem fixing phase.
class IndexNode(BinaryOperatorNode):
    def __init__(self, left: BMGNode, right: BMGNode):
        BinaryOperatorNode.__init__(self, left, right)

    @property
    def size(self) -> torch.Size:
        raise NotImplementedError()

    def __str__(self) -> str:
        return str(self.left) + "[" + str(self.right) + "]"

    def support(self) -> Iterable[Any]:
        raise NotImplementedError("support of index operator not implemented")


class ItemNode(OperatorNode):
    """Represents torch.Tensor.item() conversion from tensor to scalar."""

    def __init__(self, operand: BMGNode):
        OperatorNode.__init__(self, [operand])

    @property
    def size(self) -> torch.Size:
        raise NotImplementedError()

    def __str__(self) -> str:
        return str(self.inputs[0]) + ".item()"

    def support(self) -> Iterable[Any]:
        return self.inputs[0].support()

    def support_size(self) -> float:
        return self.inputs[0].support_size()


class VectorIndexNode(BinaryOperatorNode):
    """This represents a stochastic index into a vector. The left operand
    is the vector and the right operand is the index."""

    def __init__(self, left: BMGNode, right: BMGNode):
        BinaryOperatorNode.__init__(self, left, right)

    @property
    def size(self) -> torch.Size:
        raise NotImplementedError()

    def __str__(self) -> str:
        return str(self.left) + "[" + str(self.right) + "]"

    def support(self) -> Iterable[Any]:
        raise NotImplementedError("support of index operator not implemented")


class ColumnIndexNode(BinaryOperatorNode):
    def __init__(self, left: BMGNode, right: BMGNode):
        BinaryOperatorNode.__init__(self, left, right)

    @property
    def size(self) -> torch.Size:
        raise NotImplementedError("size of column index operator not implemented")

    def __str__(self) -> str:
        return "ColumnIndex"

    def support(self) -> Iterable[Any]:
        raise NotImplementedError("support of column index operator not implemented")


class MatrixMultiplicationNode(BinaryOperatorNode):
    """This represents a matrix multiplication."""

    # TODO: We now have matrix multiplication in BMG; finish this implementation

    def __init__(self, left: BMGNode, right: BMGNode):
        BinaryOperatorNode.__init__(self, left, right)

    @property
    def size(self) -> torch.Size:
        return torch.zeros(self.left.size).mm(torch.zeros(self.right.size)).size()

    def __str__(self) -> str:
        return "(" + str(self.left) + "*" + str(self.right) + ")"

    def support(self) -> Iterable[Any]:
        return SetOfTensors(
            torch.mm(el, ar)
            for el in self.left.support()
            for ar in self.right.support()
        )


class MultiplicationNode(BinaryOperatorNode):
    """This represents a multiplication of nodes."""

    def __init__(self, left: BMGNode, right: BMGNode):
        BinaryOperatorNode.__init__(self, left, right)

    @property
    def size(self) -> torch.Size:
        return (torch.zeros(self.left.size) * torch.zeros(self.right.size)).size()

    def __str__(self) -> str:
        return "(" + str(self.left) + "*" + str(self.right) + ")"

    def support(self) -> Iterable[Any]:
        return SetOfTensors(
            el * ar for el in self.left.support() for ar in self.right.support()
        )


class PowerNode(BinaryOperatorNode):
    """This represents an x-to-the-y operation."""

    def __init__(self, left: BMGNode, right: BMGNode):
        BinaryOperatorNode.__init__(self, left, right)

    @property
    def size(self) -> torch.Size:
        return (torch.zeros(self.left.size) ** torch.zeros(self.right.size)).size()

    def __str__(self) -> str:
        return "(" + str(self.left) + "**" + str(self.right) + ")"

    def support(self) -> Iterable[Any]:
        return SetOfTensors(
            el ** ar for el in self.left.support() for ar in self.right.support()
        )


# ####
# #### Unary operators
# ####


class UnaryOperatorNode(OperatorNode, metaclass=ABCMeta):
    """This is the base type of unary operator nodes."""

    def __init__(self, operand: BMGNode):
        OperatorNode.__init__(self, [operand])

    @property
    def operand(self) -> BMGNode:
        return self.inputs[0]

    def support_size(self) -> float:
        return self.operand.support_size()


class ExpNode(UnaryOperatorNode):
    """This represents an exponentiation operation; it is generated when
    a model contains calls to Tensor.exp or math.exp."""

    def __init__(self, operand: BMGNode):
        UnaryOperatorNode.__init__(self, operand)

    @property
    def size(self) -> torch.Size:
        return self.operand.size

    def __str__(self) -> str:
        return "Exp(" + str(self.operand) + ")"

    def support(self) -> Iterable[Any]:
        return SetOfTensors(torch.exp(o) for o in self.operand.support())


class ExpM1Node(UnaryOperatorNode):
    """This represents the operation exp(x) - 1; it is generated when
    a model contains calls to Tensor.expm1."""

    # TODO: If we have exp(x) - 1 in the graph and x is known to be of type
    # positive real or negative real then the expression as a whole is of
    # type real. If we convert such expressions in the graph to expm1(x)
    # then we can make the type more specific, and also possibly reduce
    # the number of nodes in the graph.

    def __init__(self, operand: BMGNode):
        UnaryOperatorNode.__init__(self, operand)

    @property
    def size(self) -> torch.Size:
        return self.operand.size

    def __str__(self) -> str:
        return "ExpM1(" + str(self.operand) + ")"

    def support(self) -> Iterable[Any]:
        return SetOfTensors(torch.expm1(o) for o in self.operand.support())


class LogisticNode(UnaryOperatorNode):
    """This represents the operation 1/(1+exp(x)); it is generated when
    a model contains calls to Tensor.sigmoid."""

    def __init__(self, operand: BMGNode):
        UnaryOperatorNode.__init__(self, operand)

    @property
    def size(self) -> torch.Size:
        return self.operand.size

    def __str__(self) -> str:
        return "Logistic(" + str(self.operand) + ")"

    def support(self) -> Iterable[Any]:
        return SetOfTensors(torch.sigmoid(o) for o in self.operand.support())


class LogNode(UnaryOperatorNode):
    """This represents a log operation; it is generated when
    a model contains calls to Tensor.log or math.log."""

    def __init__(self, operand: BMGNode):
        UnaryOperatorNode.__init__(self, operand)

    @property
    def size(self) -> torch.Size:
        return self.operand.size

    def __str__(self) -> str:
        return "Log(" + str(self.operand) + ")"

    def support(self) -> Iterable[Any]:
        return SetOfTensors(torch.log(o) for o in self.operand.support())


# TODO: replace "log" with "log1mexp" as needed below and update defs


class Log1mexpNode(UnaryOperatorNode):
    """This represents a log1mexp operation; it is generated when
    a model contains calls to log1mexp or math_log1mexp."""

    def __init__(self, operand: BMGNode):
        UnaryOperatorNode.__init__(self, operand)

    @property
    def size(self) -> torch.Size:
        return self.operand.size

    def __str__(self) -> str:
        return "Log1mexp(" + str(self.operand) + ")"

    def support(self) -> Iterable[Any]:
        return SetOfTensors(torch.log(1 - torch.exp(o)) for o in self.operand.support())


# BMG supports three different kinds of negation:

# * The "complement" node with a Boolean operand has the semantics
#   of logical negation.  The input and output are both bool.
#
# * The "complement" node with a probability operand has the semantics
#   of (1 - p). The input and output are both probability.
#
# * The "negate" node has the semantics of (0 - x). The input must be
#   real, positive real or negative real, and the output is
#   real, negative real or positive real respectively.
#
# Note that there is no subtraction operator in BMG; to express x - y
# we generate nodes as though (x + (-y)) was written; that is, the
# sum of x and a real-number negation of y.
#
# This presents several problems when accumulating a graph while executing
# a Python model, and then turning said graph into a valid BMG, particularly
# during type analysis.
#
# Our strategy is:
#
# * When we accumulate the graph we will create nodes for addition
#   (AdditionNode), unary negation (NegationNode) and the "not"
#   operator (NotNode).  We will not generate "complement" nodes
#   directly from Python source.
#
# * After accumulating the graph we will do type analysis and use
#   that to drive a rewriting pass. The rewriting pass will perform
#   these tasks:
#
#   (1) "not" nodes whose operands are bool will be converted into
#       "complement" nodes.
#
#   (2) "not" nodes whose operands are not bool will produce an error.
#       (The "not" operator applied to a non-bool x in Python has the
#       semantics of "x == 0" and we do not have any way to represent
#       these semantics in BMG.
#
#   (3) Call a constant "one-like" if it is True, 1, 1.0, or a single-
#       valued tensor with a one-like value. If we have a one-like node,
#       call it 1 for short, then we will look for patterns in the
#       accumulated graph such as
#
#       1 + (-p)
#       (-p) + 1
#       -(p + -1)
#       -(-1 + p)
#
#       and replace them with "complement" nodes (where p is a probability or
#       Boolean expression).
#
#   (4) Other usages of binary + and unary - in the Python model will
#       be converted to BMG following the rules for addition and negation
#       in BMG: negation must be real valued, and so on.


class NegateNode(UnaryOperatorNode):

    """This represents a unary minus."""

    def __init__(self, operand: BMGNode):
        UnaryOperatorNode.__init__(self, operand)

    @property
    def size(self) -> torch.Size:
        return self.operand.size

    def __str__(self) -> str:
        return "-" + str(self.operand)

    def support(self) -> Iterable[Any]:
        return SetOfTensors(-o for o in self.operand.support())


class NotNode(UnaryOperatorNode):
    """This represents a logical not that appears in the Python model."""

    def __init__(self, operand: BMGNode):
        UnaryOperatorNode.__init__(self, operand)

    @property
    def size(self) -> torch.Size:
        return self.operand.size

    def __str__(self) -> str:
        return "not " + str(self.operand)

    def support(self) -> Iterable[Any]:
        return SetOfTensors(not o for o in self.operand.support())


class ComplementNode(UnaryOperatorNode):
    """This represents a complement of a Boolean or probability
    value."""

    # See notes above NegateNode for details

    def __init__(self, operand: BMGNode):
        UnaryOperatorNode.__init__(self, operand)

    @property
    def size(self) -> torch.Size:
        return self.operand.size

    def __str__(self) -> str:
        return "complement " + str(self.operand)

    def support(self) -> Iterable[Any]:
        # This should never be called because we never generate
        # a complement node while executing the model to accumulate
        # the graph.
        return [1 - p for p in self.operand.support()]


# This operator is not supported in BMG.  We accumulate it into
# the graph in order to produce a good error message.
class InvertNode(UnaryOperatorNode):
    """This represents a bit inversion (~)."""

    def __init__(self, operand: BMGNode):
        UnaryOperatorNode.__init__(self, operand)

    def __str__(self) -> str:
        return "~" + str(self.operand)


class PhiNode(UnaryOperatorNode):
    """This represents a phi operation; that is, the cumulative
    distribution function of the standard normal."""

    def __init__(self, operand: BMGNode):
        UnaryOperatorNode.__init__(self, operand)

    @property
    def size(self) -> torch.Size:
        return self.operand.size

    def __str__(self) -> str:
        return "Phi(" + str(self.operand) + ")"

    def support(self) -> Iterable[Any]:
        cdf = Normal(0.0, 1.0).cdf
        return SetOfTensors(cdf(o) for o in self.operand.support())


class SampleNode(UnaryOperatorNode):
    """This represents a single unique sample from a distribution;
    if a graph has two sample nodes both taking input from the same
    distribution, each sample is logically distinct. But if a graph
    has two nodes that both input from the same sample node, we must
    treat those two uses of the sample as though they had identical
    values."""

    def __init__(self, operand: DistributionNode):
        UnaryOperatorNode.__init__(self, operand)

    @property
    def size(self) -> torch.Size:
        return self.operand.size

    @property
    def operand(self) -> DistributionNode:
        c = self.inputs[0]
        assert isinstance(c, DistributionNode)
        return c

    def __str__(self) -> str:
        return "Sample(" + str(self.operand) + ")"

    def support(self) -> Iterable[Any]:
        return self.operand.support()


class ToRealNode(UnaryOperatorNode):
    def __init__(self, operand: BMGNode):
        UnaryOperatorNode.__init__(self, operand)

    @property
    def size(self) -> torch.Size:
        return torch.Size([])

    def __str__(self) -> str:
        return "ToReal(" + str(self.operand) + ")"

    def support(self) -> Iterable[Any]:
        return SetOfTensors(float(o) for o in self.operand.support())


class ToIntNode(UnaryOperatorNode):
    """This represents an integer truncation operation; it is generated
    when a model contains calls to Tensor.int() or int()."""

    def __init__(self, operand: BMGNode):
        UnaryOperatorNode.__init__(self, operand)

    @property
    def size(self) -> torch.Size:
        return torch.Size([])

    def __str__(self) -> str:
        return "ToInt(" + str(self.operand) + ")"

    def support(self) -> Iterable[Any]:
        return SetOfTensors(int(o) for o in self.operand.support())


class ToRealMatrixNode(UnaryOperatorNode):
    def __init__(self, operand: BMGNode):
        UnaryOperatorNode.__init__(self, operand)

    @property
    def size(self) -> torch.Size:
        raise NotImplementedError()

    def __str__(self) -> str:
        return "ToRealMatrix(" + str(self.operand) + ")"

    def support(self) -> Iterable[Any]:
        raise NotImplementedError()


class ToPositiveRealMatrixNode(UnaryOperatorNode):
    def __init__(self, operand: BMGNode):
        UnaryOperatorNode.__init__(self, operand)

    @property
    def size(self) -> torch.Size:
        raise NotImplementedError()

    def __str__(self) -> str:
        return "ToPosRealMatrix(" + str(self.operand) + ")"

    def support(self) -> Iterable[Any]:
        raise NotImplementedError()


class ToPositiveRealNode(UnaryOperatorNode):
    def __init__(self, operand: BMGNode):
        UnaryOperatorNode.__init__(self, operand)

    @property
    def size(self) -> torch.Size:
        return torch.Size([])

    def __str__(self) -> str:
        return "ToPosReal(" + str(self.operand) + ")"

    def support(self) -> Iterable[Any]:
        return SetOfTensors(float(o) for o in self.operand.support())


class ToProbabilityNode(UnaryOperatorNode):
    def __init__(self, operand: BMGNode):
        UnaryOperatorNode.__init__(self, operand)

    @property
    def size(self) -> torch.Size:
        return torch.Size([])

    def __str__(self) -> str:
        return "ToProb(" + str(self.operand) + ")"

    def support(self) -> Iterable[Any]:
        return self.operand.support()


class ToNegativeRealNode(UnaryOperatorNode):
    def __init__(self, operand: BMGNode):
        UnaryOperatorNode.__init__(self, operand)

    def __str__(self) -> str:
        return "ToNegReal(" + str(self.operand) + ")"


class LogSumExpVectorNode(UnaryOperatorNode):
    # BMG supports a log-sum-exp operator that takes a one-column tensor.
    def __init__(self, operand: BMGNode):
        UnaryOperatorNode.__init__(self, operand)

    @property
    def size(self) -> torch.Size:
        return torch.Size([])

    def __str__(self) -> str:
        return "LogSumExpVector"

    def support(self) -> Iterable[Any]:
        raise ValueError("support of LogSumExpVector not yet implemented")


# ####
# #### Marker nodes
# ####


class Observation(BMGNode):
    """This represents an observed value of a sample. For example
    we might have a prior that a mint produces a coin that is
    uniformly unfair. We could then observe a flip of the coin
    and if heads, that is small but not zero evidence that
    the coin is unfair in the heads direction. Given that
    observation, our belief in the true unfairness of the coin
    should no loger be uniform."""

    # TODO: Here we treat an observation as node which takes input
    # from a sample and has an associated value. This implementation
    # choice differs from BMG, which does not treat observations as
    # nodes in the graph; since an observation is never the input
    # of any other node, this makes sense.  We might consider
    # following this pattern and making the observation not inherit
    # from BMGNode.
    #
    # TODO: **Observations are logically distinct from models.**
    # That is, it is common to have one model and many different
    # sets of observations. (And similarly but less common, we
    # could imagine having one set of observations used by many
    # models.)  Moreover it is not yet clear how exactly
    # observation nodes are to be generated by the compiler;
    # from what model source code, if any, do we generate these
    # nodes?  This code is only used right now for testing purposes
    # and we need to do significant design work to figure out
    # how users wish to generate observations of models that have
    # been compiled into BMG.
    value: Any

    def __init__(self, observed: SampleNode, value: Any):
        self.value = value
        BMGNode.__init__(self, [observed])

    @property
    def observed(self) -> SampleNode:
        c = self.inputs[0]
        assert isinstance(c, SampleNode)
        return c

    @property
    def size(self) -> torch.Size:
        if isinstance(self.value, Tensor):
            return self.value.size()
        return torch.Size([])

    def __str__(self) -> str:
        return str(self.observed) + "=" + str(self.value)

    def support(self) -> Iterable[Any]:
        return []


class Query(BMGNode):
    """A query is a marker on a node in the graph that indicates
    to the inference engine that the user is interested in
    getting a distribution of values of that node."""

    # TODO: BMG requires that the target of a query be classified
    # as an operator and that queries be unique; that is, every node
    # is queried *exactly* zero or one times. Rather than making
    # those restrictions here, instead detect bad queries in the
    # problem fixing phase and report accordingly.

    # TODO: As with observations, properly speaking there is no
    # need to represent a query as a *node*, and BMG does not
    # do so. We might wish to follow this pattern as well.

    def __init__(self, operator: BMGNode):
        BMGNode.__init__(self, [operator])

    @property
    def operator(self) -> BMGNode:
        c = self.inputs[0]
        return c

    @property
    def size(self) -> torch.Size:
        return self.operator.size

    def __str__(self) -> str:
        return "Query(" + str(self.operator) + ")"

    def support(self) -> Iterable[Any]:
        return []


# The basic idea of the Metropolis algorithm is: each possible state of
# the graph is assigned a "score" proportional to the probability density
# of that state. We do not know the proportionality constant but we do not
# need to because we take the ratio of the current state's score to a proposed
# new state's score, and accept or reject the proposal based on the ratio.
#
# The idea of a "factor" node is that we also multiply the score by a real number
# which is high for "more likely" states and low for "less likely" states. By
# carefully choosing a factor function we can express our additional knowledge of
# the model.
#
# Factors (like observations and queries) are never used as inputs even though they
# compute a value.


class FactorNode(BMGNode, metaclass=ABCMeta):
    """This is the base class for all factors.
    The inputs are the operands of each factor."""

    def __init__(self, inputs: List[BMGNode]):
        assert isinstance(inputs, list)
        BMGNode.__init__(self, inputs)


# The ExpProduct factor takes one or more inputs, computes their product,
# and then multiplies the score by exp(product), so if the product is large
# then the factor will be very large; if the product is zero then the factor
# will be one, and if the product is negative then the factor will be small.


class ExpProductFactorNode(FactorNode):
    def __init__(self, inputs: List[BMGNode]):
        assert isinstance(inputs, list)
        FactorNode.__init__(self, inputs)

    @property
    def size(self) -> torch.Size:
        return torch.Size([])

    def __str__(self) -> str:
        return "ExpProduct"

    def support(self) -> Iterable[Any]:
        # Factors never produce output so it is not meaningful to compute
        # their support
        return []


def is_zero(n: BMGNode) -> bool:
    return isinstance(n, ConstantNode) and bt.is_zero(n.value)


def is_one(n: BMGNode) -> bool:
    return isinstance(n, ConstantNode) and bt.is_one(n.value)
