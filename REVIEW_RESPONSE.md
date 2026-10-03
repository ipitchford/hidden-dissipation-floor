# Response to the supplied review

Version 1.1.0-candidate, 3 October 2026. Original v1.0 and supplied audit
hashes are in PROVENANCE.md. The review is supplied model-review evidence;
neither its prospective REF judgement nor a coordinated second checking
perspective establishes external human review.

| Request | Action and evidence |
|---|---|
| 4.1 exact prior-work positioning | PAPER.tex interpretation section and SOURCES.md distinguish inherited equilibrium mixtures, model fitting, dimension-free separation and zero-cost closure. Tu is credited via the established antecedent; its full proof was not inspected. |
| 4.2 foreground Theorem 7 | Full three-way equivalence displayed in the introduction and abstract. Original proof retained with explicit normalisations; theorem numbering changes after inserted corollaries. |
| 4.3 certificate versus optimisation | Fixed-window section separates chosen certificate, best-in-family certificate and unknown physical optimum; gives the physical bracket and warns its gap is not an error estimate. |
| 7 one-way numerical edges | rate() returns infinity for positive one-way flux. Directed three-cycle and reversible controls added. All verification assertions in revised exact/numerical scripts are explicit runtime guards. |
| 7 spectral normalisation | Restricted stationary measure explicitly unnormalised with mass p. |
| 7 mixture weights | alpha_j=c_j lambda_j/r_B and sum alpha_j=1 written out. |
| 7 bibliography | Ehrich journal DOI added; published papers and preprints distinguished; Skinner-Dunkel supplement equations and Tu antecedent identified. |
| 7 abstract | Self-contained architecture question; no commissioning-dependent opening. |
| Optional fixed-window certificate | Added cor:fixed; credits the supplied audit. New exact implementation encloses its bound; private supplied audit was separately replayed. |
| Optional example beyond variance | Added finite four-state model with CV squared >1 and negative exponential residue; exact stationary distribution, moments and transform identities checked. |
| Optional controlled uncertainty | Added deterministic simultaneous-box corollary and exact epsilon=1/10000 substitution. Statistical coverage, dependent data and data-adaptive window choice remain unproved. |

No unresolved mandatory correction remains in this revision. The original
analytic argument is not represented as a formally verified proof.
A control in the new interval implementation initially used a time outside
its declared x<=1 domain; it was corrected to t=1/5 for the equilibrium
control before release. The target certificate always remained within domain.

## Assessment boundary

The full positive optimum, finite-dimensional attainment, novel applications,
empirical transfer and worldwide priority remain open. No official REF rating
is claimed. The requested strengthening is substantive but does not warrant
promising a four-star assessment.
