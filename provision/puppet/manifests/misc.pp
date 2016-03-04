#
# Misc Packages
#

$packages = [
  'vim',
  'pgloader',
  'htop',
]

package { $packages:
  ensure => installed,
}
