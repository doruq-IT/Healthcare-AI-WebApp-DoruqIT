from website import create_app
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = create_app()

if __name__ == '__main__':
	app.run()
