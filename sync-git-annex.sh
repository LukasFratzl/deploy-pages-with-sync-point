#!/bin/bash
# Syncs Repos with git annex https://git-annex.branchable.com/

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

# Define sync function
sync() {
  cd "$SCRIPT_DIR"

  # Push
  if [ ! -z "$(git status --porcelain)" ]; then
      git add .
      git annex sync --content
  fi

  # Pull
  git annex pull
}

# Check if the user wants to run in loop mode
if [ "$1" = "-loop" ] && [ "$2" = "false" ]; then
  sync
else
  while :; do
    sync

    sleep 0.5
  done
fi