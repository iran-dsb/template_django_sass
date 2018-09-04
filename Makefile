clean:
	rm -rf ./**/*.pyc

# usage: $ make version level=[major|minor|patch]
version:
	@npm version $(level)

run: clean
	python manage.py runserver 0.0.0.0:8000 --settings=template_sass.settings_local

migrate:
	python manage.py migrate --settings=template_sass.settings_local

migrations:
	python manage.py makemigrations --settings=template_sass.settings_local

user:
	python manage.py createsuperuser

shell:
	python manage.py shell --settings=template_sass.settings_local


initial_deploy:
	cap $(stage) setup:install_requirements_server
	cap $(stage) deploy
	cap $(stage) setup:create_folders
	cap $(stage) setup:install_requirements
	cap $(stage) setup:conf_files
	cap $(stage) setup:migrations
	cap $(stage) setup:collect_static
	cap $(stage) setup:restart_app

deploy:
	cap $(stage) deploy
	cap $(stage) setup:install_requirements
	cap $(stage) setup:migrations
	cap $(stage) setup:collect_static
	cap $(stage) setup:restart_app