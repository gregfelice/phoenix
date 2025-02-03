codellama:13b > 10-configure-ansible - LLM Call Duration: 35.568891333001375
Here is a sample Ansible role that should accomplish what you are asking for:
```yaml
---
- name: Install software packages on all hosts
  hosts: all
  become: yes

  tasks:
    - name: Detect OS and install appropriate package manager
      shell: |
        if [ "$(uname)" = "Darwin" ]; then
          brew update && brew upgrade
        elif [ "$(uname)" = "Linux" ]; then
          apt-get update && apt-get upgrade
        fi
      args:
        executable: /bin/bash
      become_user: root
    - name: Install Git
      shell: |
        if [ "$(uname)" = "Darwin" ]; then
          brew install git
        elif [ "$(uname)" = "Linux" ]; then
          apt-get install git
        fi
      args:
        executable: /bin/bash
      become_user: root
    - name: Install Zsh and Oh My Zsh
      shell: |
        if [ "$(uname)" = "Darwin" ]; then
          brew install zsh oh-my-zsh
        elif [ "$(uname)" = "Linux" ]; then
          apt-get install zsh oh-my-zsh
        fi
      args:
        executable: /bin/bash
      become_user: root
    - name: Install Btop and Htop
      shell: |
        if [ "$(uname)" = "Darwin" ]; then
          brew install btop htop
        elif [ "$(uname)" = "Linux" ]; then
          apt-get install btop htop
        fi
      args:
        executable: /bin/bash
      become_user: root
```
This role will detect the OS of each host and use the appropriate package manager to install Git, Zsh, Oh My Zsh, Btop, and Htop. The `shell` module is used to execute the installation commands directly on the target machine.

You can add this role to your playbook by adding a line like this:
```yaml
---
- name: Install software packages on all hosts
  hosts: all
  become: yes
  roles:
    - install_software
```
This will include the `install_software` role in your playbook, and it will be executed for every host specified in the `hosts` parameter.