#!/bin/bash
set -eu
h=$(git log -1 --pretty=%h)

set +e      # grep -c thinks no hits is an error.  Sigh.
numAdded=$(git status --porcelain | grep -c ^"A ")
numModified=$(git status --porcelain | grep -c ^" M")
numDeleted=$(git status --porcelain | grep -c ^"D ")
numUntracked=$(git status --porcelain | grep -c ^"??")
numTotal=$(($numAdded + $numDeleted + $numModified))
set -e

# _XX: Indicates that project code was modified at the time of run
# _X:  Indicates that project files were added or deleted at the time of run

if [ $numModified -gt 0 ]
then
  suffix="_XX"
elif [ $numTotal -gt 0 ]
then
  suffix="_X"
else
  suffix=""
fi

echo "${h}${suffix}"
