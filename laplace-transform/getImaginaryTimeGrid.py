#!/usr/bin/python
import sys
import os
import re

def Delta(o):
  hIndices = "".join(map(chr,range(ord("i"),ord("i")+o)));
  pIndices = "".join(map(chr,range(ord("a"),ord("a")+o)));
  return "Delta^" + pIndices + "_" + hIndices

def Eps(o):
  return \
    "".join(map(lambda x: "+eps_"+chr(x),range(ord("a"),ord("a")+o))) + \
    "".join(map(lambda x: "-eps_"+chr(x),range(ord("i"),ord("i")+o)))

n = int(sys.argv[1]) if len(sys.argv) > 1 else 7
# note, currently, only the quotient is used. order is irrelevant
o = int(sys.argv[2]) if len(sys.argv) > 2 else 2

print("""\
Generating integration grid (tau_n,w_n) with N = {n} samples,
for order = {order}, such that
 sum_n=1^N w_n exp(-tau_n*{delta})) ~ 1/{delta}
with {delta} = {eps}""".format(delta=Delta(o), eps=Eps(o), order=o, n=n)
)

# turn into 2 digit number for fetching the source file
n = "%02d" % n

holes = list(map(float,open("HoleEigenEnergies.dat").readlines()[2:]))
particles = list(map(float,open("ParticleEigenEnergies.dat").readlines()[2:]))
mu = (holes[-1]+particles[0])/2
minDelta = o*(particles[0]-holes[-1])
maxDelta = o*(particles[-1]-holes[0])
R = maxDelta/minDelta
print("""\
mu = (max(eps_i)+min(eps_a))/2 = {mu}
min({delta}) = {min}
max({delta}) = {max}
R = max/min = {R}""".format(
    mu=mu, delta=Delta(o), min=minDelta, max=maxDelta, R=R
  )
)

# get base and exponent in scientif notation
R_scientific = "%1.0e" % R
R_exponent = int(R_scientific.split("e")[1])
# make sure FACTOR*10^EXPONENT is >= R
R += float("0.5e"+str(R_exponent))
R_scientific = "%1.0e" % R
R_factor = int(R_scientific.split("e")[0])
R_exponent = int(R_scientific.split("e")[1])

# fetch suitable file
file_name = "1_xk%s.%d_%d" % (n,R_factor,R_exponent)
tar_name = os.path.dirname(sys.argv[0]) + "/" + "1_x.tar.bz2"
print("Searching for source file %s" % file_name)
print("in %s" % tar_name)

if os.system("tar -xf %s %s" % (tar_name, file_name)) > 0 :
  print("No samples available for the system, try larger N")
  sys.exit(1)

imag_points = open("ImaginaryTimePoints.dat", "w+")
imag_points.write("ImaginaryTimePoints 1 %d\n" % int(n) )
imag_points.write("i \n")

imag_weights = open("ImaginaryTimeWeights.dat", "w+")
imag_weights.write("ImaginaryTimeWeights 1 %d\n" % int(n) )
imag_weights.write("i \n")

print("Extracting imaginary grid points tau_n and weights w_n")
for line in open(file_name).readlines():
  num = float(re.match(" *([^ ]+)", line).group(1)) / minDelta
  if re.match(".*alpha.*", line) :
    imag_points.write(str(num) + "\n")
  elif re.match(".*omega.*", line) :
    imag_weights.write(str(num) + "\n")

imag_points.close()
imag_weights.close()

chemical_potential = open("ChemicalPotential.dat", "w+")
chemical_potential.write("ChemicalPotential 0\n")
chemical_potential.write("  \n")
chemical_potential.write("%f\n" % mu)
chemical_potential.close()

if os.path.exists(file_name):
  os.system("rm -f %s" % file_name)

