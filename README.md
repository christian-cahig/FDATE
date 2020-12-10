# A Finite Difference Approach to Solving Transmission Line Telegraph Equations

---

## Overview

This is part of the curricular requirements of the graduate course
ES 205 Numerical Methods for Engineers
offered by Mindanao State University - Iligan Institute of Technology
and handled by Engr. Michael S. Villame.
Specifically, this work focuses on the following subtopics:

- finite difference approximation of the transmission line telegraph equation, which is a hyperbolic partial differential equation;
- encoding initial and boundary conditions in terms of finite differences;
- advantages of vectorizing the iterative update scheme;
- effects of domain discretization in terms of the Courant–Friedrichs–Lewy (CFL) condition; and
- applying the numerical scheme in simulating a fault event.

---

## Directory

### Documentation

The primary documentation for this project is the paper entitled
*A Finite Difference Approach to Solving the Transmission Line Telegraph Equation*.
Everything related to the paper is in [`report/`](./report/).
Some of the key files:

- [`paper.tex`](./report/paper.tex)
  contains the LaTeX code for the paper in the
  [ICLR 2021 conference article format](https://github.com/ICLR/Master-Template).
- [`paper.pdf`](./report/paper.pdf)
  is the compiled PDF file of the paper.
- [`references.bib`](./report/references.bib)
  contains the bibliographic information.

### Experiments

Experiment files and codes are in [`illustrative examples/`](./illustrative%20examples/),
which contains the following subdirectories:

- [`utility/`](./illustrative%20examples/utility/)
- [`on vectorization/`](./illustrative%20examples/on%20vectorization)
- [`on spatial domain discretization/`](./illustrative%20examples/on%20spatial%20domain%20discretization/)
- [`on temporal domain discretization`](./illustrative%20examples/on%20temporal%20domain%20discretization/)
- [`simulating a faulted bus`](./illustrative%20examples/simulating%20a%20faulted%20bus/)

Except for `utility/`,
subdirectories correspond to eponymous subsections in Section 3 of the paper.
`utility/` contains a Python module of utility class and functions for the experiments used.

### Others

[`misc/`](./misc/) contains some supporting files
that are not directly used in the paper or in the experiments.

Much of the work is performed in a conda environment with the following key packages:

- Python 3.8.0
- NumPy 1.19.1
- SciPy 1.5.2
- Matplotlib 3.3.2

To replicate the environment, use [`fdate.yml`](./misc/fdate.yml);
*e.g.*, via

```.cmd
(base) PS C:\WINDOWS\system32> conda env create --file fdate.yml
```

---
