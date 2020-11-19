# <a id=title></a>In Need of a More Creative Title

Christian Y. Cahig<br>
*Department of Electrical Engineering \& Technology, MSU-IIT*

---

## <a id=contents></a>Contents

- [Transmission Line Telegraph Equation](#sec--transmission-line-telegraph-equation)
- [Finite-Difference Approximation](#sec--finite-difference-approximations)
  - [Discretization scheme](#subsec--discretization-scheme)
  - [Difference equation](#subsec--difference-equation)
  - [Encoding initial and boundary conditions](#subsec--encoding-initial-and-boundary-conditions)
- [Iterative Solution](#sec--iterative-solution)
  - [Update equation](#subsec--update-equation)
  - [A vectorized approach](#subsec--a-vectorized-approach)
  - [Some considerations](#subsec--some-considerations)

---

## <a id=sec--transmission-line-telegraph-equation></a>Transmission Line Telegraph Equation

Consider a transmission line of length $X$
characterized by per-unit-length
resistance $R$,
shunt conductance $G$,
series inductance $L$,
and
shunt capacitance $C$.
Let $u \left(x,t\right)$ be the instantaneous voltage signal (referred to ground)
at point $x$ along the line
at time $t$,
where
$0 \leq x \leq X$
and
$0 \leq t \leq T$.
We refer to $x=0$ as the *sending end* and $x=X$ as the *receiving end* of the line.

From elementary transmission line analysis,
the propagation of a voltage signal through a transmission line
is described by the *telegraph equation*:

$$
\frac{1}{LC}
\frac{\partial^{2} u \left(x,t\right)}{\partial x^{2}}
=
\frac{\partial^{2} u \left(x,t\right)}{\partial t^{2}}
+
\left(\frac{G}{C} + \frac{R}{L}\right)
\frac{\partial u \left(x,t\right)}{\partial t}
+
\left(\frac{RG}{LC}\right)
u \left(x,t\right)
$$

which is a hyperbolic partial differential equation (PDE).
Letting

$$
c^{2} = \frac{1}{LC},\quad
\alpha = \frac{G}{C},\quad
\beta = \frac{R}{L}
$$

we can write the telegraph equation more succinctly as

$$
c^{2}
\frac{\partial^{2} u \left(x,t\right)}{\partial x^{2}}
=
\frac{\partial^{2} u \left(x,t\right)}{\partial t^{2}}
+
\left(\alpha + \beta\right)
\frac{\partial u \left(x,t\right)}{\partial t}
+
\alpha \beta
u \left(x,t\right).
$$

The quantity $c$ is referred to as the *propagation velocity*.
The first-order term on the right-hand side is called the *dissipation term*,
while the zeroth-order term is called the *dispersion term*.

---

## <a id=sec--finite-difference-approximations></a>Finite-Difference Approximation

### <a id=subsec--discretization-scheme></a>Discretization scheme

We transform the continuous spatial domain
into a set of equally separated discrete points,
*i.e.*,

$$
0 \leq x \leq X
\quad \longrightarrow \quad
x_{k} = k \Delta x,\ 
0 \leq k \leq K \in \mathbb{Z}.
$$

In other words, we approximate the spatial domain
by sampling $K+1$ points spaced $\Delta x$ apart.
Note that
$x_{0}$ corresponds to $x=0$
just as $x_{K}$ to $x=X$.

Similarly, for the temporal domain:

$$
0 \leq t \leq T
\quad \longrightarrow \quad
t_{n} = n \Delta t,\ 
0 \leq n \leq N \in \mathbb{Z}.
$$

where
$t_{0}$ corresponds to $t=0$
as $t_{N}$ to $t=T$.

We can then discretize the continuous quantity
$u \left(x,t\right)$
as
$u \left(x_{k},t_{n}\right)$.
For notational convenience,

$$
u_{k}^{n}
=
u \left(x_{k},t_{n}\right).
$$

### <a id=subsec--difference-equation></a>Difference equation

We can approximate the continuous derivatives as central divided-differences:

$$
\begin{aligned}
  \frac{\partial u \left(x,t\right)}{\partial t}
  &\quad \longrightarrow&
  \frac{\partial u_{k}^{n}}{\partial t}
  &=
  \frac{u_{k}^{n+1} - u_{k}^{n-1}}{2 \Delta t} \\
  \frac{\partial^{2} u \left(x,t\right)}{\partial t^{2}}
  &\quad \longrightarrow&
  \frac{\partial^{2} u_{k}^{n}}{\partial t^{2}}
  &=
  \frac{u_{k}^{n+1} - 2 u_{k}^{n} + u_{k}^{n-1}}{\left(\Delta t\right)^{2}} \\
  \frac{\partial^{2} u \left(x,t\right)}{\partial x^{2}}
  &\quad \longrightarrow&
  \frac{\partial^{2} u_{k}^{n}}{\partial x^{2}}
  &=
  \frac{u_{k+1}^{n} - 2 u_{k}^{n} + u_{k-1}^{n}}{\left(\Delta x\right)^{2}}
\end{aligned}
$$

Substituting these into their continuous counterparts,
we estimate the telegraph equation as a difference equation:

$$
c^{2}
\frac{u_{k+1}^{n} - 2 u_{k}^{n} + u_{k-1}^{n}}{\left(\Delta x\right)^{2}}
=
\frac{u_{k}^{n+1} - 2 u_{k}^{n} + u_{k}^{n-1}}{ \left(\Delta t\right)^{2} }
+
\left(\alpha + \beta\right)
\frac{u_{k}^{n+1} - u_{k}^{n-1}}{2 \Delta t}
+
\alpha \beta
u_{k}^{n}
$$

This numerical approximation of the hyperbolic PDE suggests that
we can estimate the voltage at point $x_{k}$ at the next time instant $n+1$
given the voltages at $x_{k}$ and at the neighboring points at the current time instant
(*i.e.*, $u_{k}^{n}$, $u_{k-1}^{n}$, and $u_{k+1}^{n}$)
and the voltage at $x_{k}$ at the preceding time instant
(*i.e.*, $u_{k}^{n-1}$).

### <a id=subsec--encoding-initial-and-boundary-conditions></a>Encoding initial and boundary conditions

Notice that the difference equation applies for $k=1,2,\ldots,K-1$ and $n=1,2,\ldots,N-1$.
It requires initial
(*i.e.*, at $t_0$)
and boundary
(*i.e.*, at $x_0$ and $x_{K}$)
values to be specified separately.

In general, initial voltage values are expressed as a function of $x$:

$$
u \left(x,0\right) = \mu \left(x\right)
\quad \longrightarrow \quad
u_{k}^{0} = \mu \left(k\right),
\quad \forall k.
$$

It is also common to assume a zero initial time rate of change,
which we can approximate by a forward finite divided difference to :

$$
\frac{\partial u \left(x,0\right)}{\partial t} = 0
\quad \longrightarrow \quad
\frac{\partial u_{k}^{0}}{\partial t}
=
\frac{u_{k}^{1} - u_{k}^{0}}{\Delta t}
=
0
\quad \longrightarrow \quad
u_{k}^{1} = u_{k}^{0},
\quad \forall k.
$$

The sending- and receiving-end voltages can be expressed as functions of $t$:

$$
\begin{aligned}
  u \left(0,t\right) &=\nu_{0} \left(t\right)
  &\longrightarrow \quad
  u_{0}^{n} &= \nu_{0} \left(n\right), \quad \forall n \\
  u \left(X,t\right) &= \nu_{X} \left(t\right)
  &\longrightarrow \quad
  u_{0}^{n} &= \nu_{X} \left(n\right), \quad \forall n
\end{aligned}
$$

One can also have receiving-end information as a space-derivative.
For example, it is commonly assumed that there is no abrupt change from just before $X$ to $X$,
and
then approximate the derivative by a backward finite divided difference:

$$
\frac{\partial u \left(X,t\right)}{\partial x} = 0
\quad \longrightarrow \quad
\frac{\partial u_{K}^{n}}{\partial x}
=
\frac{u_{K}^{n} - u_{K-1}^{n}}{\Delta x}
= 0
\quad \longrightarrow \quad
u_{K}^{n} = u_{K-1}^{n},
\quad \forall n.
$$

---

## <a id=sec--iterative-solution></a>Iterative Solution

### <a id=subsec--update-equation></a>Update equation

From the difference equation approximation of the telegraph equation,
we can obtain $u_{k}^{n+1}$ given $u_{k}^{n}$, $u_{k-1}^{n}$, $u_{k+1}^{n}$, and $u_{k}^{n-1}$.
To express this "update" scheme more explicitly, we can rewrite the difference equation as

$$
A u_{k}^{n+1}
=
E u_{k-1}^{n}
+
F u_{k}^{n}
+
E u_{k+1}^{n}
-
B u_{k}^{n-1}
$$

where

$$
\begin{aligned}
    A &=
    1 + \frac{\Delta t \left(\alpha+\beta\right)}{2} \\
    B &=
    1 - \frac{\Delta t \left(\alpha+\beta\right)}{2} \\
    E &=
    \left(c \frac{\Delta t}{\Delta x}\right)^{2} \\
    F &=
    2 - 2 \left(c \frac{\Delta t}{\Delta x}\right)^{2} - \alpha\beta \left(\Delta t\right)^{2}
\end{aligned}
$$

A basic approach to carrying out the iterative solution
for the entire spatial and temporal domains would then be as follows.

1. Set $u_{k}^{0}$, $\forall k$, according to initial conditions.
   When applicable, set $u_{0}^{0}$ and $u_{K}^{0}$ according to boundary conditions.
2. asd

### <a id=subsec--a-vectorized-approach></a>A vectorized approach

asd

### <a id=subsec--some-considerations></a>Some considerations

- von Neumann analysis
- critical time step
- numerical dispersion
