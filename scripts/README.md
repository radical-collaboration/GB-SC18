Running HTBAC-ESMACS protocol using EnTK-0.6 (latest) on Blue Waters:

* Install [EnTK-0.6](https://github.com/radical-collaboration/RADICAL-UCL/wiki/RCT)
* git clone https://github.com/radical-collaboration/GB-SC18
* cd scripts
```
myproxy-logon -l <user> -s tfca.ncsa.illinois.edu
export RADICAL_PILOT_DBURL= 

export SAGA_PTY_SSH_TIMEOUT=2000
export RADICAL_PILOT_PROFILE=True
export RADICAL_ENMD_PROFILE=True
export RADICAL_ENMD_PROFILING=1
export RP_ENABLE_OLD_DEFINES=True
export PATH=/usr/sbin:$PATH
```

* setup [RabbitMQ instances via Docker](https://github.com/radical-collaboration/GB-SC18/blob/master/scripts/docker_setup.md) or install [RabbitMQ](https://www.rabbitmq.com/download.html)

```python bac_runner_entk_0-6_barrier.py```
