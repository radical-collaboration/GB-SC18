#!/usr/bin/env python

import sys
import os
import json
import shutil

from radical.ensemblemd import Kernel
#from radical.ensemblemd import PoE
from radical.ensemblemd import EoP
from radical.ensemblemd import EnsemblemdError
from radical.ensemblemd import ResourceHandle

#Used to register user defined kernels
from radical.ensemblemd.engine import get_engine

#Import our new kernel
from untar import UntarKernel
from preprep import PreprepKernel
from tar import TarKernel

# Register the user-defined kernel with Ensemble MD Toolkit.
get_engine().add_kernel_plugin(UntarKernel)
get_engine().add_kernel_plugin(TarKernel)
get_engine().add_kernel_plugin(PreprepKernel)

# ------------------------------------------------------------------------------
# Set default verbosity

if os.environ.get('RADICAL_ENTK_VERBOSE') == None:
	os.environ['RADICAL_ENTK_VERBOSE'] = 'REPORT'


# ------------------------------------------------------------------------------
#
class RunNAMD(EoP):

	def __init__(self, stages, instances):
		EoP.__init__(self, stages, instances)

		#/move data
	def stage_1(self, instance):

		k = Kernel(name="misc.idle")
		k.arguments = [0]
		k.cores = coresp

		return k

	def stage_2(self, instance):
		k1 = Kernel(name="misc.idle")
		k1.arguments = [0]
		k1.cores = coresp

		return k1

	def stage_3(self, instance):
		k2 = Kernel(name="misc.idle")
		k2.arguments = [0]
		k2.cores = coresp

		return k2

	def stage_4(self, instance):
		k3 = Kernel(name="misc.idle")
		k3.arguments = [0]
		k3.cores = coresp

		return k3

	def stage_5(self, instance):
		k4 = Kernel(name="misc.idle")
		k4.arguments = [0]
		k4.cores = coresp

		return k4

		#sim steps
	def stage_6(self, instance):
		k5 = Kernel(name="misc.idle")
		k5.arguments = [0]
		k5.cores = coresp

		return k5

	def stage_7(self, instance):
		k6 = Kernel(name="misc.idle")
		k6.arguments = [0]
		k6.cores = coresp

		return k6
# ------------------------------------------------------------------------------
#
if __name__ == "__main__":


	# use the resource specified as argument, fall back to localhost
	if   len(sys.argv) != 5:
		print 'Usage:\t%s [resource] [modeldir] [replicas] [cores per rep]\n\n' % sys.argv[0]
		sys.exit(1)
	else:
		resource = sys.argv[1] #resource to run on
		rootdir = sys.argv[2] #dir containing input files
		replicas = int(sys.argv[3])
		coresp = int(sys.argv[4])

		totalcores = replicas * coresp

		print("Running {reps} replicas on {crs} cores".format(reps=replicas, crs=totalcores))

		my_list = []

		for subdir, dirs, files in os.walk(rootdir):
			for file in files:
				#print os.path.join(subdir, file)
				my_list.append(os.path.join(subdir, file))

	#TODO: Make the tar if it doesn't exist


	try:

		fjson = '%s/config.json' % os.path.dirname(os.path.abspath(__file__))
		with open(fjson) as data_file:
			config = json.load(data_file)

		# Create a new resource handle with one resource and a fixed
		# number of cores and runtime.
		
		cluster = ResourceHandle(
				resource=resource,
				cores=totalcores,
				walltime=720,
				#username=config[resource]['user'],

				project=config[resource]['project'],
				access_schema = config[resource]['schema'],
				queue = config[resource]['queue'],
			)

		cluster.shared_data = ["./"+rootdir+".tgz"]

		# Allocate the resources.
		cluster.allocate()

		ccount = RunNAMD(stages=7,instances=replicas)

		cluster.run(ccount)

		# Print the checksums
		print "\nResulting simulation output:"
		import glob
		for result in glob.glob("rep*.tgz"):
			print result

	except EnsemblemdError, er:

		print "Ensemble MD Toolkit Error: {0}".format(str(er))
		raise # Just raise the execption again to get the backtrace

	try:
		cluster.deallocate()
	except:
		pass
