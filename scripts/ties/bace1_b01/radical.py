from radical.entk import Pipeline, Stage, Task, AppManager, ResourceManager
import os
import traceback
# ------------------------------------------------------------------------------
# Set default verbosity

if os.environ.get('RADICAL_ENTK_VERBOSE') == None:
    os.environ['RADICAL_ENTK_VERBOSE'] = 'INFO'


class NamdTask(Task):
    def __init__(self, name, cores, mpi=True):
        super().__init__()
        t.name = name
        t.executable = ['/u/sciteam/jphillip/NAMD_build.latest/NAMD_2.12_CRAY-XE-MPI-BlueWaters/namd2']
        t.cores = cores
        t.mpi = mpi


if __name__ == '__main__':
    # Set up parameters
    cores_per_pipeline = 8
    rootdir = 'bace1_b01'
    pipelines = set()
    replicas = 5
    lambdas = [0.0, 0.05, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 0.95, 1.0]
    workflow = ['min', 'eq1', 'eq2', 'prod']


    # Generate pipelines
    for replica in range(replicas):
        for ld in lambdas:
            p = Pipeline()

            for step in workflow:
                s, t = Stage(), NamdTask(name=step, cores=cores_per_pipeline)
                t.arguments = ['replica_{}/lambda_{}/{}.conf'.format(replica, ld, task)]
                s.add_tasks(t)
                p.add_stage(s)

            pipelines.add(p)


    # Resource and AppManager

    res_dict = {
        'resource': 'ncsa.bw_aprun',
        'walltime': 1440,
        'cores': replicas * len(lambdas) * cores_per_pipeline,
        'project': 'bamm',
        'queue': 'high',
        'access_schema': 'gsissh'}

    # Create Resource Manager object with the above resource description
    rman = ResourceManager(res_dict)
    rman.shared_data = [rootdir + '.tgz']

    # Create Application Manager
    appman = AppManager(port=32775)

    # Assign resource manager to the Application Manager
    appman.resource_manager = rman

    # Assign the workflow as a set of Pipelines to the Application Manager
    appman.assign_workflow(pipelines)

    # Run the Application Manager
    appman.run()
