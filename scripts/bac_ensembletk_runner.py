#!/usr/bin/env python

import sys
import os
import json
import shutil

from radical.ensemblemd import Kernel
from radical.ensemblemd import PoE
from radical.ensemblemd import EnsemblemdError
from radical.ensemblemd import ResourceHandle

#Used to register user defined kernels
from radical.ensemblemd.engine import get_engine

#Import our new kernel
from untar import UntarKernel
from preprep import PreprepKernel

# Register the user-defined kernel with Ensemble MD Toolkit.
get_engine().add_kernel_plugin(UntarKernel)
get_engine().add_kernel_plugin(PreprepKernel)

# ------------------------------------------------------------------------------
# Set default verbosity

if os.environ.get('RADICAL_ENTK_VERBOSE') == None:
	os.environ['RADICAL_ENTK_VERBOSE'] = 'REPORT'


# ------------------------------------------------------------------------------
#
class RunNAMD(PoE):

	def __init__(self, stages, instances):
		PoE.__init__(self, stages, instances)

		#/move data
	def stage_1(self, instance):

		k = Kernel(name="untar")
		k.arguments = ["--inputfile=$SHARED/"+rootdir+".tgz"]
		k.cores = 1
		#k.copy_input_data  = "$SHARED/"+rootdir+".tgz > "+rootdir+".tgz"

		return k

	def stage_2(self, instance):
		k1 = Kernel(name="preprep")
		k1.link_input_data = []

		for f in my_list:
			k1.link_input_data.append("$STAGE_1/"+f+" > "+f)

		k1.arguments = ["--modeldir="+rootdir, "--replica=1"]
		k1.cores = 1

		return k1

	def stage_3(self, instance):
		k2 = Kernel(name="md.namd")
		#Need this to make the dir
		k2.link_input_data = ['$STAGE_2/{input1}/replicas/rep1/equilibration/holder > {input1}/replicas/rep1/equilibration/holder'.format(input1 = rootdir)]

		for f in my_list:
			k2.link_input_data.append("$STAGE_2/"+f+" > "+f)

		k2.arguments = ["%s/mineq_confs/eq0.conf" % rootdir]
		k2.cores = coresp

		return k2

	def stage_4(self, instance):
		k3 = Kernel(name="md.namd")
		k3.link_input_data = []

		my_list.append('{input1}/replicas/rep1/equilibration/eq0.coor'.format(input1 = rootdir))
		my_list.append('{input1}/replicas/rep1/equilibration/eq0.xsc'.format(input1 = rootdir))
		my_list.append('{input1}/replicas/rep1/equilibration/eq0.vel'.format(input1 = rootdir))

		for f in my_list:
			k3.link_input_data.append("$STAGE_3/"+f+" > "+f)

		k3.arguments = ["%s/mineq_confs/eq1.conf" % rootdir]
		k3.cores = coresp

		return k3

	def stage_5(self, instance):
		k4 = Kernel(name="md.namd")
		k4.link_input_data = []

		my_list.append('{input1}/replicas/rep1/equilibration/eq1.coor'.format(input1 = rootdir))
		my_list.append('{input1}/replicas/rep1/equilibration/eq1.xsc'.format(input1 = rootdir))
		my_list.append('{input1}/replicas/rep1/equilibration/eq1.vel'.format(input1 = rootdir))

		for f in my_list:
			k4.link_input_data.append("$STAGE_4/"+f+" > "+f)

		k4.arguments = ["%s/mineq_confs/eq2.conf" % rootdir]
		k4.cores = coresp

		return k4
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

	#Make the tar if it doesn't exist


	try:

		with open('%s/config.json'%os.path.dirname(os.path.abspath(__file__))) as data_file:
			config = json.load(data_file)

		# Create a new resource handle with one resource and a fixed
		# number of cores and runtime.
		cluster = ResourceHandle(
				resource=resource,
				cores=totalcores,
				walltime=15,
				username=config[resource]['user'],

				project=config[resource]['project'],
				access_schema = config[resource]['schema'],
				queue = config[resource]['queue'],
			)

		cluster.shared_data = ["./"+rootdir+".tgz"]

		# Allocate the resources.
		cluster.allocate()

		ccount = RunNAMD(stages=5,instances=replicas)

		cluster.run(ccount)

		# Print the checksums
		print "\nResulting simulation output:"
		import glob
		for result in glob.glob("*.out"):
			print "  * {0}".format(open(result, "r").readline().strip())

	except EnsemblemdError, er:

		print "Ensemble MD Toolkit Error: {0}".format(str(er))
		raise # Just raise the execption again to get the backtrace

	try:
		cluster.deallocate()
	except:
		pass
