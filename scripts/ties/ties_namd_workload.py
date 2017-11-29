from radical.entk import Pipeline, Stage, Task, AppManager, ResourceManager
import os
import traceback
# ------------------------------------------------------------------------------
# Set default verbosity

if os.environ.get('RADICAL_ENTK_VERBOSE') == None:
    os.environ['RADICAL_ENTK_VERBOSE'] = 'INFO'


class NamdTask(Task):
    def __init__(self, name, cores, mpi=True):
        super(NamdTask, self).__init__()
        self.name = name
        self.executable = ['/u/sciteam/jphillip/NAMD_build.latest/NAMD_2.12_CRAY-XE-MPI-BlueWaters/namd2']
        self.cores = cores
        self.mpi = mpi


if __name__ == '__main__':
    # Set up parameters

    rootdir = 'bace1_b01'
    my_list = []
        
    for subdir, dirs, files in os.walk(rootdir):
        for file in files:
            #print os.path.join(subdir, file)
            my_list.append(os.path.join(subdir, file))

    print my_list
    cores_per_pipeline = 32
    pipelines = set()
    stage_ref = []
    replicas = 1
    lambdas = [0.0]
    #lambdas  = [0.0, 0.05, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 0.95, 1.0]
    workflow = ['min', 'eq1', 'eq2', 'prod']


    # Generate pipelines

    for replica in range(replicas):
        for ld in lambdas:
            p = Pipeline()
           
            for step in workflow:
                task_ref = []
                s, t = Stage(), NamdTask(name=step, cores=cores_per_pipeline)
                t.arguments = ['replica_{}/lambda_{}/{}.conf'.format(replica, ld, step), '&>', 'replica_{}/lambda_{}/{}.log'.format(replica, ld, step)]
                task_ref.append("$Pipeline_{0}_Stage_{1}_Task_{2}/".format(p.uid, s.uid, t.uid))
                #print task_ref
                s.add_tasks(t)
                p.add_stages(s)

                for task_paths in stage_ref:
                    for task_path in task_paths: 
                        #print task_path 
                        #print workflow[stage_ref.index(task_paths)]
                        t.copy_input_data.append(task_path+'/replica_{}/lambda_{}/{}.coor'.format(replica,ld,workflow[stage_ref.index(task_paths)]))
                        t.copy_input_data.append(task_path+'/replica_{}/lambda_{}/{}.xsc'.format(replica,ld,workflow[stage_ref.index(task_paths)]))
                        t.copy_input_data.append(task_path+'/replica_{}/lambda_{}/{}.vel'.format(replica,ld,workflow[stage_ref.index(task_paths)]))
                
                for f in my_list:
                    t.copy_input_data.append("{}/".format(replica)+f+" > "+f)
            

            	stage_ref.append(task_ref)
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

    # FIXME this is not going to work. `rootdir` has to be copied over, but
    # only once. If `rootdir` is tarred up, then you have to untar it at then
    # other end. Where would you put that 1 untaring proccess?
    rman.shared_data = [rootdir]

    # Create Application Manager
    appman = AppManager(port=32775)

    # Assign resource manager to the Application Manager
    appman.resource_manager = rman

    # Assign the workflow as a set of Pipelines to the Application Manager
    appman.assign_workflow(pipelines)

    # Run the Application Manager
    #appman.run()
