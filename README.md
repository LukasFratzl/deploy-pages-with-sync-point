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

