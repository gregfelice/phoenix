qwen2.5-coder:latest > 20-configure-helm - LLM Call Duration: 20.538632457999483
```yaml
# Role: docker_helm_installation

# tasks/main.yml

- name: Update apt cache on Debian-based systems
  apt:
    update_cache: yes

- name: Install prerequisites for Docker and Helm
  apt:
    name: "{{ item }}"
    state: present
    update_cache: yes
  loop:
    - apt-transport-https
    - ca-certificates
    - curl
    - gnupg-agent
    - software-properties-common

- name: Add Docker’s official GPG key
  apt_key:
    url: https://download.docker.com/linux/debian/gpg
    state: present

- name: Set up stable Docker repository on Debian-based systems
  apt_repository:
    repo: deb [arch=amd64] https://download.docker.com/linux/debian $(lsb_release -cs) stable
    state: present

- name: Install Docker CE (Community Edition)
  apt:
    name: docker-ce
    state: present

- name: Start and enable Docker service
  service:
    name: docker
    state: started
    enabled: yes

- name: Add user to the Docker group (optional)
  user:
    name: "{{ ansible_user }}"
    groups: docker
    append: yes

- name: Install Helm package manager
  helm:
    repository: https://charts.helm.sh/stable
    state: present

- name: Initialize Helm
  command: helm init --client-only
  args:
    creates: /usr/local/bin/helm

# meta/main.yml
dependencies:

# README.md
# This Ansible role installs Docker and Helm on Debian-based systems.
# It updates the apt cache, installs prerequisites for Docker, adds Docker's official GPG key,
# sets up the stable Docker repository, installs Docker CE (Community Edition),
# starts and enables the Docker service, and optionally adds the current user to the Docker group.
# It also initializes Helm with a client-only installation.

# Usage:
# Include this role in your playbook to install Docker and Helm on Debian-based systems.
```

This Ansible role will configure Docker and Helm on Debian-based systems. Ensure that you have the necessary permissions to run these tasks, especially when installing packages and modifying system configurations.