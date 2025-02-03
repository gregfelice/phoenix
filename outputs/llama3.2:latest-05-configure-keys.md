llama3.2:latest > 05-configure-keys - LLM Call Duration: 26.684676624998247
Here are the Ansible roles that meet your requirements:

**roles/setup.yml**

```yml
---
- name: Setup
  hosts: all
  become: yes

  vars:
    ssh_key_path: ~/.ssh/id_rsa
    ssh_key_dir: ~/

  tasks:
  - name: Generate SSH key pair
    user:
      name: root
      home: ~
      append: yes
      shell: /bin/bash
    when: inventory_hostname in ['ywot', 'waza']

  - name: Create SSH key file
    copy:
      content: "{{ lookup('file', ssh_key_path) }}\n{{ lookup('file', ssh_key_dir)}}\n"
      dest: "{{ ssh_key_dir }}"
    when: inventory_hostname in ['ywot', 'waza']
    notify: Regenerate SSH key pair

  - name: Copy SSH public key
    copy:
      content: "{{ lookup('file', ssh_key_path) }}"
      dest: "~/.ssh/id_rsa.pub"
      mode: '0644'
    when: inventory_hostname in ['ywot', 'waza']

  - name: Create SSH key pair for localhost
    user:
      name: root
      home: ~
      append: yes
      shell: /bin/bash
    when: inventory_hostname == 'localhost'

  - name: Copy SSH public key
    copy:
      content: "ssh-rsa {{ lookup('file', ssh_key_path) }} localhost"
      dest: "~/.ssh/hosts"
      mode: '0644'
    when: inventory_hostname == 'localhost'

  - name: Configure SSH keys
    ansible.posix.ssh_key:
      key_file: "{{ ssh_key_dir }}"
      host: all
    when: inventory_hostname in ['ywot', 'waza']
```

**roles/debian.yml**

```yml
---
- name: Debian
  hosts: yerbouti, waza
  become: yes

  vars:
    apt_repos:
      - "deb http://http.debian.net/ wheezy main"
    apt_packages:
      - "git"

  tasks:
  - name: Install APT package manager
    apt:
      update_cache: yes
    when: inventory_hostname == 'ywouti'

  - name: Install SSH package
    apt:
      name: openssh-server

  - name: Generate SSH key pair
    user:
      name: root
      home: ~
      append: yes
      shell: /bin/bash
    when: inventory_hostname in ['ywouti', 'waza']

  - name: Create SSH key file
    copy:
      content: "{{ lookup('file', '/root/.ssh/id_rsa') }}\n{{ lookup('file', '~/.ssh/id_rsa.pub') }}"
      dest: "/root/.ssh/id_rsa"
    when: inventory_hostname in ['ywouti', 'waza']
    notify: Regenerate SSH key pair

  - name: Copy SSH public key
    copy:
      content: "{{ lookup('file', '/root/.ssh/id_rsa.pub') }}"
      dest: "~/.ssh/id_rsa.pub"
      mode: '0644'
    when: inventory_hostname in ['ywouti', 'waza']

  - name: Configure SSH keys
    ansible.posix.ssh_key:
      key_file: "/root/.ssh/id_rsa"
      host: all
```

**roles/macos.yml**

```yml
---
- name: Macos
  hosts: yewot
  become: yes

  vars:
    brew_repos:
      - "https://github.com/Homebrew/homebrew/releases/download/ latest homebrew.git"
    brew_packages:
      - "git"

  tasks:
  - name: Install Homebrew package manager
    brew:
      update_cache: yes

  - name: Install SSH package
    brew:
      name: ssh

  - name: Generate SSH key pair
    user:
      name: root
      home: ~
      append: yes
      shell: /bin/bash
    when: inventory_hostname == 'ywot'

  - name: Create SSH key file
    copy:
      content: "{{ lookup('file', '/root/.ssh/id_rsa') }}\n{{ lookup('file', '~/.ssh/id_rsa.pub') }}"
      dest: "/root/.ssh/id_rsa"
    when: inventory_hostname == 'ywot'
    notify: Regenerate SSH key pair

  - name: Copy SSH public key
    copy:
      content: "{{ lookup('file', '/root/.ssh/id_rsa.pub') }}"
      dest: "~/.ssh/id_rsa.pub"
      mode: '0644'
    when: inventory_hostname == 'ywot'

  - name: Configure SSH keys
    ansible.posix.ssh_key:
      key_file: "/root/.ssh/id_rsa"
      host: all
```

You can add these roles to your Ansible playbook like this:

```yml
---
- name: Setup
  hosts: yewot, yerbouti, waza
  become: yes

  roles:
    - roles/setup.yml
    - roles/debian.yml
    - roles/macos.yml
```

This will install the SSH package manager and generate a new SSH key pair for each host. The SSH public key will be copied to the `~/.ssh/hosts` file on macOS hosts, and to the `/root/.ssh/id_rsa.pub` file on Debian hosts.

Please note that you should modify the roles according to your needs and adjust them as necessary for your specific setup.