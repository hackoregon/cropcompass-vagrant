#
# UrbanDev Frontend
#
vcsrepo { '/vagrant/code/urbandev-frontend':
  ensure   => present,
  provider => 'git',
  source   => 'https://github.com/hackoregon/urbandev-frontend.git',
}
