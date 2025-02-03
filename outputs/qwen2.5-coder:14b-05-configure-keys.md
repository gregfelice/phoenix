qwen2.5-coder:14b > 05-configure-keys - LLM Call Duration: 57.59090804100015
Certainly! Below is an Ansible role that installs software packages on Debian and macOS systems using the appropriate package manager. Additionally, it creates and configures SSH keys for use with Ansible.

### Directory Structure
```
roles/
├── install_packages/
│   ├── tasks/
│   │   └── main.yml
│   ├── vars/
│   │   └── main.yml
│   └── handlers/
│       └── main.yml
└── ssh_keys/
    ├── tasks/
    │   └── main.yml
    ├── files/
    │   ├── id_rsa
    │   └── id_rsa.pub
    └── vars/
        └── main.yml
```

### install_packages/tasks/main.yml
```yaml
---
- name: Install packages using apt for Debian systems
  apt:
    name: "{{ packages }}"
    state: present
  when: ansible_os_family == 'Debian'

- name: Install packages using brew for macOS systems
  homebrew:
    name: "{{ packages }}"
    state: present
  when: ansible_os_family == 'Darwin'
```

### install_packages/vars/main.yml
```yaml
---
packages:
  - vim
  - curl
  - git
  # Add more packages as needed
```

### install_packages/handlers/main.yml
```yaml
---
- name: Restart services after package installation
  service:
    name: "{{ item }}"
    state: restarted
  loop: "{{ restart_services }}"
```

### ssh_keys/tasks/main.yml
```yaml
---
- name: Create .ssh directory if it does not exist
  file:
    path: ~/.ssh
    state: directory
    mode: '0700'

- name: Copy private key to the server
  copy:
    src: files/id_rsa
    dest: ~/.ssh/id_rsa
    owner: "{{ ansible_user }}"
    group: "{{ ansible_user }}"
    mode: '0600'
  notify: Update SSH keys

- name: Copy public key to the server
  copy:
    src: files/id_rsa.pub
    dest: ~/.ssh/id_rsa.pub
    owner: "{{ ansible_user }}"
    group: "{{ ansible_user }}"
    mode: '0644'

- name: Add SSH public key to authorized_keys
  lineinfile:
    path: ~/.ssh/authorized_keys
    line: "{{ lookup('file', '~/.ssh/id_rsa.pub') }}"
    state: present
  notify: Update SSH keys

- name: Set correct permissions for authorized_keys
  file:
    path: ~/.ssh/authorized_keys
    mode: '0644'
```

### ssh_keys/files/id_rsa
```plaintext
# Copy your private key here
```

### ssh_keys/files/id_rsa.pub
```plaintext
# Copy your public key here
```

### Playbook Example
```yaml
---
- name: Configure system environments
  hosts: all
  become: yes

  roles:
    - install_packages
    - ssh_keys
```

### Inventory Example
```ini
[weywot]
weywot ansible_host=192.168.1.100 ansible_user=your_username

[yerbouti]
yerbouti ansible_host=192.168.1.101 ansible_user=your_username

[waza]
waza ansible_host=192.168.1.102 ansible_user=your_username
```

This setup will ensure that the appropriate package manager is used based on the operating system and SSH keys are configured for secure communication between your Ansible control node and managed hosts.