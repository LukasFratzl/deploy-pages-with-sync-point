# Syncs Repos with git annex https://git-annex.branchable.com/

# Sync
function sync {
    # Push
    if (git status --porcelain)
    {
        git add .
        git annex sync --content
    }

    # Pull
    git annex pull
}

# Define Arg -loop false|true
if ($args[1] -eq "false")
{
    sync
}
else
{
    while ($true)
    {
        sync
    }
}