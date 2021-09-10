// Copyright (c) Facebook, Inc. and its affiliates.
#pragma once
#include "beanmachine/graph/graph.h"
#include "beanmachine/graph/proposer/proposer.h"
#include "beanmachine/graph/stepper/single_site_stepper.h"

namespace beanmachine {
namespace graph {

class NMCDirichletGammaSingleSiteStepper : public SingleSiteStepper {
 public:
  NMCDirichletGammaSingleSiteStepper(Graph* graph, MH* mh)
      : SingleSiteStepper(graph, mh) {}
  virtual bool is_applicable_to(graph::Node* tgt_node) override;

  virtual void step(graph::Node* tgt_node) override;

 private:
  double compute_sto_affected_nodes_log_prob(
      Node* tgt_node,
      double param_a,
      NodeValue value);
  std::unique_ptr<proposer::Proposer> create_proposal_dirichlet_gamma(
      Node* tgt_node,
      double param_a,
      double sum,
      NodeValue value,
      uint k);
};

} // namespace graph
} // namespace beanmachine
