# Sandbox

RAPID comes along with a set of test files based on a synthetic experiment.

## Study Domain

The geographic domain is the same that was used for illustration of the
matrix-based Muskingum method equations that were originally developed in
[David et al. (2011)][URL_DA2011].

The temporal domain of the simulation starts at Unix Epoch, *i.e.* on
1970-01-01 at 00:00:00 Universal Time, and lasts for 10 consecutive days.

## River Network

The river network used is composed of five reaches connected by two
confluences. The corresponding network matrix is:

```math
\mathbf{N} =
\begin{bmatrix}
 0      & 0      & 0      & 0      & 0      \\
 0      & 0      & 0      & 0      & 0      \\
 1      & 1      & 0      & 0      & 0      \\
 0      & 0      & 0      & 0      & 0      \\
 0      & 0      & 1      & 1      & 0
\end{bmatrix}
```

## Gauging Stations

Two gaging stations are contained within the network. The associated
selection matrix is:

```math
\mathbf{S} =
\begin{bmatrix}
 0      & 0      & 1      & 0      & 0      \\
 0      & 0      & 0      & 0      & 1
\end{bmatrix}
```

## Model Parameters

RAPID uses the Muskingum method for river routing, which requires two
parameters for each river reach.

The Muskingum time parameter (s) vector used here is:

```math
\mathbf{k} =
\begin{bmatrix}
 9000   \\
 9000   \\
 9000   \\
 9000   \\
 9000
\end{bmatrix}
```

The Muskingum non-dimensional parameter (-) vector used here is:

```math
\mathbf{x} =
\begin{bmatrix}
 0.250  \\
 0.250  \\
 0.250  \\
 0.250  \\
 0.250
\end{bmatrix}
```

The routing time step (s) used for simulations is set to:

```math
\Delta t = 900
```

With these, the Muskingum parameter matrices become
([David et al. 2011][URL_DA2011]):

```math
\mathbf{C_1} =
\begin{bmatrix}
-0.250  &  0.    &  0.    &  0.    &  0.    \\
 0.     & -0.250 &  0.    &  0.    &  0.    \\
 0.     &  0.    & -0.250 &  0.    &  0.    \\
 0.     &  0.    &  0.    & -0.250 &  0.    \\
 0.     &  0.    &  0.    &  0.    & -0.250
\end{bmatrix}
```

```math
\mathbf{C_2} =
\begin{bmatrix}
 0.375 &  0.    &  0.    &  0.    &  0.    \\
 0.    &  0.375 &  0.    &  0.    &  0.    \\
 0.    &  0.    &  0.375 &  0.    &  0.    \\
 0.    &  0.    &  0.    &  0.375 &  0.    \\
 0.    &  0.    &  0.    &  0.    &  0.375
\end{bmatrix}
```

```math
\mathbf{C_3} =
\begin{bmatrix}
 0.875 &  0.    &  0.    &  0.    &  0.    \\
 0.    &  0.875 &  0.    &  0.    &  0.    \\
 0.    &  0.    &  0.875 &  0.    &  0.    \\
 0.    &  0.    &  0.    &  0.875 &  0.    \\
 0.    &  0.    &  0.    &  0.    &  0.875
\end{bmatrix}
```

The three Muskingum parameter matrices always satisfy the following equality:

```math
\mathbf{C_1} + \mathbf{C_2} + \mathbf{C_3} =
\begin{bmatrix}
 1.000 &  0.    &  0.    &  0.    &  0.    \\
 0.    &  1.000 &  0.    &  0.    &  0.    \\
 0.    &  0.    &  1.000 &  0.    &  0.    \\
 0.    &  0.    &  0.    &  1.000 &  0.    \\
 0.    &  0.    &  0.    &  0.    &  1.000
\end{bmatrix}
```

## True External Inflow

We assume that the flow of water coming from the exterior of the network
and feeding into each reach of the network is a square wave function, *i.e.* a
periodic waveform that alternates between two fixed levels, switching
instantaneously between them. This "true" external flow into the network is
here defined as:

```math
\mathbf{Q^{eT}}(t) =
\begin{bmatrix}
 10     \\
 10     \\
 10     \\
 20     \\
 20
\end{bmatrix}
+
\begin{bmatrix}
 1      \\
 1      \\
 1      \\
 2      \\
 2
\end{bmatrix}
\cdot
\operatorname{sgn}\!\left( \sin\!\left(\tfrac{\pi t}{86400}
+
\varepsilon\right) \right)
```

where $\operatorname{sgn}(\cdot)$ is the sign function and $\varepsilon$ is a
small offset (e.g., $10^{-7}$) introduced to avoid the undefined case
$\operatorname{sgn}(0) = 0$.

Thus, for each reach, the inflow alternates every 86,400 seconds (one day)
between the a mean value plus and minus an amplitude.

## True Observations

This "true" inflow is used to generate the synthetic gage observations:

```math
\mathbf{g^{T}}(t)
```

## Notable Matrices

Some notable matrices related to matrix-based Muskingum routing include
([David et al. 2011][URL_DA2011]):

```math
\mathbf{I} - \mathbf{C_1} \cdot \mathbf{N} =
\begin{bmatrix}
 1.     &  0.    &  0.    &  0.    &  0.    \\
 0.250  &  0.250 &  0.    &  0.    &  0.    \\
 0.     &  0.    &  1.    &  0.    &  0.    \\
 0.     &  0.    &  0.    &  1 .   &  0.    \\
 0.     &  0.    &  0.250 &  0.250 &  1.
\end{bmatrix}
```

```math
(\mathbf{I} - \mathbf{C_1} \cdot \mathbf{N})^{-1} =
\begin{bmatrix}
 1.     &  0.    &  0.    &  0.    &  0.    \\
 0.250  &  0.250 &  0.    &  0.    &  0.    \\
 0.     &  0.    &  1.    &  0.    &  0.    \\
 0.     &  0.    &  0.    &  1 .   &  0.    \\
 0.0625 &  0.0625&  0.250 &  0.250 &  1.
\end{bmatrix}
```

In some cases, lumped routing is used for monthly simulations, *i.e* water is
assumed to be transported at an infinite speed from source to sink within the
river network. Notable matrices related to lumped routing as described in
[David et al. (2019)][URL_DA2019]
include:

```math
\mathbf{I} - \mathbf{N} =
\begin{bmatrix}
 1      & 0      & 0      & 0      & 0      \\
 0      & 1      & 0      & 0      & 0      \\
-1      &-1      & 1      & 0      & 0      \\
 0      & 0      & 0      & 1      & 0      \\
 0      & 0      &-1      &-1      & 1
\end{bmatrix}
```

```math
(\mathbf{I} - \mathbf{N})^{-1} =
\begin{bmatrix}
 1      & 0      & 0      & 0      & 0      \\
 0      & 1      & 0      & 0      & 0      \\
 1      & 1      & 1      & 0      & 0      \\
 0      & 0      & 0      & 1      & 0      \\
 1      & 1      & 1      & 1      & 1
\end{bmatrix}
```

> Note: we use
> [StackEdit][URL_STCKED],
> an online Markdown editor with MathJax support to test drive our equations
> before pushing to GitHub. We replace code blocks by `$$` blocks during test
> drive.

<!-- pyml disable-num-lines 30 line-length -->
[URL_DA2011]: https://doi.org/10.1175/2011JHM1345.1
[URL_DA2019]: https://doi.org/10.1029/2019GL083342
[URL_STCKED]: https://stackedit.io/
