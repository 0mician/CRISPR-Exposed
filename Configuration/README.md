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
$ sudo apt-add-repository ppa:ansible/ansible
$ sudo apt-get update
$ sudo apt-get install ansible
```

Configure the target host (here, we work locally, on our server):

```bash
$ echo "[crispr-exposed]" > /etc/ansible/hosts
$ echo "127.0.0.1" >> /etc/ansible/hosts
```

Then, edit the file located at: /etc/ansible/ansible.cfg and uncomment
the lines:

```bash
ask_sudo_pass = True
ask_pass      = True

```

This last step is required because Ansible uses the SSH protocol to
connect and push configurations. Here we are allowing authentication
by password (instead of public key only), which is ok since we run the
job locally.

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
$ cd /vagrant/
```

# Configuration

## Base

This playbook configures the base environment. This includes
installing the packages required on the system, creating user, folders,
the database, etc.

## Python environment

Though Ubuntu 14.04 uses python 2.7 as default (a good thing for us,
because Ansible won't run on python 3), our app is contained within a
python 3 virtual environment. So, this playbook installs the tools we
need. It includes creating the virtual environment, installing pip
packages, etc.

## Web application

Everything related to serving our webapp. This playbook installs and
configures apache2 to serve the django app.