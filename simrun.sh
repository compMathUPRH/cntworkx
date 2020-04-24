export OMP_NUM_THREADS=${OMP_NUM_THREADS:-1}
echo "using $OMP_NUM_THREADS threads"

for i in $(find generated -maxdepth 2 -mindepth 2 -type d);do 
	cd $i
	mpirun lmp -in lammps.in #usa todos los cores por defecto (no threads)
	cd ../../..
	
done









