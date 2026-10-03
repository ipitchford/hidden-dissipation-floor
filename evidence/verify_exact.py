#!/usr/bin/env python3
"""Exact arithmetic for the explicit dissipation-floor certificate.

Python standard library only. No simulation or optimizer is used.
Analytic lemmas are proved in PAPER.pdf; this checks their substitutions,
normalizations, exact margin, and a rigorous logarithmic enclosure.
"""
from fractions import Fraction as F
import json
from pathlib import Path


def enc(x):
    if isinstance(x, F):
        return {"numerator": x.numerator, "denominator": x.denominator,
                "decimal_diagnostic": float(x)}
    if isinstance(x, dict):
        return {k: enc(v) for k, v in x.items()}
    if isinstance(x, (list, tuple)):
        return [enc(v) for v in x]
    return x


def log_interval(x: F, terms: int = 64):
    """Rational enclosure using log x = 2 sum y^(2k+1)/(2k+1).

    y=(x-1)/(x+1). Absolute remainder is at most
    2 |y|^(2m+1)/((2m+1)(1-y^2)). All operations are exact.
    """
    if x <= 0:
        raise ValueError("log argument must be positive")
    y = (x - 1) / (x + 1)
    value = 2 * sum((y ** (2*k+1) / (2*k+1)
                     for k in range(terms)), F(0))
    error = 2 * abs(y) ** (2*terms+1) / ((2*terms+1)*(1-y*y))
    return value-error, value+error


def certificate(q: F, rate: F):
    if q <= 0 or rate <= 0:
        raise ValueError("q and rate must be positive")
    s = 1+q
    c = 1+q+q*q
    p = F(2,3)
    d = rate*rate+2*s*rate+c
    a = rate*(2*rate+3*s)/(2*d)
    b = rate*rate*(rate+q+2)*(rate+2*q+1)/(d*d)
    delta = a*a-b
    if not (delta == rate*rate*(1-q)**2/(4*d*d)): raise AssertionError("verification check failed")
    if not (0 < a < 1 and delta >= 0): raise AssertionError("verification check failed")
    w = [1-2*a+b, a-b, a-b, b]
    independent = [(1-a)**2, a*(1-a), a*(1-a), a*a]
    if not (min(w) > 0 and min(independent) > 0): raise AssertionError("verification check failed")
    if not (sum(w) == sum(independent) == 1): raise AssertionError("verification check failed")
    if not (w[1]+w[3] == w[2]+w[3] == a): raise AssertionError("verification check failed")
    if not ([x-y for x,y in zip(w,independent)] == [-delta,delta,delta,-delta]): raise AssertionError("verification check failed")
    c0 = 1/(a*a*(1-a)**2)
    c1 = (2*a-1)**2/(a**4*(1-a)**4)
    if not (c0 == 1/independent[0]+2/independent[1]+1/independent[3]): raise AssertionError("verification check failed")
    if not (c1 == 1/independent[0]**2-2/independent[1]**2+1/independent[3]**2): raise AssertionError("verification check failed")
    quadratic = rate*p*c0*delta*delta
    cubic = 2*rate*p*(c0*delta**2/2+c1*delta**3/6)
    pinsker = 16*rate*p*delta**2
    ilow, ihigh = F(0), F(0)
    for x,y in zip(w,independent):
        lo,hi = log_interval(x/y)
        ilow += x*lo
        ihigh += x*hi
    lower, upper = 2*rate*p*ilow, 2*rate*p*ihigh
    if not (lower >= cubic): raise AssertionError("verification check failed")
    if not (quadratic >= pinsker): raise AssertionError("verification check failed")
    return dict(q=q, clock_rate=rate, occupation_probability=p,
                denominator=d, a=a, b=b, delta=delta,
                joint=w, independent=independent,
                pinsker_floor=pinsker, quadratic_floor=quadratic,
                cubic_floor=cubic,
                logarithmic_floor_enclosure=[lower,upper],
                logarithmic_enclosure_width=upper-lower)


def main():
    c6=certificate(F(1,20),F(6))
    expected=F(182774933998705388800,22434692075028399713067)
    if not (c6['cubic_floor'] == expected): raise AssertionError("verification check failed")
    margin = expected-F(1,125)
    if not (margin == F(412174674809773886933,2804336509378549964133375)): raise AssertionError("verification check failed")
    if not (margin > 0): raise AssertionError("verification check failed")
    log_lo,log_hi=c6['logarithmic_floor_enclosure']
    if not (F(84471687960,10**13) < log_lo < log_hi < F(84471687962,10**13)): raise AssertionError("verification check failed")
    # The lower bound is a bound on entropy production, not its optimal value.
    report={
        'status':'PASS',
        'arithmetic':'exact fractions, including logarithmic remainder enclosure',
        'q_1_20_rate_1':certificate(F(1,20),F(1)),
        'q_1_20_rate_2':certificate(F(1,20),F(2)),
        'q_1_20_rate_6':c6,
        'claimed_simple_floor':F(1,125),
        'strict_margin_over_simple_floor':margin,
        'analytic_proof_required':True,
        'not_a_formal_proof_assistant_certificate':True,
        'checks':['clock moment identity','probability normalization',
                  'negative covariance identity','relative entropy cubic coefficients',
                  'exact rational dissipation floor','strict margin over 1/125',
                  'rigorous logarithm interval','quadratic dominates Pinsker']
    }
    # Rational stress substitutions, including equilibrium and q>1.
    count=0
    for q in [F(1,1000),F(1,20),F(1,3),F(9,10),F(999,1000),F(1),F(2),F(20)]:
        for z in [F(1,100),F(1,2),F(1),F(6),F(100)]:
            cc=certificate(q,z)
            if not ((cc['delta']==0) == (q==1)): raise AssertionError("verification check failed")
            count += 1
    report['exact_stress_substitutions']=count
    out=Path(__file__).with_name('exact_results.json')
    out.write_text(json.dumps(enc(report),indent=2)+'\n')
    print('PASS: exact rational certificate; all',count,'stress substitutions')
    print('Certified rate floor:',expected,'>',F(1,125))
    print('Stronger logarithmic certificate:',float(log_lo),float(log_hi))
    print('Report:',out)

if __name__=='__main__':
    main()
