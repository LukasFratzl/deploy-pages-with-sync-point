# Deploy pages with a sync point

If the web server is inside the own network and there is a drive sync point from the developer PC and the server this is for you:

The Client script does:
- Create a zip archive from a folder ( With your html )
- Moved this archive to the sync point

On the Server script:
- It scans the sync point
- Extracts newly added archives
- Move it to `/var/www/something/` and set permissions

---

# API
Here the API below, please just use `sudo` if you have verified the paths and tested it ...
```shell
# Server ( sudo for setting permissions etc... )
python 'deploy_server.py' --sync_point ".../Server Sync Point"

# Client
python "deploy_client.py" --root "/Path/To/Html/Dev" --sync_point ".../Client Sync Point" --command "/Path/On/Server/To/deploy_server.sh"
```

- Root Arg: `-r <Path>`, `--root <Path>` (Required Client)
    - This is only for client, and it defines the path to the files which needs to send to the server, usually `.../Folder/With/Index.html/`etc..
- Sync-Point Arg: `-s <Path>`, `--sync_point <Path>` (Required Client | Server)
    - If you have a NAS the sync point would be the folder which is accessible from the Work PC and the Server at the same time
- Command Arg: `-c <Path>`, `--command <Path>`
    - The client can tell the server which script to execute, but only with some conditions:
      - The Script to execute needs to be stored on the server
      - Only a file can be executed, not a folder or command

# Usage
- Clone the Repo
- Set up the server script in a test scenario
  - `deploy_server.py` only needs the `--sync_point` arg
  - Make sure the `deploy_server.sh` is located on the server, optional make some tweaks to the file
  - Run the server file at startup if you happy with the result
- Set up the client script in a test scenario
  - `deploy_client.py` needs `--root` and `--sync_point` and optional `--command` arg
  - Make sure all paths are correct
  - Start the script without the server and it does create the archive in the sync point path
    - If the server is enabled it will do the needed job on the server
    - Repeat this client command if needed..

