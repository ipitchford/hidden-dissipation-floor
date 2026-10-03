#!/usr/bin/env python3
"""Optional all-parameter symbolic checks. Requires SymPy."""
import json
from pathlib import Path
import sympy as S
q,z=S.symbols('q z', positive=True)
s=1+q; c=1+q+q*q; p=S.Rational(2,3)
Q=S.Matrix([[-s,1,q],[q,-s,1],[1,q,-s]])
pi=S.Matrix([[S.Rational(1,3)]*3])
T=Q[1:3,1:3]; alpha=S.Matrix([[1/s,q/s]]); exits=S.Matrix([q,1])
D=z*z+2*s*z+c
f=(2*q*z/s+c)/D
checks={}
def test(name, expression):
    if isinstance(expression,S.MatrixBase):
        ok=all(S.simplify(x)==0 for x in expression)
    else:
        ok=S.factor(expression)==0
    if not ok: raise AssertionError((name,expression))
    checks[name]='PASS'
test('row sums', Q*S.ones(3,1))
test('stationarity', pi*Q)
test('exact B dwell transform', (alpha*(z*S.eye(2)-T).inv()*exits)[0]-f)
test('mean B dwell',-S.diff(f,z).subs(z,0)-2/s)
test('second B dwell moment',S.diff(f,z,2).subs(z,0)-6/c)
H=(2*z+3*s)/(3*D)
test('persistence from renewal identity', H-(p/z-s*(1-f)/(3*z*z)))
test('persistence from killed generator', H-(S.Matrix([[S.Rational(1,3)]*2])*(z*S.eye(2)-T).inv()*S.ones(2,1))[0])
a=z*H/p
b=-z*z*S.diff(H,z)/p
delta=z*z*(1-q)**2/(4*D*D)
test('clock b formula',b-z*z*(z+q+2)*(z+2*q+1)/D**2)
test('negative covariance', a*a-b-delta)
quadratic=p*z*delta**2/(a*a*(1-a)**2)
test('closed quadratic floor',quadratic-p*z**3*(1-q)**4/((2*z+3*s)**2*(s*z+2*c)**2))
x,u,v,d=S.symbols('a u v delta',real=True)
r=[(1-x)**2,x*(1-x),x*(1-x),x*x]
w=[r[0]-d,r[1]+d,r[2]+d,r[3]-d]
target=[1-2*u+v,u-v,u-v,v]
test('information projection supporting inequality',1-sum(ww*rr/ss for ww,rr,ss in zip(w,target,r))-d*(v-2*x*u+x*x)/(x*x*(1-x)**2))
test('cubic C0',1/r[0]+2/r[1]+1/r[3]-1/(x*x*(1-x)**2))
test('cubic C1',1/r[0]**2-2/r[1]**2+1/r[3]**2-(2*x-1)**2/(x**4*(1-x)**4))
report={'status':'PASS','sympy_version':S.__version__,'checks':checks,
        'scope':'Polynomial/rational identities only; analytic inequalities are proved in manuscript.'}
Path(__file__).with_name('symbolic_results.json').write_text(json.dumps(report,indent=2)+'\n')
print('PASS:',len(checks),'all-parameter symbolic identities')
