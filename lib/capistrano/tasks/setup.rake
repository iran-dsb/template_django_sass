namespace :setup do

    desc "Atualizacao e instalacao de depedencias para o projeto"
    task :install_requirements_server do
      on roles(:app) do
        execute "echo '==================== Install dependencies ===================='"

        execute "sudo apt-get update -y"
        execute "sudo apt-get install build-essential -y"
        execute "sudo apt-get -y install python3 python3-pip python-dev python3-dev python-virtualenv postgresql postgresql-contrib libpq-dev nginx supervisor git ssh libjpeg-dev zlib1g-dev libpng12-dev curl"
        execute "sudo apt-get install supervisor -y"
        execute "sudo apt-get install nginx -y"
        execute "sudo apt-get -y install postgis postgresql-9.5-postgis-scripts"
        execute "sudo apt-get -y install binutils libproj-dev gdal-bin"
        execute "sudo locale-gen"
      end
    end


    task :create_folders do
      on roles(:app) do
        execute "cd /home/webapps/ && virtualenv -p python3 #{fetch(:deploy_to)} --no-site-package"
        execute "mkdir #{fetch(:deploy_to)}/shared/log/"
        execute "touch #{fetch(:deploy_to)}/shared/log/nginx-access.log"
        execute "touch #{fetch(:deploy_to)}/shared/log/nginx-error.log"
        execute "touch #{fetch(:deploy_to)}/shared/log/gunicorn_supervisor.log"
        execute "mkdir #{fetch(:deploy_to)}/static_collected"
        execute "mkdir #{fetch(:deploy_to)}/media/"
      end
    end

    desc "Install requirements"
    task :install_requirements do
      on roles(:app) do
        execute "source #{fetch(:deploy_to)}/bin/activate"
        execute "#{fetch(:deploy_to)}/bin/pip3 install -r #{fetch(:deploy_to)}/current/#{fetch(:application)}/requirements_production.txt"
      end
    end
    task :"migrations" do
      on roles(:app) do
        execute "source #{fetch(:deploy_to)}/bin/activate"
        execute "#{fetch(:deploy_to)}/bin/python3 #{fetch(:deploy_to)}/current/#{fetch(:application)}/manage.py migrate --settings=#{fetch(:application)}.#{fetch(:django_settings)}"
      end
    end
    task :"conf_files" do
      on roles(:app) do
        execute "sudo ln -s -f #{fetch(:deploy_to)}/current/#{fetch(:application)}/config/deploy_config/#{fetch(:application)}_nginx.conf /etc/nginx/sites-enabled/#{fetch(:application)}_nginx.conf"
        execute "sudo service nginx reload"
        execute "sudo ln -s -f #{fetch(:deploy_to)}/current/#{fetch(:application)}/config/deploy_config/#{fetch(:application)}_supervisor.conf /etc/supervisor/conf.d/#{fetch(:application)}_supervisor.conf"
        execute "sudo service supervisor restart"
      end
    end

    desc "Restart application"
    task :restart_app do
      on roles(:app) do
        execute "sudo supervisorctl reread && sudo supervisorctl update"
        execute "sudo supervisorctl restart all"
        execute "sudo service nginx reload"
      end
    end

    desc "Collectstatic"
    task :collect_static do
      on roles(:app) do
        execute "#{fetch(:deploy_to)}/bin/python3 #{fetch(:deploy_to)}/current/#{fetch(:application)}/manage.py collectstatic -v0 --noinput --settings=#{fetch(:application)}.#{fetch(:django_settings)}"
      end
    end

end