---
id: why_bean_machine
title: 'Why Bean Machine?'
sidebar_label: 'Why Bean Machine?'
slug: '/why_bean_machine'
---
<!-- @import "../../header.md" -->

Bean Machine is a probabilistic programming language that makes developing and deploying generative probabilistic models intuitive and efficient. This page describes the motivation for using [Probabilistic Programming](#probabilistic-programming) in general, and [Bean Machine advantages](#bean-machine-advantages) specifically.

## Probabilistic Programming

### Generative models

Bean Machine's generative modeling is concerned not only with providing useful predictions (as traditional ML techniques do), but also with estimating the uncertainty inherent in the problem at hand in the form of probability distributions. Estimating uncertainty helps ensure that predictions are reliable and robust.

Generative modeling with Bean Machine offers many benefits:

  1. **Uncertainty estimation.**  Predictions are quantified with reliable measures of uncertainty in the form of probability distributions. An analyst can understand not only the system's prediction, but also the relative likelihood of other possibilities.
  2. **Expressivity.**  It's extremely easy to encode a rich model directly in source code. This allows one to match the structure of the model to the structure of the problem.
  3. **Interpretability.**  Because the model matches the domain, one can query intermediate variables within the model as conceptually meaningful properties. This can be used to interpret *why* a particular prediction was made, and can aid the model development process.

### Generative Probabilistic Models

A generative probabilistic model consists of **random variables** and **conditional probability distributions** (CPDs) that encode knowledge about some domain. For example, consider a simplified model for the spread of infectious diseases, where we wish to express the idea that the average number of new cases on a given day is proportional to the current number of infections, with the proportionality constant being the daily reproduction rate of the disease. In order to express this mathematically, it is common practice to rely on _elementary probability distributions_ (EPDs) with well known statistics, such as the _Poisson_ distribution here:

```
num_new_cases ~ Poisson(reproduction_rate * num_infected)
```

![](/img/poisson_3.png)

<!-- It might be more interesting to show the Poisson distribution for reproduction_rate=0.1 and num_inference=1000000 -->

Let's fix for now the value of `num_infected`, then the above statement gives the CPD of the random variable `num_new_cases`, conditioned on the value of its **parent** random variable `reproduction_rate`. Since the parameter of the Poisson distribution is also its mean, this CPD is consistent with the knowledge that we were trying to express.

A well-formed generative model must specify the EPD or CPD of each random variable, and the **directed graph** induced by all the parent-child relationships among random variables must be **acyclic**. To complete our model, we must therefore also specify a distribution for the random variable `reproduction_rate`. In the case of new diseases, where we don't know anything yet about the actual reproduction rate, this poses a seemingly intractable problem. In the **Bayesian approach** to this problem, we specify the probability distributions of random variables without parents as our **_a priori_** beliefs (i.e., before seeing any data) about them. So, in this example, if infectious disease experts believe that a new disease would have a daily reproduction rate which is strictly positive and could be expected to be drawn from a distribution with a mean of 0.1, then we could express this belief with the help of another EPD, the *Exponential* distribution, as follows:

```
reproduction_rate ~ Exponential(1 / 0.1)
```

![](/img/exponential_10.png)

### Inference

Given a generative model, the natural next step is to use it to perform inference. Inference is the process of combining a **model** with **data** to obtain **insights**, in the form of **_a posteriori_** beliefs over values of interest. Our documentation refers to the data as _"observations"_, to the values of interest as _"queried random variables"_, and to the insights as _"posterior distributions"_.

In our example above, let's say we observe that `num_infected = 1087980` and that `num_new_cases = 238154`. Now, given this observation, we might want to query the posterior distribution for `reproduction_rate`. Mathematically speaking, we seek the following CPD:

$$\mathbb{P}(\texttt{reproduction\_rate} \,\mid\, \texttt{num\_infected}=1087980,\; \texttt{num\_new\_cases} = 238154)$$

One way to understand the semantics of the inference task is to think of a generative probabilistic model as specifying a distribution over possible **worlds**. A world can be thought of as an assignment of specific admissible values to all random variables in the model. So, for example, some possible worlds in our case are:

- `reproduction_rate = 0.01, num_new_cases = 9000`,
- `reproduction_rate = 0.1, num_new_cases = 90000`, or
- `reproduction_rate = 0.9, num_new_cases = 800000`.

Our generative model specifies a _joint_ probability distribution over each of these worlds, based on the _prior_ distribution we've chosen for `reproduction_rate` and the _likelihood_ of `num_new_cases` given some `reproduction_rate`. Now, the inference task is to restrict attention to only those worlds in which `num_new_cases = 238154`. We're interested in learning the resulting _posterior_ distribution over `reproduction_rate` assignments within these worlds that are compatible with our observation.

### Where Does Bean Machine Fit In?

In the rest of this Overview we'll introduce you to Bean Machine's syntax, and show you how it can be used to learn about problems like this one. Traditionally, lots of painstaking, hand-crafted work has gone into modeling generative scenarios. Bean Machine aims to handle all of the manual work involved in fitting data to your model, leaving you to focus on the exciting part: the problem itself! Keep on reading to find out how.

### Target Audience

While we hope that the guides you'll find here are relevant to anyone with an ML background, there are excellent resources available if this is your first exposure to Bayesian analysis! We highly recommend the excellent YouTube series _[Statistical Rethinking](https://www.youtube.com/playlist?list=PLDcUM9US4XdNM4Edgs7weiyIguLSToZRI)_, which walks through Bayesian thinking and probabilistic modeling. For a more hands-on experience, you can check out the free, online tutorial _[Bayesian Methods for Hackers](https://camdavidsonpilon.github.io/Probabilistic-Programming-and-Bayesian-Methods-for-Hackers/#contents)_.

If you have previous knowledge of probabilistic programming, you may want to read below to learn more about specific details of the Bean Machine system. Otherwise, you can go directly to [Quick Start](../quickstart) for details on how Bean Machine is used!

## Bean Machine Advantages

Bean Machine builds on top of PyTorch with a declarative modeling syntax, being therefore simultaneously performant and intuitive for building probabilistic models. It provides further value by implementing cutting-edge inference algorithms and allowing the user to select and program custom inferences for different problems and subproblems.

### Site-based inference

<!-- ### Single-site inference -->

Bean Machine uses a site-based inference engine. "Sites" are random variable families, and Bean Machine uses these families to enable a modular inference engine.

The simplest form of site-based inference is called "single-site" inference. In the single-site paradigm, models are built up from random variables that can be reasoned about individually. Bean Machine can exploit this modularity to update random variables one-at-a-time, reducing unnecessary computation and enabling posterior updates that might not be possible if processing the entire model in one go.

Bean Machine also supports "multi-site" inference, in which sites are families of multiple random variables are reasoned about jointly. This increases complexity during inference, but it allows the engine to exploit inter-site correlations when fitting the posterior distribution.

Altogether, site-based inference is a flexible pattern for trading off complexity and modularity, and enables the advanced techniques outlined below.

### Declarative modeling

<!-- Usability improvements -->
In Bean Machine, random variables are implemented as decorated Python functions, which naturally form an interface for the model. Using functions makes it simple to determine a random variable's definition, since it is contained in a function that is usually only a few lines long. This lets you directly refer to random variables to access inferred distributions or when binding data to your model. This is safer and more natural than relying on string identifiers, and also enables IDE support and type-checking in many cases.

<!-- Efficiency improvements -->
Declarative modeling also frees the inference engine to reorder model execution. Foremost, it enables computation of immediate dependencies for random variables. This makes it possible to propose new values for a random variable by examining only its dependencies, saving significant amounts of compute in models with complex structure.

### Programmable inference

<!-- Compositional inference -->
Bean Machine allows the user to design and apply powerful inference methods. Because Bean Machine can propose updates for random variables individually, the user is free to customize the _method_ which it uses to propose those values. Different inference methods can be supplied for different families of random variables. For example, a particular model can leverage gradient information when proposing values for differentiable random variables, and at the same time might sample from discrete ones with a particle filter. This single-site "compositional inference" pattern enables seamless interoperation among any MCMC-based inference strategies.

<!-- Block inference -->
Though powerful, compositional inference limits Bean Machine's global understanding of the model. To combat this, Bean Machine exposes a separate functionality to allow joint processing of multiple sites. This "multi-site inference" causes Bean Machine to process both sites together before updating either, which is especially useful for updating highly-correlated random variables. Certain inference methods may be able to further exploit multi-sites with inference-specific optimizations.  Since multi-site inference is orthogonal to compositional inference, it allows you to create sophisticated, model-specific inference strategies with virtually no additional effort.

### Advanced methods

Bean Machine supports a variety of classic inference methods such as ancestral sampling and the No-U-Turn sampler (NUTS). However, the framework also leverages single-site understanding of the model in order to provide efficient methods that take advantage of higher-order gradients and model structure.

<!-- NMC -->
Bean Machine includes the first implementation of Newtonian Monte Carlo (NMC) in a more general platform. NMC utilizes second-order gradient information to construct a multivariate Gaussian proposer that takes local curvature into account. As such, it can produce sample very efficiently with no warmup period when the posterior is roughly Gaussian. Bean Machine's structural understanding of the model lets us keep computation relatively cheap by only modeling a subset of the space that is relevant to updating a particular random variable.

<!-- Custom proposers -->
For certain domains, prepackaged inference methods may not be the best tool for the job. For example, if dealing with a problem specified in spherical coordinates, it may be useful to incorporate a notion of spherical locality into the inference proposal. Or, you may want to incorporate some notion of ordering when dealing with certain discrete random variables. Bean Machine exposes a flexible abstraction called _custom proposers_ for just this problem. Custom proposers let the user design powerful new inference methods from the building blocks of existing ones, while easily plugging into Bean Machine's multi-site paradigm.

### Bean Machine Graph compilation

<!-- PyTorch performance -->
PyTorch offers strong performance for models comprised of a small number of large tensors. However, many probabilistic models have a rich or sparse structure that is difficult to write in terms of just a handful of large tensor operations. And in many cases, these are exactly the problems for which probabilistic modeling is most compelling!

To address this, we are developing an experimental inference runtime called Bean Machine Graph (BMG) Inference. BMG Inference is a specialized combination of compiler and a fast, independent runtime that is optimized to run inference even for un-tensorized models. By design, BMG Inference has the same interface as other Bean Machine inference methods, relying on a custom behind-the-scenes compiler to interpret your model and translate it to a faster implementation with no Python dependencies.

BMG Inference routinely achieves 1 to 2 orders-of-magnitude speedup for untensorized models. However, please note that this infrastructure is under development, and the supported feature set may be limited.

<!-- ## Sneak Peek at Bean Machine Syntax

At this point it would be helpful to briefly look at our example model written in Bean Machine.
Random variables such as reproduction_rate and num_new_cases are represented as functions which compute the CPD of these variables and return a distribution object.
These CPD functions are marked with the `beanmachine.ppl.random_variable` decorator and all EPDs are based on PyTorch EPDs in the `torch.distribution` package.

```
import beanmachine.ppl as bm
import torch.distribution as dist

num_infected = 1087980

@bm.random_variable
def reproduction_rate():
    return Exponential(0.1)

@bm.random_variable
def num_new_cases():
    return Poisson(reproduction_rate() *  num_infected)
```

The call to inference involves first creating an appropriate inference engine object and then invoking the `infer` method as follows

```
engine = bm.<Inference Engine>()
engine.infer(queries = [reproduction_rate()],
             observations = {new_new_cases() : 238154})
```

Here it is important to note that the call `reproduction_rate()` in the list of queried variables refers to the name of a random variable while the same call in the CPD of `num_new_cases()` refers to the value of the random variable.
 -->
