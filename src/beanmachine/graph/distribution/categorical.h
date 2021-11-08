// Copyright (c) Facebook, Inc. and its affiliates.
#pragma once
#include "beanmachine/graph/distribution/distribution.h"

namespace beanmachine {
namespace distribution {

class Categorical : public Distribution {
 public:
  Categorical(
      graph::AtomicType sample_type,
      const std::vector<graph::Node*>& in_nodes);
  ~Categorical() override {}
  graph::natural_t _natural_sampler(std::mt19937& gen) const override;
  double log_prob(const graph::NodeValue& value) const override;
  void log_prob_iid(const graph::NodeValue& value, Eigen::MatrixXd& log_probs)
      const override;
  void gradient_log_prob_value(
      const graph::NodeValue& value,
      double& grad1,
      double& grad2) const override;
  void gradient_log_prob_param(
      const graph::NodeValue& value,
      double& grad1,
      double& grad2) const override;

  void backward_value(
      const graph::NodeValue& /* value */,
      graph::DoubleMatrix& /* back_grad */,
      double /* adjunct */ = 1.0) const override {}
  void backward_value_iid(
      const graph::NodeValue& /* value */,
      graph::DoubleMatrix& /* back_grad */) const override {}
  void backward_value_iid(
      const graph::NodeValue& /* value */,
      graph::DoubleMatrix& /* back_grad */,
      Eigen::MatrixXd& /* adjunct */) const override {}

  void backward_param(const graph::NodeValue& value, double adjunct = 1.0)
      const override;
  void backward_param_iid(const graph::NodeValue& value) const override;
  void backward_param_iid(
      const graph::NodeValue& value,
      Eigen::MatrixXd& adjunct) const override;

  static double _grad1_log_prob_param(bool x, double p);
};

} // namespace distribution
} // namespace beanmachine