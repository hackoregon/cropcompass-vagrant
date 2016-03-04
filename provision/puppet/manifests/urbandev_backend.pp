#
# UrbanDev Backend
#
vcsrepo { '/vagrant/code/urbandev-backend':
  ensure   => present,
  provider => 'git',
  source   => 'https://github.com/hackoregon/urbandev-backend.git',
}
