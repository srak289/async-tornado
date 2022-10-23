#!/bin/bash

for((i=0;i<10;i++))
do
    time curl localhost:8000 &
done
