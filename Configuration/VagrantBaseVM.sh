#!/bin/bash

echo 'provisioning.. '

# installing vagrant
sudo apt-add-repository ppa:ansible/ansible
sudo apt-get update
sudo apt-get -y install ansible

# configure vagrant
sudo sed -i "s/\#ask_sudo_pass = True/ask_sudo_pass = True/" /etc/ansible/ansible.cfg

# configure vagrant host
sudo mv /vagrant/hosts /etc/ansible/

echo '.. done!'
