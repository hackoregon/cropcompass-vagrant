require 'yaml'

project_dir = File.dirname(File.expand_path(__FILE__))

settings = YAML.load_file("#{project_dir}/vagrant_conf/settings.yaml")
servers  = YAML.load_file("#{project_dir}/vagrant_conf/boxes.yaml")

Vagrant.configure(2) do |config|

  config.vm.provider 'virtualbox'

  config.vm.synced_folder '.', '/vagrant'

  config.hostmanager.enabled         = true
  config.hostmanager.manage_host     = true
  config.hostmanager.include_offline = true

  ############################################################################
  # Build Servers from YAML
  #
  servers.each do |server|

    config.vm.define server['name'] do |srv|

      srv.vm.hostname         = server['name'] + '.' + settings['domain']
      srv.vm.box              = server['box']
      srv.vm.box_check_update = settings['box_check_update']

      # VMware Desktop Provider
      srv.vm.provider :vmware_workstation do |v, override|
        v.gui    = true
        v.memory = server['memory']
      end

      # Virtual Box Provider
      srv.vm.provider :virtualbox do |vb, override|
        vb.gui    = settings['vm_gui']
        vb.memory = server['memory']
      end

      # Multiple shell provisioning scripts can be defined
      if server['provision_shell'].is_a?(Array)
        server['provision_shell'].each do |script|
          srv.vm.provision 'shell', path: script
        end
      end

      if server['post_up_message'].is_a?(String)
        srv.vm.post_up_message = server['post_up_message']
      end

    end
  end

  if settings['post_up_message'].is_a?(String)
    config.vm.post_up_message = settings['post_up_message']
  end
end
