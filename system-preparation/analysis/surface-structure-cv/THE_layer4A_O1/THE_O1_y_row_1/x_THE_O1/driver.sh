rm analysis.* density
plumed driver --mf_xtc ../../../../THE170ASP170H2O6286Face001_T298_NVT.r0.part0001.xtc --plumed plumed.dat --timestep 0.002 --trajectory-stride 500
