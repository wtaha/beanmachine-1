// Copyright (c) Facebook, Inc. and its affiliates.
#pragma once

// to keep the linter happy this template specialization has been declared here
// in a header file that is only meant to be included by pybindings.cpp
namespace pybind11 { namespace detail {
  using namespace beanmachine::graph;

  // We want AtomicValues output from C++ to show up as native Python types
  // such as floats, ints, bool etc. Hence we have the specific `cast` function
  // in pybindings.cpp. However from Python to C++ we want to use the simple mappings that we
  // will define below with `py::class_<AtomicValue>` hence we create a super class
  // and delegate the Python to C++ load to the base class as explained in this link:
  // https://github.com/pybind/pybind11/issues/1176#issuecomment-343312352
  template <> struct type_caster<AtomicValue> : public type_caster_base<AtomicValue> {
    using base = type_caster_base<AtomicValue>;
   public:
    bool load(handle src, bool convert) {
      // use base class for Python -> C++
      return base::load(src, convert);
    }

    static handle cast(AtomicValue src, return_value_policy policy, handle parent) {
      // for C++ -> Python condition the return object on the type
      switch (src.type) {
          case AtomicType::BOOLEAN: {
            return type_caster<bool>::cast(src._bool, policy, parent);
          }
          case AtomicType::PROBABILITY:
          case AtomicType::REAL:
          case AtomicType::POS_REAL: {
            return type_caster<double>::cast(src._double, policy, parent);
          }
          case AtomicType::NATURAL: {
            return type_caster<int>::cast(src._natural, policy, parent);
          }
          case AtomicType::TENSOR: {
            return type_caster<torch::Tensor>::cast(src._tensor, policy, parent);
          }
          default: {
            throw std::runtime_error("unexpected type for AtomicValue");
          }
      }
    }
  };
}} // namespace pybind11::detail