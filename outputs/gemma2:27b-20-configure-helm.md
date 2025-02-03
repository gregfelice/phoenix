gemma2:27b > 20-configure-helm - LLM Call Duration: 77.0320386250005
```yaml
---
# Role to install Docker and Helm

- hosts: all
  become: true
  roles:
    - role: docker
    - role: helm
      
---

# Roles definitions

# role/docker/tasks/main.yml

---
- name: Install Docker dependencies
  apt:
    name: apt-transport-https ca-certificates curl gnupg lsb-release
    state: present
  when: ansible_distribution == 'Debian'

- name: Add Docker GPG key
  apt_key:
    url: https://download.docker.com/linux/debian/gpg
    state: present

- name: Add Docker repository
  apt_repository:
    repo: deb [arch=$(dpkg --print-architecture)] https://download.docker.com/linux/debian $(lsb_release -cs) stable
    state: present
    filename: docker.list

- name: Install Docker CE
  apt:
    name: docker-ce
    state: present

- name: Start and enable Docker service
  service:
    name: docker
    state: started
    enabled: yes



# role/helm/tasks/main.yml

---
- name: Add Helm repository
  apt_repository:
    repo: 'deb https://balto.debian.org/debian buster main'
    state: present
    filename: helm.list

- name: Install Helm
  apt:
    name: helm
    state: present
```


**Explanation:**



* **Roles Structure**: The code defines two Ansible roles: `docker` and `helm`. Each role has its own tasks directory (`tasks/main.yml`) containing the specific steps for installation.

* **Docker Role (role/docker/tasks/main.yml):**

    * **Dependencies:** Installs necessary packages for Docker on Debian systems using `apt`.
    * **GPG Key:** Adds Docker's GPG key for package authentication.
    * **Repository:**  Adds the official Docker repository to the system.
    * **Installation:** Installs the `docker-ce` package.
    * **Service Management:** Starts and enables the Docker service.

* **Helm Role (role/helm/tasks/main.yml):**

    * **Repository:** Adds the Helm repository for Debian systems.
    * **Installation:** Installs the `helm` package. 


**Important Considerations:**



* **Operating Systems:** This code assumes you are running Debian on your servers (`yerbouti`, `waza`). The Docker installation part is tailored specifically for Debian.

* **Customization:** You might need to adjust these roles based on your specific requirements, such as:
    * Different Docker versions. 
    * Helm plugins or customizations.
    * Additional configuration options for Docker or Helm.