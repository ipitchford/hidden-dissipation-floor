# Analytic review notes and claim boundaries

Historical v1.0 notes retained for provenance. For the revised v1.1 findings,
extensions and current assurance boundary, see REVIEW_RESPONSE.md and
CLAIM_STATUS.json. These notes are not an external peer-review report.

## What was checked

**Target fidelity.** The source's complete B-dwell transform is
((2q/(1+q))z + 1+q+q^2)/(z^2+2(1+q)z+1+q+q^2); A has exponential
rate 1+q. An explicit three-state ring reproduces this transform exactly.
The single A state resets successive visits, establishing the entire
alternating-renewal law, not only two marginal dwell distributions.

**Unrestricted architecture.** The lower-bound argument starts from an
arbitrary finite exact realization with any number of states in either
visible block. It does not assume a single microscopic A state, a minimal
phase-type representation, a prescribed graph, bounded activity, or
uniformly bounded rates. The comparison reversible model need not realize
the target. No compactification theorem from the source is required.

**Entropy-production convention.** The sum is over unordered edges:
(F_ij-F_ji) log(F_ij/F_ji). The equivalent ordered-edge entropy sum has no
additional factor 1/2. Used edges without reverse flux have infinite cost.

**Path comparison.** Additive reversibilization preserves stationary mass
and every exit rate. Holding-time likelihood terms cancel. The scalar
flux inequality gives KL_rate(Q || R) <= sigma(Q)/4. This does not identify
the path law of R with a mixture of the forward and reversed path laws.

**Random window.** Two independent, external Exp(z) clocks have total mean
length 2/z. Conditioning on clock lengths and using stationarity gives
KL <= sigma/(2z). There is no optional-stopping argument or independence
assumption about increments of the observed process.

**Two-clock observation.** The tests ask whether the path remains in B
throughout the respective half-window. They are not endpoint coincidences.
Under hidden equilibrium, past and future are conditionally independent
and identically distributed given the present microscopic state. Mixture
therefore gives nonnegative covariance, regardless of hidden dimension.

**Conditional data processing.** The present B probability is p under
both Q and its reversibilization. Retaining B/not-B and, only on B, the
binary tests gives the factor p in sigma/(2z) >= p D(w || w_R).

**Information projection.** The relative entropy direction is target to
comparison. The projection onto symmetric binary laws with nonnegative
covariance is the product law with the target marginal. Its supporting
inequality is explicit and is checked symbolically. No convexity of the
parameter region is assumed.

**Rational bound.** The information's second derivative has an exact
linear lower bound. Twice integrating yields the quadratic plus cubic
expression. The explicit substitution q=1/20, z=6 gives the stated
fraction and strictly positive rational margin over 1/125. A separate
rational logarithm enclosure verifies the stronger certificate.

**General dichotomy.** Vanishing entropy forces persistence functions to
be limits of positive exponential mixtures. Weak compactness after the
change of variable x=exp(-lambda), continuity at zero, and decay at
infinity preserve the positive mixture representation. Finite realizability
of the fixed target then supplies a constant-coefficient ODE, which forces
the positive spectral measure onto finitely many roots. A reversible
bipartite construction proves sufficiency for independent alternating
renewal visits. The sufficiency is not asserted for general nonrenewal
processes on the basis of marginal dwell distributions alone.

## What the checks are not

These are analytic self-checks plus separate algebraic and numerical
implementations performed in this research workflow. They are not an
external independent referee report, a proof-assistant certificate, or an
exhaustive prior-art search. Random tests cannot establish a universal
inequality; the manuscript supplies its proof.

## Remaining questions beyond the specified zero/nonzero target

The exact positive all-dimension infimum and its finite-dimensional
attainment are not settled. The explicit ring is an upper-bound competitor,
not an optimizer. No claim covers odd time-reversal variables, nonstationary
driving, diffusion models, or observation mechanisms outside the specified
finite-CTMC deterministic-observation class.
