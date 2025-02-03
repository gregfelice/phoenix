codellama:13b > 20-configure-helm - LLM Call Duration: 27.24321400000008

Here is an Ansible role to install Docker and Helm on a Debian-based system:
```yaml
---
- name: Install Docker and Helm
  hosts: all
  become: yes

  tasks:
    - name: Add Docker repository key
      apt_key:
        url: https://download.docker.com/linux/debian/gpg
        state: present

    - name: Add Docker repository
      apt_repository:
        repo: deb [arch=amd64] https://download.docker.com/linux/debian {{ ansible_distribution_version }} stable
        state: present

    - name: Install Docker package
      apt:
        name: docker-ce
        state: latest

    - name: Start Docker service
      service:
        name: docker
        enabled: yes
        state: started

    - name: Add Helm repository key
      command: curl https://baltocdn.com/helm/helm-v3.4.1-linux-amd64.tar.gz | tar xzvf -

    - name: Install Helm package
      apt_package:
        name: helm
        state: latest
```
This role will add the Docker repository key, add the Docker repository, install the Docker package, start the Docker service, and download and install the Helm package.

You can then use this role in your playbook like this:
```yaml
---
- name: Install Docker and Helm
  hosts: all
  become: yes
  roles:
    - docker_and_helm
```