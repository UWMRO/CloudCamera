# /usr/bin/bash

echo "installing openssag via git"
git submodule update --init --recursive

echo "building image taking program"
cmake -S ./ImageTaker/ -B ./ImageTaker/build/ 
make -C ./ImageTaker/build/

echo "build complete"
