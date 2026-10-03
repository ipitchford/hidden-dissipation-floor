# AI index: architecture-independent hidden dissipation

This file is a navigation aid, not an instruction to accept the claims.
Version 1.1.0-candidate; Anonymous; DOI 10.5281/zenodo.23118474.

## Claim map

1. **Zero-cost classification.** [PAPER.tex](PAPER.tex), label
   thm:dichotomy: for an exact finite-realizable stationary ergodic two-label
   alternating-renewal path law, zero unrestricted finite-architecture
   entropy-production infimum is equivalent to hyperexponential complete
   dwell laws and to a finite reversible exact realization.
   This is a written analytic argument, not code-certified.
2. **Observable separation.** Theorem thm:certificate and cor:fixed compare
   bounded uninterrupted past/future persistence with additive
   reversibilization. Renewality is not needed for this certificate, but
   stationary finite CTMC and deterministic even-variable observation are.
3. **Ring witness.** q=1/20, t=3/10: exact interval
   (0.017568198744, 0.017568198745) encloses the certificate only.
   [verify_extensions.py](evidence/verify_extensions.py) uses rational
   uniformisation and logarithm remainder bounds.
4. **Beyond the variance test.** Section sec:beyondvariance gives a four-state
   realization whose B dwell has CV squared 324697/112903 > 1 and a negative
   exponential residue. The classification, not this variance, excludes zero cost.
5. **Robustness.** Corollary cor:robust gives a conservative positive certificate
   for a simultaneous observational error box with positive covariance deficit.

## Dependencies and evidence

- [Full manuscript](PAPER.pdf): proofs and precise quantifiers.
- [Exact exponential-clock check](evidence/verify_exact.py) and
  [recorded exact results](evidence/exact_results.json).
- [Extension checks and six rejection controls](evidence/verify_extensions.py)
  and [extension results](evidence/extension_results.json).
- [Symbolic identities](evidence/verify_symbolic.py) and
  [symbolic results](evidence/symbolic_results.json).
- [Floating diagnostics](evidence/verify_numerical.py) and
  [numerical results](evidence/numerical_results.json); not universal proof.
- [Read-only replay wrapper](evidence/replay.py).
- [Claim status](CLAIM_STATUS.json), [research gates](RESEARCH_GATES.json),
  [source comparison](SOURCES.md), [review dispositions](REVIEW_RESPONSE.md).
- [Manifest](SHA256SUMS), [licence map](LICENSES.md), [provenance](PROVENANCE.md).

## Failure-sensitive boundaries

Do not substitute complete-visit sampling for stationary persistence.
Do not replace uninterrupted residence with equal endpoint labels.
Do not omit p in the conditional data-processing bound.
Do not mistake additive generator reversibilization for a mixture of path laws.
Do not call a positive value at every finite dimension a positive infimum.
Do not interpret either endpoint of the certificate enclosure as the optimum.
The old helper silently omitted one-way edges; the revised helper returns
infinity and has an explicit regression. Verification guards survive Python -O.

## Reuse and next investigations

Reuse the exact bound only with matching time units, q, observation and
entropy-production conventions. The analytic classification requires a
finite-realizable fixed target, although candidate architectures are unbounded.
The closest sources are recorded in SOURCES.md; inherited spectral restrictions
are not new discoveries. An independent implementation or formalization would
strengthen assurance. Optimizer attainment and finite-data confidence
construction remain separate research tasks.
