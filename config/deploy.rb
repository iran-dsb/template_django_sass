# config valid only for current version of Capistrano
lock '3.4.1'

set :application, 'template_sass'
set :repo_url, ''

#set :repository,  "."

set :user, "root"
set :use_sudo, true

set :deploy_to, "/home/webapps/template_sass"
#set :deploy_via, :copy

set :copy_dir, "/tmp"
set :copy_remote_dir, "/tmp"

set :copy_exclude, [".git", ".gitignore", "*.pyc", "**/.git", "**/*.log", "**/.pyc", ".swp", ".swp", "Gemfile", "tmp/", '**/.gitignore', 'Capfile', 'REVISION', 'Vagrant', 'Gemfile.lock', '**/Vagrant', '**/Capfile', '**/REVISION']


namespace :deploy do

    after :restart, :clear_cache do
        on roles(:web), in: :groups, limit: 3, wait: 10 do
          # Here we can do anything such as:
          within release_path do
            #execute :rake, 'setup:atualizacao_projeto'
          end
        end
    end

end
