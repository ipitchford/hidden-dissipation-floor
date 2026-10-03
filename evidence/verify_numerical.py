#!/usr/bin/env python3
"""Independent floating-point diagnostics, NOT a proof.

Random irreducible chains with many hidden states test the symmetrization
rate inequality, equilibrium clock positivity, and universal clock bound.
Requires NumPy and SciPy. No Monte Carlo trajectory estimates are used.
"""
import json
from pathlib import Path
import numpy as np
from scipy.linalg import solve


def stationary(Q):
    A=Q.T.copy(); rhs=np.zeros(len(Q)); A[-1,:]=1;rhs[-1]=1
    return solve(A,rhs)


def rate(Q,pi):
    F=pi[:,None]*Q
    result=0.0
    for i in range(len(Q)):
        for j in range(i+1,len(Q)):
            x,y=F[i,j],F[j,i]
            if (x > 0 and y == 0) or (y > 0 and x == 0):
                return float('inf')
            if x>0 and y>0: result+=(x-y)*np.log(x/y)
    return result


def kl_rate(Q,R,pi):
    n=len(Q); total=0.0
    for i in range(n):
        for j in range(n):
            if i!=j and Q[i,j]>0:
                total+=pi[i]*Q[i,j]*np.log(Q[i,j]/R[i,j])
    return total


def clock(Q,pi,B,z):
    T=Q[np.ix_(B,B)]; p=pi[B].sum(); one=np.ones(len(B))
    x=solve(z*np.eye(len(B))-T,one)
    y=solve(z*np.eye(len(B))-T,x)
    a=z*pi[B]@x/p;b=z*z*pi[B]@y/p
    return p,a,b


def mi(a,b):
    w=np.array([1-2*a+b,a-b,a-b,b])
    r=np.array([(1-a)**2,a*(1-a),a*(1-a),a*a])
    if not (w.min()>-1e-12): raise AssertionError("verification check failed")
    return sum(x*np.log(x/y) for x,y in zip(w,r) if x>0)


def main():
    directed=np.array([[-1,1,0],[0,-1,1],[1,0,-1]],float)
    if not np.isinf(rate(directed,np.ones(3)/3)):
        raise RuntimeError('one-way flux must have infinite entropy production')
    if rate(np.array([[-1,1],[1,-1]],float),np.ones(2)/2) != 0:
        raise RuntimeError('reversible chain must have zero entropy production')
    rng=np.random.default_rng(603102026)
    tests=0;negative=0;max_kl_ratio=0.0;max_bound_ratio=0.0
    for n in [3,4,5,8,12,20]:
        for _ in range(30):
            Q=np.exp(rng.uniform(-2,2,(n,n)))
            np.fill_diagonal(Q,0);Q-=np.diag(Q.sum(axis=1))
            pi=stationary(Q); rev=Q.T*pi[None,:]/pi[:,None]
            R=(Q+rev)/2
            if not (np.max(np.abs(np.diag(Q)-np.diag(R)))<1e-9): raise AssertionError("verification check failed")
            if not (np.max(np.abs(pi@R))<1e-9): raise AssertionError("verification check failed")
            if not (np.max(np.abs(pi[:,None]*R-(pi[:,None]*R).T))<1e-9): raise AssertionError("verification check failed")
            sigma=rate(Q,pi);k=kl_rate(Q,R,pi)
            if not (k<=sigma/4+1e-10): raise AssertionError("verification check failed")
            max_kl_ratio=max(max_kl_ratio,k/sigma)
            B=np.arange(n//2,n); z=float(np.exp(rng.uniform(-1,3)))
            p,a,b=clock(Q,pi,B,z)
            _,ar,br=clock(R,pi,B,z)
            if not (br>=ar*ar-1e-11): raise AssertionError("verification check failed")
            if b<a*a-1e-10:
                negative+=1; lower=2*z*p*mi(a,b)
                if not (lower<=sigma+1e-10): raise AssertionError("verification check failed")
                max_bound_ratio=max(max_bound_ratio,lower/sigma)
            tests+=1
    # Known family with exact two-phase killed law, including near equilibrium.
    family=[]
    for q in [.001,.05,.2,.7,.95,.99,1,2]:
        s=1+q; Q=np.array([[-s,1,q],[q,-s,1],[1,q,-s]],float)
        pi=np.ones(3)/3
        for z in [.1,1,6,20]:
            p,a,b=clock(Q,pi,np.array([1,2]),z)
            D=z*z+2*s*z+1+q+q*q
            expected=z*z*(1-q)**2/(4*D*D)
            if not (abs(a*a-b-expected)<2e-14): raise AssertionError("verification check failed")
            lower=2*z*p*mi(a,b) if expected>1e-12 else 0.0
            sigma=rate(Q,pi)
            if not (lower<=sigma+1e-10): raise AssertionError("verification check failed")
            family.append(dict(q=q,z=z,sigma=sigma,clock_bound=lower))
    # Information projection: negative-correlated data vs arbitrary mixtures of Bernoullis.
    projection_tests=0
    for _ in range(1000):
        a=float(rng.uniform(.05,.95));delta=float(rng.uniform(.001,.999))*min(a*a,(1-a)**2)
        b=a*a-delta;w=np.array([1-2*a+b,a-b,a-b,b])
        params=rng.uniform(.01,.99,5);weights=rng.dirichlet(np.ones(5))
        u=weights@params;v=weights@(params**2)
        r=np.array([1-2*u+v,u-v,u-v,v])
        if not (sum(w*np.log(w/r))>=mi(a,b)-1e-12): raise AssertionError("verification check failed")
        projection_tests+=1
    report=dict(status='PASS',seed=603102026,random_chain_tests=tests,
                negative_covariance_random_cases=negative,
                maximum_KL_rate_over_sigma=max_kl_ratio,
                maximum_random_clock_bound_over_sigma=max_bound_ratio,
                information_projection_tests=projection_tests,family_tests=family,
                scope='Floating-point diagnostics; not proof and not global optimization.')
    Path(__file__).with_name('numerical_results.json').write_text(json.dumps(report,indent=2)+'\n')
    print('PASS:',tests,'random chain tests;',projection_tests,'projection tests;',len(family),'family tests')

if __name__=='__main__': main()
