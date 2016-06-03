require 'yaml'

ENV['VAGRANT_DEFAULT_PROVIDER'] = 'virtualbox'

project_dir = File.dirname(File.expand_path(__FILE__))

settings = YAML.load_file("#{project_dir}/conf/settings.yaml")
servers  = YAML.load_file("#{project_dir}/conf/servers.yaml")

Vagrant.configure(2) do |config|

  ##
  # General Settings
  #
  config.vm.synced_folder '.', '/vagrant'
  config.vm.synced_folder './cropcompass', '/home/vagrant/cropcompass'

  ##
  # Host Manager Plugin
  #  - Use vagrant-hostmanager to update your workstations hosts file with
  #    the hostname of your virtual machine.
  #
  if settings['enable_hostmanager']
    config.hostmanager.enabled         = true
    config.hostmanager.manage_host     = true
    config.hostmanager.include_offline = true
  end

  ##
  # Build Servers from YAML
  #
  servers.each do |server|

    config.vm.define server['name'] do |srv|

      ##
      # General Box Settings
      #
      srv.vm.hostname         = server['name'] + '.' + settings['domain']
      srv.vm.box              = server['box']
      srv.vm.box_check_update = settings['box_check_update']

      ##
      # Port Forwarding
      #  - These should be pushed into the box settings file.
      #
      srv.vm.network "forwarded_port", guest: 8000, host: 8000, auto_correct: true

      ##
      # Provider: Virtual Box
      #
      srv.vm.provider :virtualbox do |vb, override|
        vb.gui    = settings['vm_gui']
        vb.memory = server['memory']
      end

      ##
      # Ubuntu thinks all shells are login shells
      #
      srv.vm.provision "fix-no-tty", type: "shell" do |s|
        s.privileged = false
        s.inline = "sudo sed -i '/tty/!s/mesg n/tty -s \\&\\& mesg n/' /root/.profile"
      end

      ##
      # Shell Provisioning Scripts
      #  - See 'conf/boxes.yaml'
      #  - Scripts are in 'scripts/'
      #
      if server['provision_shell'].is_a?(Array)
        server['provision_shell'].each do |script|
          srv.vm.provision 'shell', path: script, privileged: false
        end
      end

      ##
      # Puppet Provisioning
      #  - This has been disabled in favor of invoking puppet via
      #    the shell provisioner.
      #  - The puppet provisioner in Vagrant does not follow Puppet 4
      #    conventions well enough to spend time on right now. 
      #  - Vagrant provisioners are processed "outside-in" order.
      #    This is the reason for the "if true" below. We want 
      #    The puppet provisioner running second.
      #
      #if true
      #  srv.vm.provision "puppetapply", type: "puppet" do |puppet|
      #    puppet.environment_path = "./puppet/code/environments"
      #    puppet.environment = "vagrant"
      #    puppet.options = "--confdir /vagrant/puppet"
      #  end
      #end

      ##
      # Box Up Message
      #
      if server['post_up_message'].is_a?(String)
        srv.vm.post_up_message = server['post_up_message']
      end

    end
  end

  ##
  # All Boxes Up Message
  #
  if settings['post_up_message'].is_a?(String)
    config.vm.post_up_message = settings['post_up_message']
  end
end
