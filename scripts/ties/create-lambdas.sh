#! /bin/bash

for lw in 0.00 0.05 0.10 0.20 0.30 0.40 0.50 0.60 0.70 0.80 0.90 0.95 1.00
do 
    dirname="LAMBDA_${lw}"
    mkdir $dirname
    cp -r mineq_confs/ $dirname
    cp -r sim_confs/ $dirname
    cp -r replicas/ $dirname
    cp -r build/ $dirname
    cp -r constraint/ $dirname
    cp fep.tcl $dirname

    cd $dirname/mineq_confs

    sed -i "s/LAMBDA/${lw}/" *.conf

    for repno in `seq 1 5`
    do
        sed "s/REPX/${repno}/" eq0.conf >eq0-rep${repno}.conf
        sed "s/REPX/${repno}/" eq1.conf >eq1-rep${repno}.conf
        sed "s/REPX/${repno}/" eq2.conf >eq2-rep${repno}.conf
    done

    cd ../sim_confs
    sed -i "s/LAMBDA/${lw}/" *.conf
    
    for repno in `seq 1 5`
    do
        sed "s/REPX/${repno}/" sim1.conf >sim1-rep${repno}.conf
    done

    cd ../../

done
