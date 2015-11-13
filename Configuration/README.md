# Introduction

The basic idea is to try and document the environment so that people
can reproduce it. Our basic construct is an Ubuntu Server 14.04 LTS
(vanilla install).

Once the server is up and running, the only software you need for the
proceeding steps of configuration is Ansible.

Ansible configuration files can be read and understood easily by
sysadmins, so if you can't/won't use Ansible, feel free to go through
the files as they document the environment in which CRISPR-Exposed
runs.

# Ansible

You can install Ansible through the [ansible PPA](https://launchpad.net/~ansible/+archive/ubuntu/ansible)

```bash
$ sudo apt-add-repository -y ppa:ansible/ansible
$ sudo apt-get update
$ sudo apt-get -y install ansible
```

Configure the target host (here, we work locally, on our server):

```bash
$ echo "[crispr-exposed]" | sudo tee /etc/ansible/hosts
$ echo "localhost" | sudo tee --append /etc/ansible/hosts
```

Edit the file located at: /etc/ssh/sshd_config:

```bash
$ sudo sed -i "s/without-password/yes/" /etc/ssh/sshd_config
$ sudo service ssh restart
```

This previous step will make some sysadmins cringe, and will not make
it into a production environment. Check with them.

Then, edit the file located at: /etc/ansible/ansible.cfg and uncomment
the line:

```bash
ask_pass      = True

```

This last step is required because Ansible uses the SSH protocol to
connect and push configurations. Here we are allowing authentication
by password (instead of public key only), which should be ok since we
run the job locally.

Check out the post_install.sh script if you want to run those commands
in batch.

# Development/Test environment

During the development of this application, we used a virtualized
environment based on [Vagrant](https://www.vagrantup.com/downloads.html).

In case you are interested to tryout the environment and/or further
develop the application, we have provided the vagrant config
file. Vagrant is available on many architectures, and can use Virtual
Box as a VM provider. Once installed, you can clone the CRISPR-Exposed
repository on github, then navigate to the Configuration folder.

```bash
$ cd CRISPR-Exposed/Configuration
$ vagrant up
$ vagrant ssh
```

From there, you can configure the environment as you would do for the
server. The vagrant playbooks described below would all be located in:

```bash
$ ssh localhost  #this is required to add the host key to the know_hosts
$ exit
$ cd /vagrant/Playbooks
$ ansible-playbook base.yml
$ ansible-playbook python.yml
```

# Configuration

## base.yml

This playbook configures the base environment. This includes
installing the packages required on the system, creating user, and
cloning the github repo of the project.

## mysql-secure.yml

Takes care of the setup of MySQL and creates a database for the
application and a user to access it. It also goes through some
housekeeping for a new installation of MySQL.

## python.yml

Though Ubuntu 14.04 uses python 2.7 as default (a good thing for us,
because Ansible won't run on python 3), our app is contained within a
python 3 virtual environment. So, this playbook installs the tools we
need. It includes creating the virtual environment, installing pip
packages, etc.

## pipelines.yml

Sets up the tools required by our different pipelines. 

## blast-local.yml

Uses NCBI's update-blastdb script to download and maintain a local
copy of the [nucleotide database](ftp://ftp.ncbi.nlm.nih.gov/blast/db/README).

## webapp.yml

Everything related to serving our webapp. To be defined