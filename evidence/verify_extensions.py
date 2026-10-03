#!/usr/bin/env python3
"""Exact v1.1 checks; explicit guards remain active under python -O.

Independently coded interval evaluation of the supplied referee's fixed-window
corollary, plus rational extension and semantic negative controls. Not a formal
verification of the analytic theorems. Standard library only.
"""
from fractions import Fraction as F
from decimal import Decimal, localcontext
import json
from pathlib import Path

def require(v, message):
    if not v:
        raise ValueError(message)

def box(x):
    return x if isinstance(x, tuple) else (F(x), F(x))

def add(x, y):
    x,y=box(x),box(y)
    return x[0]+y[0],x[1]+y[1]

def neg(x):
    x=box(x)
    return -x[1],-x[0]

def sub(x,y):
    return add(x,neg(y))

def mul(x,y):
    x,y=box(x),box(y)
    p=[a*b for a in x for b in y]
    return min(p),max(p)

def div(x,y):
    y=box(y)
    require(not y[0]<=0<=y[1], 'interval division through zero')
    return mul(x,(1/y[1],1/y[0]))

def logarithm(x,n=40):
    x=F(x); require(x>0,'log domain')
    y=(x-1)/(x+1)
    s=sum((2*y**(2*k+1)/F(2*k+1) for k in range(n)),F(0))
    e=2*abs(y)**(2*n+1)/((2*n+1)*(1-y*y))
    return s-e,s+e

def persistence(t,q=F(1,20),n=32):
    s=1+q; x=s*t
    require(q>0 and 0<=x<=1 and n%2==0,'uniformisation domain')
    # e^-x alternating enclosure; positive Poisson series tail enclosure.
    term=F(1); upper=F(1); series=F(1); v=(F(1),F(1))
    for k in range(1,n+1):
        term*=x/k
        upper+=(-1)**k*term
        v=(v[1]/s,q*v[0]/s)
        c=sum(v)/2
        require(0<=c<=1,'substochastic coefficient')
        series+=term*c
    tailterm=term*x/(n+1)
    return mul((upper-tailterm,upper),(series,series+tailterm/(1-x/(n+2))))

def information(a,b):
    w=[add(sub(1,mul(2,a)),b),sub(a,b),sub(a,b),b]
    c=sub(1,a); r=[mul(c,c),mul(a,c),mul(a,c),mul(a,a)]
    total=box(0)
    for wi,ri in zip(w,r):
        require(wi[0]>0 and ri[0]>0,'nonpositive probability cell')
        ratio=div(wi,ri)
        log=(logarithm(ratio[0])[0],logarithm(ratio[1])[1])
        total=add(total,mul(wi,log))
    return total

def robust(p0,a0,b1,z):
    require(p0>0 and a0>=0 and z>0,'robust domain')
    eta=a0*a0-b1
    require(eta>0,'nonpositive covariance deficit')
    return 16*z*p0*eta*eta

def enclosed(x,lo,hi):
    require(F(lo)<x[0]<=x[1]<F(hi),'claimed certificate enclosure fails')

def main():
    t=F(3,10); a=persistence(t); b=persistence(2*t)
    require(sub(mul(a,a),b)[0]>0,'negative covariance not established')
    bound=mul(F(4,3)/t,information(a,b))
    enclosed(bound,'0.017568198744','0.017568198745')
    # Equilibrium is a control, not a positive witness.
    ae=persistence(F(1,5),F(1)); be=persistence(F(2,5),F(1))
    deficit=sub(mul(ae,ae),be)
    require(deficit[0]<=0<=deficit[1],'equilibrium control')
    # High-variance example: integrate its signed density exactly.
    weights=[F(81,160),-F(49,160),F(1,200)]
    rates=[F(3,4),F(7,4),F(1,100)]
    require(sum(w/r for w,r in zip(weights,rates))==1,'density mass')
    mean=sum(w/r**2 for w,r in zip(weights,rates))
    second=sum(2*w/r**3 for w,r in zip(weights,rates))
    cv=second/mean**2-1
    require((mean,second,cv)==(F(254,5),F(70016,7),F(324697,112903)),'moment identities')
    Q=[[-1,F(2,5),F(1,10),F(1,2)], [F(1,4),-F(5,4),1,0],
       [1,F(1,4),-F(5,4),0], [F(1,100),0,0,-F(1,100)]]
    pi=[F(5,259),F(2,259),F(2,259),F(250,259)]
    require(all(sum(row)==0 for row in Q),'generator rows')
    require(all(sum(pi[i]*Q[i][j] for i in range(4))==0 for j in range(4)),'stationarity')
    # Exact resolvent identity, checked symbolically by coefficient cross-products
    # (81/80)/(z+3/4)-(49/80)/(z+7/4) = ((2/5)z+21/16)/D.
    require(F(81,80)-F(49,80)==F(2,5),'ring numerator slope')
    require(F(81,80)*F(7,4)-F(49,80)*F(3,4)==F(21,16),'ring numerator constant')
    eps=F(1,10000)
    floor=robust(F(2,3)-eps,F(18180,19861)-eps,F(329212800,394459321)+eps,F(6))
    require(floor>0,'uncertainty floor')
    failures=0
    for task in [lambda: enclosed(bound,'0.018','0.019'),
                 lambda: robust(F(1,2),F(1,2),F(1,3),F(6)),
                 lambda: robust(F(1,2),-F(1,2),F(0),F(6)),
                 lambda: div(1,(-F(1),F(1))),
                 lambda: logarithm(0),
                 lambda: persistence(F(2))]:
        try: task()
        except ValueError: failures+=1
    require(failures==6,'negative control accepted a false claim')
    with localcontext() as ctx:
        ctx.prec=40
        decimal=lambda x:str(Decimal(x.numerator)/Decimal(x.denominator))
        out={'status':'PASS','fixed_window_enclosure':['0.017568198744','0.017568198745'],
             'interval_width':decimal(bound[1]-bound[0]),'high_variance_cv_squared':str(cv),
             'uncertainty_halfwidth':str(eps),'robust_floor_exact':str(floor),
             'robust_floor_decimal_diagnostic':decimal(floor),'semantic_negative_controls':failures,
             'scope':'Exact arithmetic; analytic proof and source comparison remain separate obligations.'}
    Path(__file__).with_name('extension_results.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2))

if __name__=='__main__': main()
