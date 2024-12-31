ansible-playbook deploy-full.yml -i inventory.yml --extra-vars cluster_state=present
ansible-playbook deploy-k8s-cluster.yml -i inventory.yml --extra-vars cluster_state=present