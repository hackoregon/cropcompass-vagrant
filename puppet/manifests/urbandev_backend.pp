#
# UrbanDev Backend
#
vcsrepo { '/vagrant/src/urbandev-backend':
  ensure   => present,
  provider => 'git',
  source   => 'https://github.com/hackoregon/urbandev-backend.git',
}
