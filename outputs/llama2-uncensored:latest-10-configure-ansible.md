llama2-uncensored:latest > 10-configure-ansible - LLM Call Duration: 11.220275625000795
Sure! Here's a role that installs software packages on every host using Ansible:
```yaml
# role name
name: package_installation

# this is an example of how to configure variables in your playbook
- name: Define host vars
 hosts: all
 
- set_fact:
   debian_os: false
   macos_os: true

- name: Install Git on macOS and Debian
 tasks:
 - name: Check OS type
   when: debian_os == False
   ignore_errors: True
 
 - name: Install Git on MacOS
   command: "brew install git"
   become: true
   async: false
 
- name: Check OS type
 
 if: macos_os
 
 - name: Install Zsh and Oh My Zsh
   command: "brew install zsh oh-my-zsh"
   become: true
   async: false
 
- name: Install BTop and Htop on MacOS
   command: "brew install btop htop"
   become: true
   async: false
```
You can customize the playbook to fit your specific needs. Let me know if you have any questions!