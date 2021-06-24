function 8ns() {
    local pod=${1-cache-pod-0}
    kubectl get pod -A | grep "$pod" | tr -s "[:space:]" | awk '{print $1}'
}

function 8cp() { # copy file into pod
    kubectl cp test_profile.tgz smi/ops-center-smi-cluster-deployer-6bccc7fd4b-d5px5:/data/software/host-profile
    kubectl exec -it smi/ops-center-smi-cluster-deployer-6bccc7fd4b-d5px5 'ls /date/software'
}

function 8bash() {
    local pod=$1
    local cmd=${2-bash}
    local ns

    ns=$(8ns "$pod")
    kubectl -n "$ns" exec -it "$pod"  -- "$cmd"
}

function 8hugepages() {
    local node

    node=$(kubectl get node | grep Ready | cut -f1 -d ' ')
    sudo sysctl vm.nr_hugepages=2048
    sudo systemctl restart kubelet
    kubectl describe node "$node" | grep huge
}

function kk8() {
    local what

    what=$(ksGetInput 'pod bar')
    echo "$what"
}

function 8lbl() {  # assign label to node
    local node=$1
    local lbl=${2-smi-cisco.com/node-type=ngupf}
    kubectl label node "$node" "$lbl"
}

function 8problem() {
    local pod=${1-cache-pod-0}
    local ns
    ns=$(8ns "$pod")
    kubectl describe pod "$pod" -n "$ns"
    echo --------------------------------------------------------
    kubectl logs "$pod" -n "$ns"
    echo --------------- log of "$pod" ----------------------------
}

function 8docker_pull(){  # pull all images used by k8s pods from docker registry
    local ns, list

    ns=${1-ngupf}
    list=$(kubectl -n "$ns" get pods -o jsonpath="{..image}" |tr -s '[:space:]' '\n' |sort | uniq)

    for t in "${list[@]}"; do
        docker pull "$t"
    done
}

function u(){
  local pod
  local ns

  pod=$(kubectl get pod -A | grep ops-center-ngupf | awk '{ print $2}')
  ns=$(8ns "$pod")
  kubectl -n "$ns" exec -it -c confd "$pod" -- /var/confd/bin/confd_cli -u admin
}

function v(){
  local pod

  pod=$(kubectl get pod -A | grep ngupf-fe | awk '{ print $2}')
  8bash "$pod" vppctl
}

function p(){
  local pod

  pod=$(kubectl get pod -A | grep patsworkspace | awk '{ print $2}')
  8bash "$pod"
}

function upf_get_cfg(){
  local pod
  local ns

  pod=$(kubectl get pod -A | grep ops-center-ngupf | awk '{ print $2}')
  ns=$(8ns "$pod")
  kubectl -n "$ns" exec -i -c confd "$pod" -- /var/confd/bin/confd_load -f /tmp/opscenter_cfg
  kubectl cp "$ns/$pod":/tmp/opscenter_cfg OPS.CFG -c confd >> /dev/null
  less OPS.CFG
}

alias k='kubectl'
alias ka='kubectl get ns,node,deployment,replicaset,pod,service,ing,pvc,pv,cm,secrets'
alias kd='kubectl get deployments --all-namespaces'
alias ke='kubectl get events'
alias kn='kubectl get nodes --show-labels'
alias kns='kubectl get namespace'
alias kp='kubectl get pods --all-namespaces'
alias ks='kubectl get services'
alias krbac='kubectl get ClusterRoleBinding -A'
