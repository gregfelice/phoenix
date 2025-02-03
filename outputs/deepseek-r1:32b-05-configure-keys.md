deepseek-r1:32b > 05-configure-keys - LLM Call Duration: 192.96801974999835
<think>
Okay, I need to help the user by creating Ansible roles to configure their system environments. They have three machines: weywot (MacOS), yerbouti (Debian), and waza (Debian). The main tasks are installing software packages using the appropriate package manager and setting up SSH keys for Ansible.

First, I'll start with the package installation role. Since the OS varies, I need to detect whether it's Debian or MacOS. For Debian, we'll use apt, and for MacOS, brew. I should structure this in a way that Ansible can handle conditionally. Maybe using variables to determine the package manager.

Next, SSH key configuration is crucial for Ansible to communicate between hosts. The user will need an SSH key pair on each machine. On Debian hosts, the keys go into ~/.ssh/, while on MacOS, it's the same but might require different permissions or steps. I should ensure that the public key is added to authorized_keys so that Ansible can connect without password prompts.

I'll structure the roles in separate directories under roles/. Each role will have tasks, templates, and maybe handlers if needed. For the package installation, variables like os_family can help determine which package manager to use. I should include a pre-task to update package lists on Debian systems.

For SSH keys, using Ansible's built-in modules like file, command, and authorized_key would be efficient. The user may need different key pairs for each host or a shared one; the example uses a single pair, but they might want separate ones depending on their setup.

I also need to make sure that the permissions are correct, especially for SSH keys. On Debian, ensuring the .ssh directory has 700 permissions and the keys have 600 is standard. For MacOS, similar permissions apply, but sometimes users might have different settings, so it's good to enforce this.

Testing each role separately would be a good idea before combining them. Maybe run each task on one host first to ensure there are no issues with package installation or SSH key setup.

Finally, I should provide an example inventory file that includes all three hosts, grouped by their OS family. This way, the user can easily apply the roles to the correct groups without manually specifying each time.

I think I covered the main points. Now, let me structure this into actual Ansible code for both roles.
</think>

Here is an Ansible role configuration that will handle installing software packages and configuring SSH keys across different operating systems:

```yaml
# Install Software Packages Role: roles/install_packages/tasks/main.yml
---
- name: Update package cache on Debian systems
  apt:
    update_cache: yes
  when: ansible_os_family == 'Debian'

- name: Install required packages with APT (Debian)
  apt:
    name: "{{ packages_apt }}"
    state: present
  when: ansible_os_family == 'Debian'

- name: Install Homebrew on MacOS if not installed
  homebrew:
    name: brew
    state: present
  when: ansible_platform_id == 'macos'

- name: Install required packages with Brew (MacOS)
  homebrew:
    name: "{{ packages_brew }}"
    state: present
  loop: "{{ packages_brew }}"
  when: ansible_platform_id == 'macos'
```

```yaml
# SSH Key Configuration Role: roles/configure_ssh/tasks/main.yml
---
- name: Create .ssh directory if it doesn't exist
  file:
    path: ~/.ssh
    state: directory
    mode: 0700

- name: Generate SSH key pair if not exists
  command: ssh-keygen -t rsa -b 4096 -f ~/.ssh/id_rsa -N ""
  args:
    creates: ~/.ssh/id_rsa

- name: Add public key to authorized_keys
  authorized_key:
    user: "{{ ansible_user }}"
    state: present
    key: "{{ lookup('file', '~/.ssh/id_rsa.pub') }}"
```

To use these roles, create an inventory file with your hosts:

```ini
# Inventory file: inventory/hosts
[development]
weywot

[servers]
yerbouti
waza

[all]
weywot ansible_python_interpreter=/usr/bin/python3
yerbouti
waza
```

Then, create a playbook to use these roles:

```yaml
# Playbook: site.yml
---
- name: Configure all systems
  hosts: all
  become: yes
  roles:
    - install_packages
    - configure_ssh

  vars:
    packages_apt:
      - git
      - python3
      - python3-pip
    packages_brew:
      - git
      - python@3.9
```

To run the playbook:

```bash
ansible-playbook -i inventory/hosts site.yml --ask-become-pass
```

This setup will:
1. Install required packages using APT on Debian systems and Brew on MacOS.
2. Configure SSH keys for Ansible communication across all hosts.

Make sure to adjust the `packages_apt` and `packages_brew` lists according to your specific needs.