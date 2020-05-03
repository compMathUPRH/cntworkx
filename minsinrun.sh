export OMP_NUM_THREADS=${OMP_NUM_THREADS:-1}
echo "using $OMP_NUM_THREADS threads"

for i in $(find generated -maxdepth 2 -mindepth 2 -type d);do 
	cd $i
	echo $i
	mpirun lmp -in lammps.in #minimizar
	python3 ../../../replacer.py "tube.data" 
	#reemplazar los atomos del ultimo frame
	mpirun lmp -in lammps2.in #simular
	cd ../../..
done

