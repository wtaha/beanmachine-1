#include "beanmachine/graph/global/global_mh.h"
#include <random>

namespace beanmachine {
namespace graph {
GlobalMH::GlobalMH(Graph& g, uint seed)
    : graph(g), state(GlobalState(g, seed)) {}

std::vector<std::vector<NodeValue>>& GlobalMH::infer(
    int num_samples,
    uint seed,
    int num_warmup_samples,
    bool save_warmup) {
  std::mt19937 gen(seed);
  // TODO: tie samples directly to inference
  graph.agg_type = AggregationType::NONE;
  graph.samples.clear();
  std::vector<std::vector<NodeValue>> values;

  prepare_graph();
  proposer->initialize(state, gen, num_warmup_samples);

  for (int i = 0; i < num_samples + num_warmup_samples; i++) {
    double acceptance_log_prob = proposer->propose(state, gen);

    bool accept_sample;
    if (acceptance_log_prob > 0) {
      accept_sample = true;
    } else {
      std::uniform_real_distribution<> uniform(0.0, 1.0);
      double alpha = std::log(uniform(gen));
      accept_sample = (acceptance_log_prob > alpha);
    }

    if (accept_sample) {
      // backup new samples + grads for future proposals to revert to
      // Note: we are backing up only when the samples have changed
      // for the sake of performance
      state.backup_unconstrained_values();
      state.backup_unconstrained_grads();
    } else {
      // revert to previously backed up samples + grads
      state.revert_unconstrained_values();
      state.revert_unconstrained_grads();
      state.update_log_prob();
    }

    if (i < num_warmup_samples) {
      double acceptance_prob = std::min(std::exp(acceptance_log_prob), 1.0);
      proposer->warmup(acceptance_prob, i + 1, num_warmup_samples);
      if (save_warmup) {
        graph.collect_sample();
      }
    } else {
      graph.collect_sample();
    }
  }

  return graph.samples;
}

} // namespace graph
} // namespace beanmachine