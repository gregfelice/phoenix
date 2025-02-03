wizard-vicuna-uncensored:latest > 05-configure-keys - LLM Call Duration: 20.167468957999517
Here is a role that installs software packages on every host, detects if the OS is Debian or MacOS, and creates SSH keys:
```python
from ansible.utils import getsystem_fallback
from ansible.inventory import InventoryFile

class SoftwareInstallerRole(object):
 def __init__(self, inventory_file=None):
 self.inventory_file = inventory_file or InventoryFile()
 
 def run(self):
 if getsystem_fallback().system == "macos":
 package_manager = "brew"
 else:
 package_manager = "apt"
 
 # Install packages on all hosts
 self.install_packages(package_manager)
 
 # Create and configure SSH keys
 self.configure_ssh_keys()
 
 def install_packages(self, package_manager):
 tasks = []
 for host in self.inventory_file:
 if host["hostname"].startswith("w"):
 tasks.append({"name": "apt-get", "args": {"update": True, "yes": False}, "hosts": host})
 elif host["hostname"].startswith("y"):
 tasks.append({"name": "brew", "args": {"install": "nginx"}, "hosts": host})
 else:
 tasks.append({"name": "apt-get", "args": {"update": True, "yes": False}, "hosts": host})
 
 return tasks
 
 def configure_ssh_keys(self):
 if self.inventory_file["wawa"].os == "macos":
 # Use brew to install SSH key utility
 self.install_packages({"name": "brew", "args": {"update": True, "yes": False}, "hosts": ["wawa"]})
 else:
 # Use apt-key to generate and upload SSH key
 self.install_packages({"name": "apt-get", "args": {"update": True, "yes": False}, "hosts": ["wawa"]})
 
 # Configure SSH keys on all hosts
 for host in self.inventory_file:
 if host["hostname"].startswith("w") and host["os"] == "macos":
 self.install_packages({"name": "brew", "args": {"update": True, "yes": False}, "hosts": host})
 else:
 # Use apt-key to generate and upload SSH key
 self.install_packages({"name": "apt-get", "args": {"update": True, "yes": False}, "hosts": host})
