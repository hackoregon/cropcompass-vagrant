#
# UrbanDev Frontend
#
vcsrepo { '/vagrant/src/urbandev-frontend':
  ensure   => present,
  provider => 'git',
  source   => 'https://github.com/hackoregon/urbandev-frontend.git',
}
