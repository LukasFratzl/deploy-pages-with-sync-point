#!/bin/bash
# Syncs Repos with git annex https://git-annex.branchable.com/

while :
do
  # Push
  if [ ! -z "$(git status --porcelain)" ]; then
      git add .
      git annex sync --content
  fi

  # Pull
  git fetch --all
  if [ "$(git rev-parse origin/main)" != "$(git rev-parse HEAD)" ]; then
    git annex sync --content
  fi

  sleep 1

done