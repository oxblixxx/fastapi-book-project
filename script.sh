#!/bin/bash
# Move Nginx configuration file
sudo cp /home/oxblixxx/fast-deploy/fastapi-book-project/fast-api /etc/nginx/sites-available/fast-api

  # Create a symbolic link
sudo ln -sf /etc/nginx/sites-available/fast-api /etc/nginx/sites-enabled/

##change permision