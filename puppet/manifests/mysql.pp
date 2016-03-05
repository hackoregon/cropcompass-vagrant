#
# MySQL Server
#
class { '::mysql::server': }

mysql::db { 'urbandev':
  user     => 'urbandev',
  password => 'vagrant',
  host     => 'localhost',
  grant    => ['ALL'],
}
