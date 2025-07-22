#!/bin/bash

# Instala Python3, pip, Flask y el cliente MySQL
sudo yum update -y
sudo yum install -y python3 git mysql
pip3 install flask pymysql

# Variables de entorno para la app y la inicialización de la DB
export DB_HOST="${db_host}"
export DB_USER="${db_user}"
export DB_PASS="${db_pass}"
export DB_NAME="${db_name}"

# Clona el repo de la app (ajusta la URL de tu repo)
git clone https://github.com/tu_usuario/tu_repo.git /home/ec2-user/app
cd /home/ec2-user/app

# Ejecuta el script de inicialización de la base de datos
mysql -h "$DB_HOST" -u "$DB_USER" -p"$DB_PASS" < /home/ec2-user/app/db/init.sql

# Inicia la app Flask
nohup python3 app.py &
