#!/bin/bash
# Move Nginx configuration file
sudo /bin/bash -c cp /home/oxblixxx/fast-deploy/fastapi-book-project/fast-api /etc/nginx/sites-available/fast-api
  # Create a symbolic link
sudo /bin/bash -c ln -sf /etc/nginx/sites-available/fast-api /etc/nginx/sites-enabled/
##change permision
#add binbanf