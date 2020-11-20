# <a id=title></a>In Need of a More Creative Title

Christian Y. Cahig<br>
*Department of Electrical Engineering \& Technology, MSU-IIT*

---

## <a id=contents></a>Contents

- [Transmission Line Telegraph Equation](#sec--transmission-line-telegraph-equation)
- [Finite-Difference Approximation](#sec--finite-difference-approximations)
  - [Discretization scheme](#subsec--discretization-scheme)
  - [Difference equation](#subsec--difference-equation)
  - [Update scheme](#subsec--update-scheme)
- [Some remarks](#sec--some-remarks)
  - [Encoding initial and boundary conditions](#subsec--encoding-initial-and-boundary-conditions)
  - [A vectorized update scheme](#subsec--a-vectorized-update-scheme)
  - [On $\Delta t$ and $\Delta x$](#subsec--on-delta-t-and-delta-x)

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

The first-order term on the right-hand side is called the *dissipation term*,
while the zeroth-order term is called the *dispersion term*.
In the absence of losses, *i.e.*, $R=G=0$,
the telegraph equation reduces into one describing a wave with a propagation velocity of $c$
and an angular frequency $\omega$ given as

$$
\omega = \frac{1}{X \sqrt{LC}}
$$

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

### <a id=subsec--update-scheme></a>Update scheme

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

---

## <a id=sec--some-remarks></a>Some Remarks

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

It is also common to have predetermined initial time rate of change of voltage,
which can then be approximated by a forward finite divided difference:

$$
\frac{\partial u \left(x,0\right)}{\partial t} = \gamma^{0}
\quad \longrightarrow \quad
\frac{\partial u_{k}^{0}}{\partial t}
=
\frac{u_{k}^{1} - u_{k}^{0}}{\Delta t}
=
\gamma^{0}
\quad \longrightarrow \quad
u_{k}^{1} = u_{k}^{0} + \gamma^{0} \Delta t,
\quad \forall k.
$$

The sending- and receiving-end voltages can be expressed as functions of $t$:

$$
\begin{aligned}
  u \left(0,t\right) &=\nu_{0} \left(t\right)
  &\longrightarrow \quad
  u_{0}^{n} &= \nu_{0} \left(n\right), \quad &\forall n \\
  u \left(X,t\right) &= \nu_{X} \left(t\right)
  &\longrightarrow \quad
  u_{0}^{n} &= \nu_{X} \left(n\right), \quad &\forall n
\end{aligned}
$$

Information at the boundaries may also be expressed in terms of space-derivatives,
which can be approximated using forward and backward finite divided differences:

$$
\begin{aligned}
  \frac{\partial u \left(0,t\right)}{\partial x} = \gamma_{0}
  &\quad \longrightarrow \quad&
  \frac{\partial u_{0}^{n}}{\partial x}
  &=
  \frac{u_{1}^{n} - u_{0}^{n}}{\Delta x}
  = \gamma_{0}
  &\quad \longrightarrow \quad
  u_{0}^{n} &= u_{1}^{n} - \gamma_{0} \Delta x,
  \quad \forall n \\
  \frac{\partial u \left(X,t\right)}{\partial x} = \gamma_{X}
  &\quad \longrightarrow \quad&
  \frac{\partial u_{K}^{n}}{\partial x}
  &=
  \frac{u_{K}^{n} - u_{K-1}^{n}}{\Delta x}
  = \gamma_{X}
  &\quad \longrightarrow \quad
  u_{K}^{n} &= u_{K-1}^{n} + \gamma_{X} \Delta x,
  \quad \forall n
\end{aligned}
$$

### <a id=subsec--a-vectorized-update-scheme></a>A vectorized update scheme

The update scheme is essentially a system of $K-1$ linear equations:

$$
A
\begin{bmatrix}
  u_{1}^{n+1} \\
  u_{2}^{n+1} \\
  \vdots \\
  u_{K-1}^{n+1}
\end{bmatrix}
=
\begin{bmatrix}
  E & F & E & 0 & \cdots & 0 & 0 & 0 \\
  0 & E & F & E & \cdots & 0 & 0 & 0 \\
  \vdots & \vdots & \vdots & \vdots & \ddots & \vdots & \vdots & \vdots \\
  0 & 0 & 0 & 0 & \cdots & E & F & E
\end{bmatrix}
\begin{bmatrix}
  u_{0}^{n} \\
  u_{1}^{n} \\
  \vdots \\
  u_{K-1}^{n} \\
  u_{K}^{n}
\end{bmatrix}
-
B
\begin{bmatrix}
  0 & 1 & 0 & \cdots & 0 & 0 \\
  0 & 0 & 1 & \cdots & 0 & 0 \\
  \vdots & \vdots & \vdots & \ddots & \vdots & \vdots \\
  0 & 0 & 0 & \cdots & 1 & 0
\end{bmatrix}
\begin{bmatrix}
  u_{0}^{n-1} \\
  u_{1}^{n-1} \\
  \vdots \\
  u_{K-1}^{n-1} \\
  u_{K}^{n-1}
\end{bmatrix}
$$

Letting

$$
\begin{aligned}
  \tilde{\mathbf{u}}^{n} &=
  \begin{bmatrix}
    u_{1}^{n}, u_{2}^{n}, \ldots, u_{K-1}^{n}
  \end{bmatrix}^{\intercal} \in \mathbb{R}^{K-1} \\
  \mathbf{u}^{n} &=
  \begin{bmatrix}
    u_{0}^{n}, u_{1}^{n}, \ldots, u_{K-1}^{n}, u_{K}^{n}
  \end{bmatrix}^{\intercal} \in \mathbb{R}^{K+1} \\
  \mathbf{E} &=
  \begin{bmatrix}
    E & F & E & 0 & \cdots & 0 & 0 & 0 \\
    0 & E & F & E & \cdots & 0 & 0 & 0 \\
    \vdots & \vdots & \vdots & \vdots & \ddots & \vdots & \vdots & \vdots \\
    0 & 0 & 0 & 0 & \cdots & E & F & E
  \end{bmatrix} \in \mathbb{R}^{\left(K-1\right) \times K} \\
  \mathbf{B} &=
  B
  \begin{bmatrix}
    \mathbf{0} & \mathbf{I} & \mathbf{0}
  \end{bmatrix}  \in \mathbb{R}^{\left(K-1\right) \times K}
\end{aligned}
$$

where $\mathbf{0}$ is an $\left(K-1\right)$-vector of zeros
and $\mathbf{I}$ is the identity matrix of size $\left(K-1\right) \times \left(K-1\right)$,
the update equation can be expressed compactly as

$$
\begin{aligned}
  A \tilde{\mathbf{u}}^{n+1} &= \mathbf{E} \mathbf{u}^{n} - \mathbf{B} \mathbf{u}^{n-1} \\
  \mathbf{u}^{n+1} &=
  \begin{bmatrix}
    u_{0}^{n+1} \\
    \tilde{\mathbf{u}}^{n+1} \\
    u_{K}^{n+1}
  \end{bmatrix}
\end{aligned}
$$

where $u_{0}^{n+1}$ and $u_{K}^{n+1}$ are determined from the boundary conditions.

### <a id=subsec--on-delta-t-and-delta-x></a>On $\Delta t$ and $\Delta x$

- choosing $\Delta x$
- critical $\Delta t$
- numerical dispersion?
