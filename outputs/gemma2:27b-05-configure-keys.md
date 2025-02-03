gemma2:27b > 05-configure-keys - LLM Call Duration: 74.34114341700115
```yaml
---
- hosts: all
  become: true
  roles:
    - software_installation

# Roles directory

roles/
└── software_installation
    ├── tasks
    │   └── main.yml
    └── handlers
        └── apt_update.yml

roles/software_installation/tasks/main.yml
---
- name: Detect OS and install packages
  ansible.builtin.debug:
    msg: "Host {{ inventory_hostname }} is running {{ ansible_distribution }}"

  # Debian systems use apt
  when: ansible_distribution == 'Debian'
  become: true

- name: Update apt cache
  apt: update_cache=yes
  register: apt_update
  notify:
    - Update apt cache

- name: Install packages using apt
  apt:
    name: "{{ item }}"
    state: present
  loop: 
    - nginx
    - git
  when: ansible_distribution == 'Debian'

# macOS systems use brew
  when: ansible_distribution == 'MacOS'

- name: Install Homebrew if not installed
  command: /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
  when: not ansible_facts['homebrew_installed']

- name: Ensure brew is up to date
  command: brew update

- name: Install packages using brew
  brew:
    name: "{{ item }}"
    state: present
  loop:
    - nginx
    - git

roles/software_installation/handlers/apt_update.yml
---
- name: Update apt cache
  apt: update_cache=yes



```

 **SSH Key Configuration (Separate Role)**


You'll need a separate role for SSH key configuration. This is best practice to keep roles focused.

```yaml
---
- hosts: all
  become: true
  roles:
    - ssh_keys

roles/ssh_keys/tasks/main.yml
---
- name: Generate SSH Key Pair
  ssh_keygen: 
    state: present

- name: Add Public Key to Authorized Keys
  copy:
    src: ~/.ssh/id_rsa.pub
    dest: ~/.ssh/authorized_keys
    mode: '0600'
```

**Important Considerations:**



* **Inventory:** Make sure you have an inventory file (`hosts`) that correctly defines your machines (weywot, yerbouti, waza).
* **SSH Access:** Ensure Ansible can connect to the target hosts via SSH.

* **Security:**  Consider using SSH keys for authentication instead of passwords for enhanced security.