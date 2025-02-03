llama3.2:latest > 20-configure-helm - LLM Call Duration: 16.286513708997518
I'll generate Ansible roles to install Docker and Helm on your existing machines. Here are the roles:

**docker-role.yml**
```yaml
---
- name: Install and configure Docker
  become: yes

  tasks:
    - name: Add Docker GPG key
      apt_key:
        url: https://download.docker.com/linux/ubuntu/gpg
        state: present

    - name: Add Docker repository
      apt_repository:
        repo: 'https://download.docker.com/linux/ubuntu ${docker_version}'
        state: present

    - name: Install Docker
      apt:
        name: docker-ce
        state: present

    - name: Start and enable Docker service
      service:
        name: docker
        enabled: yes
        state: started

    - name: Configure Docker timeout
      file:
        path: /etc/docker/daemon.json
        mode: '0644'
        content: |
          {
            "storage-driver": "devicemapper",
            "timeout": 1200
          }

    - name: Add user to Docker group
      user:
        groups: docker
        name: "{{ ansible_user }}"
```

**helm-role.yml**
```yaml
---
- name: Install and configure Helm
  become: yes

  tasks:
    - name: Add Helm GPG key
      apt_key:
        url: https://storage.googleapis.com/helm/releases/latest/gpg
        state: present

    - name: Add Helm repository
      apt_repository:
        repo: 'https://stable.googleapis.com/kubernetes-release/release-{{ helm_version }}/deb ${distro_id} main'
        state: present

    - name: Install Helm
      apt:
        name: helm
        state: present

    - name: Configure Helm version
      file:
        path: /etc/helm/helm.conf
        mode: '0644'
        content: |
          repo = https://stable.googleapis.com/kubernetes-release/release-{{ helm_version }}
          apiVersion = v1

    - name: Add user to Helm group
      user:
        groups: docker
        name: "{{ ansible_user }}"
```

**main.yml**
```yaml
---
- name: Install and configure Docker and Helm on all hosts
  hosts: weywot, yerbouti, waza
  become: yes

  roles:
    - role: docker-role
      version: '1.0'
    - role: helm-role
      version: '1.0'
```

This Ansible playbook will install Docker and Helm on all specified hosts, including your development laptop (ywewot) and two Debian-based servers (yerbouti and waza). The roles are written in YAML and can be easily modified to suit your needs.

Note that you'll need to replace `helm_version` with the desired version of Helm. You can find available versions on the [Helm releases page](https://storage.googleapis.com/helm/releases/index.html).

Run the playbook using `ansible-playbook -i hosts main.yml`, where `hosts` is the file containing your machine's IP addresses or hostname.