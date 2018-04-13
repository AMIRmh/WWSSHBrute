#!/bin/bash

num_threads=10
python3 findIP.py germany
python3 findSSH.py $num_threads germany
python3 brute.py $num_threads
