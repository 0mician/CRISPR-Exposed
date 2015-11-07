#!/bin/bash

echo 'provisioning.. '

# installing ansible
sudo apt-add-repository ppa:ansible/ansible
sudo apt-get update
sudo apt-get -y install ansible

# configure ansible
sudo sed -i "s/\#ask_pass = True/ask_pass = True/" /etc/ansible/ansible.cfg
# okaying root auth by password for ssh
sudo sed -i "s/without-password/yes/" /etc/ssh/sshd_config
sudo service ssh restart

# configure ansible hosts
sudo cp /vagrant/hosts /etc/ansible/

echo '.. done!'
