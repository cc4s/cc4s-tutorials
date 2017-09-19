#!/usr/bin/python
import sys
import os
import re

n = int(sys.argv[1]) if len(sys.argv) > 1 else 7
# turn into 2 digit number
n = "%02d" % n

holes = list(map(float,open("HoleEigenEnergies.dat").readlines()[2:]))
particles = list(map(float,open("ParticleEigenEnergies.dat").readlines()[2:]))
minDelta = 2*(particles[0]-holes[-1])
maxDelta = 2*(particles[-1]-holes[0])
R = maxDelta/minDelta
mu = (holes[-1]+particles[0])/2
print(mu)

print("min(eps_a-eps_i) = %f" % minDelta)
print("max(eps_a-eps_i) = %f" % maxDelta)
print("R = max/min = %f" % R)

# get base and exponent in scientif notation
R_scientific = "%1.0e" % R
R_exponent = int(R_scientific.split("e")[1])
# make sure FACTOR*10^EXPONENT is >= R
R += float("0.5e"+str(R_exponent))
R_scientific = "%1.0e" % R
R_factor = int(R_scientific.split("e")[0])
R_exponent = int(R_scientific.split("e")[1])

print (str(R_factor) + "e" + str(R_exponent))

# fetch suitable file
file_name = "1_xk%s.%d_%d" % (n,R_factor,R_exponent)
print (file_name)
tar_name = os.path.dirname(sys.argv[0]) + "/" + "1_x.tar.bz2"
print (tar_name)

if os.system("tar -xf %s %s" % (tar_name, file_name)) > 0 :
  print ("No samples available for the system, try larger N")
  sys.exit(1)

imag_points = open("ImaginaryTimePoints.dat", "w+")
imag_points.write("ImaginaryTimePoints 1 %d\n" % int(n) )
imag_points.write("i \n")

imag_weights = open("ImaginaryTimeWeights.dat", "w+")
imag_weights.write("ImaginaryTimeWeights 1 %d\n" % int(n) )
imag_weights.write("i \n")

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


if os.path.exists(file_name):
  os.system("rm -f %s" % file_name)

