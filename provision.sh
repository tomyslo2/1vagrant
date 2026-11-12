#!/bin/bash
set -e

apt update
DEBIAN_FRONTEND=noninteractive apt-get install -y nginx python3-flask

mkdir -p /opt/devops
cp /vagrant/app/app.py /opt/devops/app.py
cp /vagrant/app/devops.service /etc/systemd/system/devops.service
cp /vagrant/app/nginx.conf /etc/nginx/sites-available/default

systemctl daemon-reload
systemctl enable --now devops
systemctl restart devops

nginx -t
systemctl enable --now nginx
systemctl restart nginx
