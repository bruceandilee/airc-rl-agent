#!/bin/bash


echo "** Install requirement"
sudo apt update
sudo apt install -y liblapack-dev python3-scipy libfreetype6-dev python3-pandas
sudo pip3 install Cython gym git+https://github.com/tawnkramer/gym-donkeycar.git#egg=gym-donkeycar

echo "** Building..."
sudo pip3 install .\[jetpack]\

echo "** Install learning_racer successfully"
echo "** Bye :)"