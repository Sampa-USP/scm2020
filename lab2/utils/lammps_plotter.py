#!/usr/bin/env python3
"""
Receives a lammps log file (output) to plot two columns.

Author: Henrique Musseli Cezar
Date: APR/2020
"""

import argparse
import os
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
from distutils.spawn import find_executable

# from https://stackoverflow.com/a/11541495
def extant_file(x):
    """
    'Type' for argparse - checks that file exists but does not open.
    """
    if not os.path.exists(x):
        # Argparse uses the ArgumentTypeError to give a rejection message like:
        # error: argument input: x does not exist
        raise argparse.ArgumentTypeError("{0} does not exist".format(x))
    return x

def parse_log(file, colx, coly, multdt):
  # read data until EOF
  data = {}
  sim = 1
  with open(file,'r') as f:
    line = f.readline()
    while line:
      line = f.readline()

      if not line:
        break

      if "Time step" in line:
        dt = float(line.split(":")[1])
        continue

      if "Per MPI rank" not in line:
        continue

      # if headers were found, read them and the data
      headers = f.readline()
      try:
        headx = headers.split()[colx-1]
        heady = headers.split()[coly-1]
      except:
        # these header are not available
        print("Columns %d and %d are not valid for simulation %d" % (colx,coly,sim))
        sim += 1
        continue
      xaxis = []
      yaxis = []
      while True:
        line = f.readline()
        
        if "Loop" in line:
          break

        if not line:
          print("Simulation %d has not finished, check your output!" % sim)
          data[sim] = [(headx,heady),xaxis,yaxis]
          sim += 1
          break

        if multdt:
          xaxis.append(dt*float(line.split()[colx-1]))
        else:
          xaxis.append(float(line.split()[colx-1]))
        yaxis.append(float(line.split()[coly-1]))

      data[sim] = [(headx,heady),xaxis,yaxis]
      sim += 1

  return data

if __name__ == '__main__':
  parser = argparse.ArgumentParser(description="Receives a LAMMPS log to plot one column vs another.")
  parser.add_argument("logfile", type=extant_file, help="path to the LAMMPS output file")
  parser.add_argument("columnx", type=int, help="column of the x axis (starting from 1)")
  parser.add_argument("columny", type=int, help="column of the y axis (starting from 1)")
  parser.add_argument("--simulation", type=int, help="plot data of a single simulation only")
  parser.add_argument("--multx-timestep", action="store_true", help="multiply the x axis by the time step (to have time as the axis, for example)")
  parser.add_argument("--output-format", default="pdf", help="format of the output (default pdf)")


  args = parser.parse_args()

  data = parse_log(args.logfile, args.columnx, args.columny, args.multx_timestep)

  # plot it
  if find_executable('latex') and find_executable('dvipng'):
    mpl.rcParams.update({'font.size':18, 'text.usetex':True, 'font.family':'serif', 'ytick.major.pad':4})
  else:
    mpl.rcParams.update({'font.size':18, 'font.family':'serif', 'ytick.major.pad':4})

  if args.simulation:
    # print values to screen
    for i in range(len(data[args.simulation][1])):
      print("%f\t%f" % (data[args.simulation][1][i],data[args.simulation][2][i]))
    # plot
    plt.plot(data[args.simulation][1],data[args.simulation][2])
    plt.xlabel(data[args.simulation][0][0].replace("_","\_"))
    plt.ylabel(data[args.simulation][0][1].replace("_","\_"))
    plt.savefig("plotter_"+str(args.columnx)+"_"+str(args.columny)+"."+args.output_format, bbox_inches="tight")
  else:
    pass
  # plt.scatter(step,angles,s=2)

  # plt.xlabel(r"MC Cycle")
  # plt.ylabel(r"$\phi$ ($^\circ$)")
  # plt.xlim([0,step[-1]])
  # plt.ylim([-180,180])
  # plt.yticks([-180,-120,-60,0,60,120,180])
  # plt.savefig(os.path.splitext(args.fangles)[0]+".pdf", bbox_inches='tight')
