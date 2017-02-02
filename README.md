# GB-SC18

This a collaborative project that will study XXXX using ensemble-based methods at unprecedented scales. In order to do so, we are developing the High-Throughput Binding Affinity Calculator (HT-BAC) which is the integration of the BAC -- Binding Affinity Calculator  developed by the CCS at UCL, and RADICAL-Cybertools (RADICAL Laboratory). BAC represents the state-of-the-art in defining biomedically important workflows for binding affinity calculations. RADICAL-Cybertools are a suite of functional componenents that support the interoperable and scalable execution of multiple simulations. 

HT-BAC provides the ability to separate the "setting-up" (i.e., definining) a worklfow from the "execution" of the workflow. The two components (BAC and Ensemble-Toolkit) separate the two concerns.  HT-BAC will use well defined Ensemble-Toolkit APIs to support multiple distinct workflows of increasing sophistication. Starting with "bag -of-tasks" it will support adaptive sampling. The runtime system of RADICAL-Cybertools (which is known as RADICAL-Pilot) is being engineered to support up to $10^5$ ensemble members.

