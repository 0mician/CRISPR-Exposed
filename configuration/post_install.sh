#!/bin/bash

echo 'provisioning.. '

# installing ansible
sudo apt-add-repository -y ppa:ansible/ansible
sudo apt-get update
sudo apt-get -y install ansible

# configure ansible
sudo sed -i "s/\#ask_pass      = True/ask_pass = True/" /etc/ansible/ansible.cfg
# okaying root auth by password for ssh
sudo sed -i "s/without-password/yes/" /etc/ssh/sshd_config
sudo service ssh restart

# configure ansible hosts
echo '[crispr-exposed]' | sudo tee /etc/ansible/hosts
echo 'localhost' | sudo tee --append /etc/ansible/hosts

echo '.. done!'
