# In Need of a More Creative Title

Christian Y. Cahig<br>
*Department of Electrical Engineering \& Technology, MSU-IIT*

---

## Contents

- [Transmission Line Telegraph Equation](#sec--transmission-line-telegraph-equation)
- [Finite-Difference Approximation](#sec--finite-difference-approximations)
  - [Discretization scheme](#subsec--discretization-scheme)
  - [Difference equation](#subsec--difference-equation)
  - [Initial and boundary conditions](#subsec--initial-and-boundary-conditions)
- [Implementation](#sec--implementation)

---

## <a id=sec--transmission-line-telegraph-equation></a>Transmission Line Telegraph Equation

Consider a transmission line of length $L$
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
$0 \leq x \leq L$
and
$0 \leq t \leq T$.

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
u \left(x,t\right)
$$

The quantity $c$ is referred to as the *propagation velocity*.

---

## <a id=sec--finite-difference-approximations></a>Finite-Difference Approximation

### <a id=subsec--discretization-scheme></a>Discretization scheme

We transform the continuous spatial domain
into a set of equally separated discrete points,
*i.e.*,

$$
0 \leq x \leq L
\quad \longrightarrow \quad
x_{k} = k \Delta x,\ 
0 \leq k \leq K \in \mathbb{Z}
$$

In other words, we approximate the spatial domain
by sampling $K+1$ points spaced $\Delta x$ apart.
Note that
$x_{0}$ corresponds to $x=0$
just as $x_{K}$ to $x=L$.

Similarly, for the temporal domain:

$$
0 \leq t \leq T
\quad \longrightarrow \quad
t_{n} = n \Delta t,\ 
0 \leq n \leq N \in \mathbb{Z}
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
u \left(x_{k},t_{n}\right)
$$

### <a id=subsec--difference-equation></a>Difference equation

We can approximate the continuous derivatives as central divided-differences:

$$
\frac{\partial u \left(x,t\right)}{\partial t}
\quad \longrightarrow \quad
\frac{\partial u_{k}^{n}}{\partial t}
=
\frac{u_{k}^{n+1} - u_{k}^{n-1}}{2 \Delta t}
$$

$$
\frac{\partial^{2} u \left(x,t\right)}{\partial t^{2}}
\quad \longrightarrow \quad
\frac{\partial^{2} u_{k}^{n}}{\partial t^{2}}
=
\frac{u_{k}^{n+1} - 2 u_{k}^{n} + u_{k}^{n-1}}{\left(\Delta t\right)^{2}}
$$

$$
\frac{\partial^{2} u \left(x,t\right)}{\partial x^{2}}
\quad \longrightarrow \quad
\frac{\partial^{2} u_{k}^{n}}{\partial x^{2}}
=
\frac{u_{k+1}^{n} - 2 u_{k}^{n} + u_{k-1}^{n}}{\left(\Delta x\right)^{2}}
$$

Substituting these into their continuous counterparts,
we estimate the telegraph equation as a difference equation:

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
u \left(x,t\right)
$$

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

### <a id=subsec--initial-and-boundary-conditions></a>Initial and boundary conditions

Notice that the difference equation requires initial
(*i.e.*, at $t_0$)
and boundary
(*i.e.*, at $x_0$ and $x_{K}$)
values to be specified separately.



---

## <a id=sec--implementation></a>Implementation

he
