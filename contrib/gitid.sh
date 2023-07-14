#!/bin/bash
h=$(git log -1 --pretty=%h)

numAdded=$(git status --porcelain | grep -c ^"A ")
numModified=$(git status --porcelain | grep -c ^" M")
numDeleted=$(git status --porcelain | grep -c ^"D ")
numUntracked=$(git status --porcelain | grep -c ^"??")
numTotal=$(($numAdded + $numDeleted + $numModified))

if [ $numTotal -gt 0 ]
then
suffix="_X"
else
suffix=""
fi

echo "${h}${suffix}"
