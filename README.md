REMIX de:
-https://apexapps.oracle.com/pls/apex/r/dbpm/livelabs/view-workshop?wid=3279 
-https://followthecoffee.com/python-oracle-autonomous-database-connect-three-ways/
-https://www.youtube.com/watch?v=z3YMz-Gocmw
-https://github.com/alura-es-cursos/1911-OCI2-doguito-api-es/tree/master

COMANDOS

apt install python3.11-venv

	python3 -m venv .venv

	source .venv/bin/activate

	pip install flask

	pip install flask_restful

ORM (object relational mapping)

	pip install flask_sqlalchemy
	
	pip freeze > requirements.txt
	
	touch .gitignore
		-- agregar .venv
	
	pip install -r requirements.txt
	
		-- crear api.py
		
		pip install oracledb
		

FIREWALL PARA FLASK
	sudo firewall-cmd --add-port=8000/tcp --permanent
	sudo firewall-cmd --reload


QUE SE EJECUTE EN SEGUNDO PLANO

sudo nano clientes-api.service

sudo cp clientes-api.service /lib/systemd/system

sudo systemctl status clientes-api.service

sudo systemctl start clientes-api.service
