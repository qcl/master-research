mkdir -p dataset;
cd dataset;
echo "Build ./dataset, cd into...";
echo "Start download PATTY";
wget http://www.mpi-inf.mpg.de/yago-naga/patty/data/README.txt;
wget http://www.mpi-inf.mpg.de/yago-naga/patty/data/patty-dataset.tar.gz;
wget http://www.mpi-inf.mpg.de/yago-naga/patty/data/patty-dataset-freebase.tar.gz;
wget http://www.mpi-inf.mpg.de/yago-naga/patty/data/patty-eval.tar.gz;
echo "Done."
