# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure("2") do |config|
    config.vm.box = "trusty-server-cloudimg-amd64-vagrant-disk1"
    config.vm.box_url = "https://cloud-images.ubuntu.com/vagrant/trusty/current/trusty-server-cloudimg-amd64-vagrant-disk1.box"

    config.vm.provider "virtualbox" do |custom_virtualbox_settings|
      custom_virtualbox_settings.name = "boutique"
    end

    config.vm.network :forwarded_port, guest: 80, host: 8080
    config.vm.network :forwarded_port, guest: 8000, host: 8000

    config.vm.synced_folder "./", "/home/vagrant/boutique"
    config.vm.provision :shell, :path => "vagrant/provisioning.sh"
end
