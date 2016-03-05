#
# NGINX
#
class { 'nginx':

}
nginx::resource::vhost { 'urbandev':
  www_root       => '/vagrant/doc',
  listen_port    => '80',
  listen_options => 'default_server',
  autoindex      => 'on',
}
