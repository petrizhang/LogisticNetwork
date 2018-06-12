/*********************************************
 * OPL 12.8.0.0 Model
 * Author: pcz
 * Creation Date: 2018年6月11日 at 上午10:44:24
 *********************************************/
 

int N = 81;
int numPairs = 2 * N * N;
range r = 1..N;
int D[r][r]=...;
int T[r][r]=...;
int F[r][r]=...;
float scale = 100000;
float numPairsXscale = numPairs * scale;

float U[r]=...;

dvar boolean A[r][r];
dvar boolean Y[r];

dexpr float updateCost = sum(k in r) U[k]*Y[k];

dexpr float opCost = 
  sum(i,j,k,m in r) 
    (A[i][k]*A[j][m]) * F[i][j] * (D[i][k]+D[k][m]+D[m][j]) / numPairsXscale;
    
dexpr float transTime = 
  sum(i,j,k,m in r) 
    (A[i][k]*A[j][m]) * (T[i][k]+T[k][m]+T[m][j]) / numPairs;

minimize updateCost+opCost+transTime;
 
subject to{ 
  forall(i,k in r) 
    A[i][k] <= Y[k];
  forall(i in r)
    sum(k in r)
      A[i][k] == 1;
} 
 
 
