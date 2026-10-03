# Hidden dissipation without a known architecture

Anonymous. Version 1.1.0-candidate, 3 October 2026.
DOI: https://doi.org/10.5281/zenodo.23118474
Repository: https://github.com/ipitchford/hidden-dissipation-floor

This unrefereed mathematical candidate classifies zero all-dimension entropy-production cost for **finite-realizable stationary ergodic two-label alternating-renewal laws**. Zero infimum, hyperexponential complete dwell laws, and a finite reversible exact realization are equivalent. Finite hidden CTMCs, deterministic observation and ordinary even-variable reversal are essential assumptions.

The established equilibrium spectral restriction is credited to prior work. The additional closure argument permits unbounded hidden dimensions and rates in the vanishing-cost sequence. No worldwide-priority certification is made.

For the three-state-ring observation at q=1/20, the fixed-window certificate is enclosed strictly between 0.017568198744 and 0.017568198745. Thus the unknown physical optimum exceeds the first number; the second is an upper bound on the **certificate**, not on that optimum. The available physical upper bound is (19/20) log 20.

## Start here

- [Paper](PAPER.pdf) and [editable source](PAPER.tex).
- [AI index](AI_INDEX.md): claims, dependencies, checker entry points and limits.
- [Review response](REVIEW_RESPONSE.md): every mandatory and optional request.
- [Sources and reading](SOURCES.md), [research gates](RESEARCH_GATES.json).
- [Claim status](CLAIM_STATUS.json), [provenance](PROVENANCE.md), [licences](LICENSES.md).

## Reproduce

Exact arithmetic needs Python 3.10 or newer and no external package:

```sh
python3 evidence/verify_exact.py
python3 evidence/verify_extensions.py
python3 -O evidence/verify_exact.py
python3 -O evidence/verify_extensions.py
```

For the symbolic and floating-point diagnostics install the pinned
[optional requirements](requirements-optional.txt) in an isolated environment,
then run `python3 evidence/replay.py`. It checks the manifest, copies the
evidence to a temporary directory, executes all four programs normally and
with `-O`, compares exact outputs, and leaves the released package unchanged.
Floating diagnostics have their declared tolerances; bitwise portability is
not promised. The publication environment was Python 3.13, SymPy 1.14.0,
NumPy 2.4.4 and SciPy 1.17.1.

The exact scripts certify substitutions and interval bounds. The symbolic
script checks thirteen rational identities. Random-chain diagnostics are
implementation checks, not proofs of universal claims. The analytic arguments
are in the manuscript. No formal proof assistant, external human peer review,
or unaffiliated reproduction is established.

## Limits and reuse

The positive optimum and its attainment remain open. The uncertainty-box
corollary assumes a valid simultaneous box; it does not construct statistical
confidence sets or justify data-adaptive window selection. Nonrenewal laws,
odd time-reversal variables and nonstationary systems lie outside the
classification. No empirical biological or engineering effect is measured.

Original prose, diagrams and data: CC0-1.0. Original code: MIT. Third-party
literature retains its own terms. Supplied reviewer material informed revision
but is not redistributed in this package.
