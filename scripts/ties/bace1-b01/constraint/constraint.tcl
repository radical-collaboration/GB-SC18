mol load pdb /net/dirac/mnt/store6/dave/janssen/store/ties/bace1/com/drug/b01/b01/build/complex.pdb
set a [atomselect top all]

set outfile [open tmp_cbv w]
set minmax [measure minmax $a]
set boxsize [vecsub [lindex $minmax 1] [lindex $minmax 0]]
set centre [measure center $a]

puts $outfile $boxsize
puts $outfile $centre

close $outfile

$a set beta 0
$a set occupancy 0
set b [atomselect top "(resid 1 to 390) and noh"]
$b set beta 4
set z [atomselect top "(not (resid 1 to 390) and not water and not type IM) and noh"]
$z set beta 4

set c [atomselect top "resname B01 and name N4 C13 O2 C14 C15 N5 C16 C17 N6 O3 C18 C19 F2 F3 F4 H14 H15 H16 H17 H18"]
$c set occupancy -1
set d [atomselect top "resname B01 and name N10 C32 O5 C33 C34 C35 C36 CL1 C37 N11 H33 H34 H35 H36"]
$d set occupancy 1
$a writepdb /net/dirac/mnt/store6/dave/janssen/store/ties/bace1/com/drug/b01/b01/build/tags.pdb


$a writepdb /net/dirac/mnt/store6/dave/janssen/store/ties/bace1/com/drug/b01/b01/constraint/f4.pdb

quit
