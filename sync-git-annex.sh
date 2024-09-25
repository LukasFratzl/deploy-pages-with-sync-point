#!/bin/bash
# Syncs Repos with git annex https://git-annex.branchable.com/

while :
do
  SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

  cd "$SCRIPT_DIR"

  # Push
  if [ ! -z "$(git status --porcelain)" ]; then
      git add .
      git annex sync --content
  fi

  # Pull
  git annex pull
  sleep 0.5

done
