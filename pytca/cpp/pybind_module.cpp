#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include "vwap.cpp"

namespace py = pybind11;

PYBIND11_MODULE(pytca_cpp, m) {
    m.def("calculate_vwap", &calculate_vwap, "A function that calculates VWAP");
}
