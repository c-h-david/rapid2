# Sandbox

RAPID2 comes along with a set of test files based on a symbolic domain.

The symbolic domain is a the same that was used for illustration of the
matrix-based Muskingum method equations that were originally developed in
[David et al. (2011)][URL_DA2011].

This river network is composed of five reaches connected by two confluences.
The network matrix for this domain is:

```math
\mathbf{N} =
\begin{bmatrix}
 0      & 0      & 0      & 0      & 0      \\
 0      & 0      & 0      & 0      & 0      \\
 1      & 1      & 0      & 0      & 0      \\
 0      & 0      & 0      & 0      & 0      \\
 0      & 0      & 1      & 1      & 0      \\
\end{bmatrix}
```

Two gaging stations are contained within the network.
The selection matrix for this domain is:

```math
\mathbf{S} =
\begin{bmatrix}
 0      & 0      & 1      & 0      & 0      \\
 0      & 0      & 0      & 0      & 1      \\
\end{bmatrix}
```

The Muskingum time parameter (s) vector is:

```math
\mathbf{k} =
\begin{bmatrix}
 9000   \\
 9000   \\
 9000   \\
 9000   \\
 9000   \\
\end{bmatrix}
```

The Muskingum non-dimensional parameter vector is:

```math
\mathbf{x} =
\begin{bmatrix}
 0.250  \\
 0.250  \\
 0.250  \\
 0.250  \\
 0.250  \\
\end{bmatrix}
```

The routing time step (s) used for simulations is:

```math
\Delta t = 900
```

With these, the Muskingum parameter matrices become
[(David et al. 2011)][URL_DA2011]:

```math
\mathbf{C_1} =
\begin{bmatrix}
-0.250  &  0.    &  0.    &  0.    &  0.    \\
 0.     & -0.250 &  0.    &  0.    &  0.    \\
 0.     &  0.    & -0.250 &  0.    &  0.    \\
 0.     &  0.    &  0.    & -0.250 &  0.    \\
 0.     &  0.    &  0.    &  0.    & -0.250 \\
\end{bmatrix}
```

```math
\mathbf{C_2} =
\begin{bmatrix}
 0.375 &  0.    &  0.    &  0.    &  0.    \\
 0.    &  0.375 &  0.    &  0.    &  0.    \\
 0.    &  0.    &  0.375 &  0.    &  0.    \\
 0.    &  0.    &  0.    &  0.375 &  0.    \\
 0.    &  0.    &  0.    &  0.    &  0.375 \\
\end{bmatrix}
```

```math
\mathbf{C_3} =
\begin{bmatrix}
 0.875 &  0.    &  0.    &  0.    &  0.    \\
 0.    &  0.875 &  0.    &  0.    &  0.    \\
 0.    &  0.    &  0.875 &  0.    &  0.    \\
 0.    &  0.    &  0.    &  0.875 &  0.    \\
 0.    &  0.    &  0.    &  0.    &  0.875 \\
\end{bmatrix}
```

These three parameter matrices satisfy the following equality:

```math
\mathbf{C_1} + \mathbf{C_2} + \mathbf{C_3} =
\begin{bmatrix}
 1.000 &  0.    &  0.    &  0.    &  0.    \\
 0.    &  1.000 &  0.    &  0.    &  0.    \\
 0.    &  0.    &  1.000 &  0.    &  0.    \\
 0.    &  0.    &  0.    &  1.000 &  0.    \\
 0.    &  0.    &  0.    &  0.    &  1.000 \\
\end{bmatrix}
```

The matrices related to Muskingum routing are as follows:
[(David et al. 2011)][URL_DA2011]:

```math
\mathbf{I} - \mathbf{C_1} \cdot \mathbf{N} =
\begin{bmatrix}
 1.     &  0.    &  0.    &  0.    &  0.    \\
 0.250  &  0.250 &  0.    &  0.    &  0.    \\
 0.     &  0.    &  1.    &  0.    &  0.    \\
 0.     &  0.    &  0.    &  1 .   &  0.    \\
 0.     &  0.    &  0.250 &  0.250 &  1.    \\
\end{bmatrix}
```

```math
(\mathbf{I} - \mathbf{C_1} \cdot \mathbf{N})^{-1} =
\begin{bmatrix}
 1.     &  0.    &  0.    &  0.    &  0.    \\
 0.250  &  0.250 &  0.    &  0.    &  0.    \\
 0.     &  0.    &  1.    &  0.    &  0.    \\
 0.     &  0.    &  0.    &  1 .   &  0.    \\
 0.0625 &  0.0625&  0.250 &  0.250 &  1.    \\
\end{bmatrix}
```

The duration of the simulation is 10 days.
We assume that the true flow of water coming from the exterior of the network
and feeding into each reach of the network is a square wave function, i.e. a
periodic waveform that alternates between two fixed levels, switching
instantaneously between them. We use $\lfloor y \rfloor$ to describe the floor
of a number $y$. Additionally, $y \bmod z$ is used for the remainder of $y$
divided by $z$.

```math
\mathbf{Q^{eT}}(t) =
\begin{bmatrix}
 1      \\
 1      \\
 1      \\
 2      \\
 2      \\
\end{bmatrix}
+
\begin{bmatrix}
 1      \\
 1      \\
 1      \\
 2      \\
 2      \\
\end{bmatrix}
\cdot
\left( \left\lfloor \frac{t}{86400} \right\rfloor \right) \bmod 2
```

This inflow is used to generate the observations:

```math
\mathbf{g^{T}}(t)
```

The matrices related to lumped routing are as follows
[(David et al. 2019)][URL_DA2019]:

```math
\mathbf{I} - \mathbf{N} =
\begin{bmatrix}
 1      & 0      & 0      & 0      & 0      \\
 0      & 1      & 0      & 0      & 0      \\
-1      &-1      & 1      & 0      & 0      \\
 0      & 0      & 0      & 1      & 0      \\
 0      & 0      &-1      &-1      & 1      \\
\end{bmatrix}
```

```math
(\mathbf{I} - \mathbf{N})^{-1} =
\begin{bmatrix}
 1      & 0      & 0      & 0      & 0      \\
 0      & 1      & 0      & 0      & 0      \\
 1      & 1      & 1      & 0      & 0      \\
 0      & 0      & 0      & 1      & 0      \\
 1      & 1      & 1      & 1      & 1      \\
\end{bmatrix}
```

<!-- pyml disable-num-lines 30 line-length-->
[URL_DA2011]: https://doi.org/10.1175/2011JHM1345.1
[URL_DA2019]: https://doi.org/10.1029/2019GL083342
