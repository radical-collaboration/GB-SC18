# Radical simulation workflow for the *TIES* protocol

BACE1 protein system

### Problems

- `rootdir` has to be copied over, but only once. If `rootdir` is tarred up, then you have to untar it at then other end. Where would you put that 1 untaring proccess? Having an untar `Stage` would run for all pipelines.
- Setting up a `Task` correctly. How to specify an output pipe for the namd2 executable, i.e. `namd2 min.conf >& min.log` is equivalent to:
```
t  = Task()
t.executable = ['/u/sciteam/jphillip/NAMD_build.latest/NAMD_2.12_CRAY-XE-MPI-BlueWaters/namd2']
t.arguments = ['min.conf', '>&', 'min.log']
```
?
