#!/bin/bash
set -e

apt update
DEBIAN_FRONTEND=noninteractive apt-get install -y nginx python3-flask postgresql python3-psycopg2 redis-server python3-redis apache2-utils

mkdir -p /opt/devops
cp /vagrant/app/app.py /opt/devops/app.py
cp /vagrant/app/devops.service /etc/systemd/system/devops.service
cp /vagrant/app/nginx.conf /etc/nginx/sites-available/default

htpasswd -ic /etc/nginx/.htpasswd devops < /vagrant/auth.password

systemctl enable --now postgresql
if ! runuser -u postgres -- psql -tAc "SELECT 1 FROM pg_roles WHERE rolname='www-data'" | grep -q 1; then
    runuser -u postgres -- createuser www-data
fi
if ! runuser -u postgres -- psql -tAc "SELECT 1 FROM pg_database WHERE datname='devops'" | grep -q 1; then
    runuser -u postgres -- createdb -O www-data devops
fi
runuser -u www-data -- psql -d devops -f /vagrant/app/db.sql

systemctl enable --now redis-server

systemctl daemon-reload
systemctl enable --now devops
systemctl restart devops

nginx -t
systemctl enable --now nginx
systemctl restart nginx
