deepseek-r1:14b > 10-configure-ansible - LLM Call Duration: 65.77561479200085
<think>
Okay, so I need to create an Ansible role that installs some software packages on different hosts. The hosts have varying OSes—two are Debian and one is macOS. For Debian, I should use apt, and for macOS, brew.

First, I'll structure the role with tasks. Since each host might be either Debian or macOS, I need to detect the OS first. Ansible has a fact called ansible_os_family that can help here. So I'll set up conditionals based on whether it's 'Debian' or 'Darwin'.

For Debian hosts, I'll update the package list with apt-get update and then install git, zsh, oh-my-zsh, btop, and htop using apt-get install. For macOS, I'll use Homebrew (brew) to install these packages.

Wait, but oh-my-zsh isn't a system package. On Debian, maybe it's better to install zsh first, then download oh-my-zsh via curl. Similarly, on macOS, after installing zsh with brew, I should also get oh-my-zsh from the git repo.

I'll structure each task within a block, using when: ansible_os_family == "Debian" or "Darwin". For the curl commands, I'll make sure they run only on Debian since that's where oh-my-zsh isn't a package.

Finally, I'll include this role in my playbook so it runs on all three hosts. That should cover installing the necessary packages on each appropriately.
</think>

I'll help you create an Ansible role to install software packages on your systems. Here's the code:

```yaml
---
# File: roles/common_packages/tasks/main.yml

- name: Ensure package manager is updated
  become: yes
  apt:
    update_cache: yes
  when: ansible_os_family == "Debian"

- name: Install common packages using apt (Debian)
  become: yes
  apt:
    name:
      - git
      - zsh
      - htop
      - btop
    state: present
  when: ansible_os_family == "Debian"

- name: Ensure Homebrew is installed (MacOS)
  shell: /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
  when: ansible_os_family == "Darwin"
  become: yes

- name: Install common packages using Homebrew (MacOS)
  become: yes
  homebrew:
    name:
      - git
      - zsh
      - htop
      - btop
    state: present
  when: ansible_os_family == "Darwin"

- name: Ensure oh-my-zsh is installed (Debian systems)
  shell: sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"
  when: ansible_os_family == "Debian"
  become: yes

- name: Ensure oh-my-zsh is installed (MacOS systems)
  shell: sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"
  when: ansible_os_family == "Darwin"
  become: yes
```

Then, include this role in your playbook:

```yaml
---
# File: playbook.yml

- hosts: all
  roles:
    - common_packages
```

This Ansible role will:

1. Update package manager cache for Debian systems
2. Install packages (git, zsh, btop, htop) using apt on Debian systems
3. Handle Homebrew installation and package management on MacOS systems
4. Install oh-my-zsh on both Debian and MacOS systems

The role is OS-agnostic and will automatically detect whether it's running on a Debian or MacOS system to use the correct package manager.

To run this playbook, you can execute:

```bash
ansible-playbook playbook.yml -i inventory.yaml --become
```

Make sure your inventory file (`inventory.yaml`) properly defines your hosts (weywot, yerbouti, waza) with their respective operating systems.