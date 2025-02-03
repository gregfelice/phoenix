qwen2.5-coder:14b > 20-configure-helm - LLM Call Duration: 53.49127374999989
Sure! Below is an example of an Ansible role that installs Docker and Helm on a Debian-based system. This role can be applied to your `yerbouti` and `waza` hosts.

### Directory Structure

```plaintext
docker_helm_installation/
├── tasks/
│   └── main.yml
├── handlers/
│   └── main.yml
├── vars/
│   └── main.yml
└── defaults/
    └── main.yml
```

### tasks/main.yml

```yaml
---
- name: Update apt cache
  become: yes
  apt:
    update_cache: yes

- name: Install required packages for Docker and Helm
  become: yes
  apt:
    name:
      - apt-transport-https
      - ca-certificates
      - curl
      - software-properties-common
    state: present

- name: Add Docker’s official GPG key
  become: yes
  apt_key:
    url: https://download.docker.com/linux/debian/gpg
    state: present

- name: Set up the stable repository for Docker
  become: yes
  apt_repository:
    repo: "deb [arch=amd64] https://download.docker.com/linux/debian {{ ansible_distribution_release }} stable"
    state: present

- name: Install Docker CE
  become: yes
  apt:
    name: docker-ce
    state: present
    update_cache: no

- name: Ensure Docker service is running and enabled
  become: yes
  systemd:
    name: docker
    state: started
    enabled: yes

- name: Add current user to the Docker group
  become: yes
  user:
    name: "{{ ansible_user }}"
    groups:
      - docker
    append: yes

- name: Install Helm using curl
  become: yes
  shell: |
    curl https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3 | bash
```

### handlers/main.yml

```yaml
---
- name: Restart Docker service
  become: yes
  systemd:
    name: docker
    state: restarted
```

### vars/main.yml

```yaml
# Custom variables if needed
```

### defaults/main.yml

```yaml
# Default variables
```

### playbook.yml

To apply this role to your `yerbouti` and `waza` hosts, create a playbook like the following:

```yaml
---
- name: Install Docker and Helm on Debian-based systems
  hosts:
    - yerbouti
    - waza
  become: yes
  roles:
    - docker_helm_installation
```

### Running the Playbook

To run the playbook, use the following command:

```sh
ansible-playbook -i inventory_file playbook.yml
```

Replace `inventory_file` with your actual inventory file that includes the hosts `yerbouti` and `waza`.

This role will install Docker and Helm on the specified Debian-based systems. Note that for macOS (`weywot`), you would need a different approach, as Docker is typically installed via Homebrew or directly from Docker's website on macOS.