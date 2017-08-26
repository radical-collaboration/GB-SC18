from radical.entk import Pipeline, Stage, Task, AppManager, ResourceManager
import os

# ------------------------------------------------------------------------------
# Set default verbosity

if os.environ.get('RADICAL_ENTK_VERBOSE') == None:
    os.environ['RADICAL_ENTK_VERBOSE'] = 'INFO'


# def generate_state():

#     s = Stage()

#     t = Task()
#     t.executable = ['/bin/sleep']
#     t.arguments = ['0']
#     t.cores = 8
#     s.add_tasks(t)

#     return s

def stage_1():

	t.name = 'untar'
	t.executable = ['untar']
	t.arguments = ["--inputfile="+rootdir+".tgz"]
	t.cores = 1
	t.copy_input_data  = "$SHARED/"+rootdir+".tgz > "+rootdir+".tgz"
	s.add_task(t)
	
	return s

def stage_2():
	
	t1.name = 'preprep'
	t1.executable = ['preprep']
	t1.link_input_data = []

	for f in my_list:
		t1.link_input_data.append("$STAGE_1/"+f+" > "+f)

	t1.arguments = ["--modeldir="+rootdir, "--replica=%d" % instance]
	t1.cores = 1
	s1.add_tasks(t1)

	return s1

def stage_3():
	
	t2.name = 'stage3_namd'
	t2.executable = ['/u/sciteam/jphillip/NAMD_build.latest/NAMD_2.12_CRAY-XE-MPI-BlueWaters/namd2']
	#Need this to make the dir
	t2.link_input_data = ['$STAGE_2/{input1}/replicas/rep{input2}/equilibration/holder > {input1}/replicas/rep{input2}/equilibration/holder'.format(input1 = rootdir, input2=instance)]

	for f in my_list:
		t2.link_input_data.append("$STAGE_2/"+f+" > "+f)

	t2.arguments = ["%s/mineq_confs/eq0.conf" % rootdir]
	t2.cores = coresp
	s2.add_tasks(t2)
	
	return s2

def stage_4():

	t3.name = 'stage4_namd'
	t3.executable = ['/u/sciteam/jphillip/NAMD_build.latest/NAMD_2.12_CRAY-XE-MPI-BlueWaters/namd2']
	t3.link_input_data = ['$STAGE_3/{input1}/replicas/rep{input2}/equilibration/eq0.coor > {input1}/replicas/rep{input2}/equilibration/eq0.coor'.format(input1 = rootdir, input2 = instance), '$STAGE_3/{input1}/replicas/rep{input2}/equilibration/eq0.xsc > {input1}/replicas/rep{input2}/equilibration/eq0.xsc'.format(input1 = rootdir, input2 = instance), '$STAGE_3/{input1}/replicas/rep{input2}/equilibration/eq0.vel > {input1}/replicas/rep{input2}/equilibration/eq0.vel'.format(input1 = rootdir, input2 = instance)]

	for f in my_list:
		t3.link_input_data.append("$STAGE_3/"+f+" > "+f)

	t3.arguments = ["%s/mineq_confs/eq1.conf" % rootdir]
	t3.cores = coresp
	s3.add_tasks(t3)
	
	return s3

def stage_5():

	t4.name = 'stage5_namd'
	t4.executable = ['/u/sciteam/jphillip/NAMD_build.latest/NAMD_2.12_CRAY-XE-MPI-BlueWaters/namd2']
	t4.link_input_data = ['$STAGE_4/{input1}/replicas/rep{input2}/equilibration/eq0.coor > {input1}/replicas/rep{input2}/equilibration/eq0.coor'.format(input1 = rootdir, input2 = instance), '$STAGE_4/{input1}/replicas/rep{input2}/equilibration/eq0.xsc > {input1}/replicas/rep{input2}/equilibration/eq0.xsc'.format(input1 = rootdir, input2 = instance), '$STAGE_4/{input1}/replicas/rep{input2}/equilibration/eq0.vel > {input1}/replicas/rep{input2}/equilibration/eq0.vel'.format(input1 = rootdir, input2 = instance),
	'$STAGE_4/{input1}/replicas/rep{input2}/equilibration/eq1.xsc > {input1}/replicas/rep{input2}/equilibration/eq1.xsc'.format(input1 = rootdir, input2 = instance),
	'$STAGE_4/{input1}/replicas/rep{input2}/equilibration/eq1.vel > {input1}/replicas/rep{input2}/equilibration/eq1.vel'.format(input1 = rootdir, input2 = instance),
	'$STAGE_4/{input1}/replicas/rep{input2}/equilibration/eq1.coor > {input1}/replicas/rep{input2}/equilibration/eq1.coor'.format(input1 = rootdir, input2 = instance)]

	for f in my_list:
		t4.link_input_data.append("$STAGE_4/"+f+" > "+f)

	t4.arguments = ["%s/mineq_confs/eq2.conf" % rootdir]
	t4.cores = coresp
	s4.add_stages(t4)

	return s4

def stage_6():


	t5.name = 'stage6_namd'
	t5.executable = ['/u/sciteam/jphillip/NAMD_build.latest/NAMD_2.12_CRAY-XE-MPI-BlueWaters/namd2']
	t5.link_input_data = ['$STAGE_2/{input1}/replicas/rep{input2}/simulation/holder > {input1}/replicas/rep{input2}/simulation/holder'.format(input1 = rootdir, input2=instance), '$STAGE_5/{input1}/replicas/rep{input2}/equilibration/eq0.coor > {input1}/replicas/rep{input2}/equilibration/eq0.coor'.format(input1 = rootdir, input2 = instance), '$STAGE_5/{input1}/replicas/rep{input2}/equilibration/eq0.xsc > {input1}/replicas/rep{input2}/equilibration/eq0.xsc'.format(input1 = rootdir, input2 = instance), '$STAGE_5/{input1}/replicas/rep{input2}/equilibration/eq0.vel > {input1}/replicas/rep{input2}/equilibration/eq0.vel'.format(input1 = rootdir, input2 = instance),
	'$STAGE_5/{input1}/replicas/rep{input2}/equilibration/eq1.xsc > {input1}/replicas/rep{input2}/equilibration/eq1.xsc'.format(input1 = rootdir, input2 = instance),
	'$STAGE_5/{input1}/replicas/rep{input2}/equilibration/eq1.vel > {input1}/replicas/rep{input2}/equilibration/eq1.vel'.format(input1 = rootdir, input2 = instance),
	'$STAGE_5/{input1}/replicas/rep{input2}/equilibration/eq1.coor > {input1}/replicas/rep{input2}/equilibration/eq1.coor'.format(input1 = rootdir, input2 = instance),
	'$STAGE_5/{input1}/replicas/rep{input2}/equilibration/eq2.xsc > {input1}/replicas/rep{input2}/equilibration/eq2.xsc'.format(input1 = rootdir, input2 = instance),
	'$STAGE_5/{input1}/replicas/rep{input2}/equilibration/eq2.vel > {input1}/replicas/rep{input2}/equilibration/eq2.vel'.format(input1 = rootdir, input2 = instance),
	'$STAGE_5/{input1}/replicas/rep{input2}/equilibration/eq2.coor > {input1}/replicas/rep{input2}/equilibration/eq2.coor'.format(input1 = rootdir, input2 = instance)]

	for f in my_list:
		t5.link_input_data.append("$STAGE_5/"+f+" > "+f)

	t5.arguments = ["%s/sim_confs/sim1.conf" % rootdir]
	t5.cores = coresp
	s5.add_task(t5)

	return s5

def stage_7():

	t6.name = 'stage7_tar'
	t6.executable = 'tar'
	t6.arguments = ["--directory="+rootdir, "--tarname=rep%d" % instance]
	t6.cores = 1
	t6.link_input_data = ['$STAGE_6/{input1}/replicas/rep{input2}/equilibration/eq0.coor > {input1}/replicas/rep{input2}/equilibration/eq0.coor'.format(input1 = rootdir, input2 = instance), '$STAGE_6/{input1}/replicas/rep{input2}/equilibration/eq0.xsc > {input1}/replicas/rep{input2}/equilibration/eq0.xsc'.format(input1 = rootdir, input2 = instance), '$STAGE_6/{input1}/replicas/rep{input2}/equilibration/eq0.vel > {input1}/replicas/rep{input2}/equilibration/eq0.vel'.format(input1 = rootdir, input2 = instance),
	'$STAGE_6/{input1}/replicas/rep{input2}/equilibration/eq1.xsc > {input1}/replicas/rep{input2}/equilibration/eq1.xsc'.format(input1 = rootdir, input2 = instance),
	'$STAGE_6/{input1}/replicas/rep{input2}/equilibration/eq1.vel > {input1}/replicas/rep{input2}/equilibration/eq1.vel'.format(input1 = rootdir, input2 = instance),
	'$STAGE_6/{input1}/replicas/rep{input2}/equilibration/eq1.coor > {input1}/replicas/rep{input2}/equilibration/eq1.coor'.format(input1 = rootdir, input2 = instance),
	'$STAGE_6/{input1}/replicas/rep{input2}/equilibration/eq2.xsc > {input1}/replicas/rep{input2}/equilibration/eq1.xsc'.format(input1 = rootdir, input2 = instance),
	'$STAGE_6/{input1}/replicas/rep{input2}/equilibration/eq2.vel > {input1}/replicas/rep{input2}/equilibration/eq1.vel'.format(input1 = rootdir, input2 = instance),
	'$STAGE_6/{input1}/replicas/rep{input2}/equilibration/eq2.coor > {input1}/replicas/rep{input2}/equilibration/eq1.coor'.format(input1 = rootdir, input2 = instance),
	'$STAGE_6/{input1}/replicas/rep{input2}/simulation/sim1.xsc > {input1}/replicas/rep{input2}/simulation/sim1.xsc'.format(input1 = rootdir, input2 = instance),
	'$STAGE_6/{input1}/replicas/rep{input2}/simulation/sim1.vel > {input1}/replicas/rep{input2}/simulation/sim1.vel'.format(input1 = rootdir, input2 = instance),
	'$STAGE_6/{input1}/replicas/rep{input2}/simulation/sim1.coor > {input1}/replicas/rep{input2}/simulation/sim1.coor'.format(input1 = rootdir, input2 = instance)]

	t6.download_output_data = "rep{0}.tgz".format(instance)
	s6.add_task(t6)

	return s6

def generate_pipeline():

    # Create a Pipeline object
    p = Pipeline()
      
    p.add_stages(stage_1())
    p.add_stages(stage_2())
    p.add_stages(stage_3())
    p.add_stages(stage_4())
    p.add_stages(stage_5())
    p.add_stages(stage_6())
    p.add_stages(stage_7())
        
        

    return p


if __name__ == '__main__':

    pipelines = []

    num_pipelines=8
    
    for cnt in range(num_pipelines):
        pipelines.append(generate_pipeline())


    # Create a dictionary describe four mandatory keys:
    # resource, walltime, cores and project
    # resource is 'local.localhost' to execute locally
    res_dict = {

            'resource': 'ncsa.bw_aprun',
            'walltime': 720,
            'cores': num_pipelines * 8,
            'project': 'bamm',
            'queue': 'normal',
            'access_schema': 'gsissh'
    }

    # Create Resource Manager object with the above resource description
    rman = ResourceManager(res_dict)

    # Create Application Manager
    appman = AppManager()

    # Assign resource manager to the Application Manager
    appman.resource_manager = rman

    # Assign the workflow as a set of Pipelines to the Application Manager
    appman.assign_workflow(set(pipelines))

    # Run the Application Manager
    appman.run()