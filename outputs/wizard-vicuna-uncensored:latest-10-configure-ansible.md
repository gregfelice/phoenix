wizard-vicuna-uncensored:latest > 10-configure-ansible - LLM Call Duration: 36.80668016600066
# This role installs software packages on every host using the appropriate package manager based on the OS type.
- name: Install Software Packages
  hosts: all
  become: True
  tasks:
 - name: Check OS type
 c:
 - os: '{{ item }}'
 - set_fact: package_manager={{ lookup('package_manager', item) }}
   when: item in ['debian', 'macos']
 - debug:
 - item
 - package_manager
 - package_install
 
- name: Install Git
  command: apt-get install git
  when: package_manager == 'apt' and os == 'debian'

- name: Install ZSH
  command: brew install zsh
  when: package_manager == 'brew' and os == 'macos'

- name: Install Oh-My-Zsh
  command: brew install oh-my-zsh
  when: package_manager == 'brew' and os == 'macos'

- name: Install Btop
  command: apt-get install btop
  when: package_manager == 'apt' and os == 'debian'

- name: Install Htop
  command: apt-get install htop
  when: package_manager == 'apt' and os == 'debian'

- name: Check if the server is running
  command: service {{ item }} status
  with_items: ['mysqld', 'postgres']
  when: package_install.contains(item):
 - debug:
 - item
 - service_status

# This role configures the development laptop to use Git, ZSH, Oh-My-Zsh and Btop on MacOS and Htop on Debian.
- name: Configure Weywot Development Laptop
  hosts: weywot
  become: True
  tasks:
 - name: Check OS type
 c:
 - os: 'macos'
 - set_fact: package_manager = 'brew'
   when: item in ['debian', 'macos']
 - debug:
 - item
 - package_manager
 - package_install
 
- name: Install Git
  command: brew install git
  when: package_install.contains('git') and package_manager == 'brew'

- name: Install ZSH
  command: brew install zsh
  when: package_install.contains('zsh') and package_manager == 'brew'

- name: Install Oh-My-Zsh
  command: brew install oh-my-zsh
  when: package_install.contains('oh-my-zsh') and package_manager == 'brew'

- name: Install Btop
  command: brew install btop
  when: package_install.contains('btop') and package_manager == 'brew'

- name: Install Htop
  command: apt-get install htop
  when: package_install.contains('htop') and package_manager == 'apt'

# This role configures the generic host to use Git, ZSH, Oh-My-Zsh and Btop on Debian.
- name: Configure Yerbouti Generic Host
  hosts: yerbouti
  become: True
  tasks:
 - name: Check OS type
 c:
 - os: 'debian'
 - set_fact: package_manager = 'apt'
   when: item in ['debian', 'macos']
 - debug:
 - item
 - package_manager
 - package_install
 
- name: Install Git
  command: apt-get install git
  when: package_install.contains('git') and package_manager == 'apt'

- name: Install ZSH
  command: apt-get install zsh
  when: package_install.contains('zsh') and package_manager == 'apt'

- name: Install Oh-My-Zsh
  command: apt-get install oh-my-zsh
  when: package_install.contains('oh-my-zsh') and package_manager == 'apt'

- name: Install Btop
  command: apt-get install btop
  when: package_install.contains('btop') and package_manager == 'apt'

- name: Install Htop
  command: apt-get install htop
  when: package_install.contains('htop') and package_manager == 'apt'