#!/bin/bash

hostComputer=vm-hw01
python=/usr/bin/python3.11

echo 'Player name (atom): '

read playerName 

make client HOST=$hostComputer PYTHON3=$python CLIENT=$playerName