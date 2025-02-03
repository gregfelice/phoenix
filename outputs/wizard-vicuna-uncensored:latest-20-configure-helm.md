wizard-vicuna-uncensored:latest > 20-configure-helm - LLM Call Duration: 32.381370666000294
Here's an Ansible role to install Docker and Helm on Debian machines:
```python
from ansible.module_utils.basic import *
import yaml
# Define the playbook
roles:
 - name: Install Docker and Helm
 tasks:
 # Load the role configuration from YAML
 - set_fact:
 vars:
 docker_version: '19.03'
 helm_version: '2.4.1'
 - include: /etc/ansible/roles/docker-helm.yaml
 
 # Download and install Docker and Helm
 - name: Install Docker
 hosts: all
 tasks:
 - docker:
 name: "{{ docker_version }}"
 state: present
 extra:
 services:
 - docker
 - dns
 - etcd
 - kubelet
 - kubernetes-dashboard
 - kubectl
 - kubefed
 - kube-scheduler
 - kubernetes-cni
 - fluentd
 - calico
 - kibana
 - openshift-config-generator
 - openshift-node-config-generator
 - k3s
 - kops
 - kube-apiserver
 - kube-controller-manager
 - kube-scheduler
 - kubernetes-dashboard
 - kubectl
 - kubelet
 - kubernetes-dashboard
 - kubefed
 - kube-scheduler
 - kubernetes-cni
 - fluentd
 - calico
 - kibana
 - openshift-config-generator
 - openshift-node-config-generator
 - k3s
 - kops
 - kube-apiserver
 - kube-controller-manager
 - kube-scheduler
 - kubernetes-dashboard
 - kubectl
 - kubelet
 # Install Helm
 - name: Install Helm
 hosts: all
 tasks:
 - helm:
 version: "{{ helm_version }}"
 state: present
 extra:
 services:
 - kibana
 - calico
 
 # Save the configuration
 - set_fact:
 vars:
 playbook_path: "/etc/ansible/roles/docker-helm.yaml"
 role_name: "{{ role }}"
 role_version: "{{ docker_version }}-{{ helm_version }}"
 
 # Copy the configuration to /etc/ansible/
 - copy:
 dest: "/etc/ansible/roles/docker-helm.yaml"
 content: "{{ playbook_path }}"
 
# Load the role configuration from YAML
- include: /etc/ansible/roles/docker-helm.yaml
```
This Ansible role uses the `docker` and `helm` modules to install Docker version `{{ docker_version }}` and Helm version `{{ helm_version }}`. It also includes the necessary services for Docker and Helm to function properly, such as kubelet, kubernetes-dashboard, and kubectl.
To use this role on a Debian machine (`hostname: waza`), you can run the following command:
```bash
ansible-role-install --name docker-helm --path /etc/ansible/roles/docker-helm.yaml
```
This will install the Ansible role for Docker and Helm onto the `waza` machine, and save it in `/etc/ansible/`. You can then use this configuration to configure other Debian machines (`hostname: weywot` and `hostname: yerbouti`) by running the following command:
```bash
ansible-role-apply --name docker-helm --inventory /etc/ansible/inventory/ --extra-vars "{{ playbook_path }}: {{ role_version }}". 
```