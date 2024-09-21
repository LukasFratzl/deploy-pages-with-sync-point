#!/bin/bash

# Server
# sudo python 'deploy_server.py' -s ".../Server Sync Point"

# Client
# python "deploy_client.py" --root "/Path/To/Html/Dev" --sync_point ".../Client Sync Point" --command "/Path/On/Server/To/deploy_server.sh"

echo "Starting Deploy from server script"

# deploy_client_temp_file_dir is like always the extracted dir name
# the folder is relative one level deeper on the sync point folder on the server
# and in this case I treat it as a temp folder anyway....
deploy_archive_folder="/home/flow____/Desktop/server-sync-point/deploy_client_temp_file_dir"

# the wanted folder ...
deploy_wanted_folder="/var/www/lukas.read-books.org/public_html/blog"

if [ -d "$deploy_wanted_folder" ]; then
  sudo rm -r "$deploy_wanted_folder"
fi

sudo mv "$deploy_archive_folder" "$deploy_wanted_folder"

sudo chown -R www-data:www-data "$deploy_wanted_folder"

