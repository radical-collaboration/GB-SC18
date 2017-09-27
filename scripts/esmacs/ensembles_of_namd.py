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

# Register the user-defined kernel with Ensemble MD Toolkit.
get_engine().add_kernel_plugin(UntarKernel)

# ------------------------------------------------------------------------------
# Set default verbosity

if os.environ.get('RADICAL_ENTK_VERBOSE') == None:
	os.environ['RADICAL_ENTK_VERBOSE'] = 'REPORT'


# ------------------------------------------------------------------------------
#
class RunNAMD(PoE):

	def __init__(self, stages, instances):
		PoE.__init__(self, stages, instances)

#	def stage_1(self, instance):
#		k = Kernel(name="untar")
#		k.arguments = ["--inputfile=apoa1.tgz"]
#		k.cores = 1
#		k.upload_input_data  = "/Users/stef/Development/Radical/apoa1.tgz > apoa1.tgz"

#		return k

	def stage_1(self, instance):

		k = Kernel(name="md.namd")
		k.arguments = ["%s.namd" % rootdir]
		k.copy_input_data = my_list_shared
		#k.link_input_data = my_list_shared		# You may choose to use link data if data is too large to copy
		k.cores = 4
		k.download_output_data = "STDOUT > %s-{0}.out".format(instance) % rootdir

		return k

# ------------------------------------------------------------------------------
#
if __name__ == "__main__":


	# use the resource specified as argument, fall back to localhost
	if   len(sys.argv) != 3:
		print 'Usage:\t%s [resource]\n\n' % sys.argv[0]
		sys.exit(1)
	else:
		resource = sys.argv[1] #resource to run on
		rootdir = sys.argv[2] #dir containing input files

		my_list = []
		my_list_shared = []

		for subdir, dirs, files in os.walk(rootdir):
			for file in files:
				print os.path.join(subdir, file)
				my_list.append(os.path.join(subdir, file))
				my_list_shared.append('$SHARED/%s'%os.path.basename(file))

	try:

		with open('%s/config.json'%os.path.dirname(os.path.abspath(__file__))) as data_file:
			config = json.load(data_file)

		# Create a new resource handle with one resource and a fixed
		# number of cores and runtime.
		cluster = ResourceHandle(
				resource=resource,
				cores=config[resource]["cores"],
				walltime=15,
				username=config[resource]['uzer'],

				project=config[resource]['project'],
				access_schema = config[resource]['schema'],
				queue = config[resource]['queue'],
			)

		cluster.shared_data = my_list

		# Allocate the resources.
		cluster.allocate()

		ccount = RunNAMD(stages=1,instances=4)


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
