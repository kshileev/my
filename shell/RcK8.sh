function 8ns() {
    local pod=${1-kube-proxy}
    kubectl get pod -A | grep "$pod" | tr -s "[:space:]" | awk '{print $1}'
}
function 8pod() {
    local pod=${1-kube-proxy}
    kubectl get pod -A | grep "$pod" | tr -s "[:space:]" | awk '{print $2}'
}
function 8bash() {
    local pod=${1-lfs-lfs}
    # shellcheck disable=SC2124
    local cmd="${@:2}"
    local ns
    [[ -z $cmd ]] && cmd=bash
    pod=$(8pod "$pod")
    ns=$(8ns "$pod")
    kubectl exec -it "$pod" -n "$ns"  -- $cmd
}
function 8cp() { # copy file into pod
  # shellcheck disable=SC2155
  local pod=$(8pod "$2")
  # shellcheck disable=SC2155
  local ns=$(8ns "$pod")

  kubectl cp "$1" "$ns"/"$pod":"$3"
  echo $1 copied to:
  8bash "$pod" ls "$3"
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
    local ns
    local list

    ns=${1-ngupf}
    list=$(kubectl -n "$ns" get pods -o jsonpath="{..image}" |tr -s '[:space:]' '\n' |sort | uniq)

    for t in "${list[@]}"; do
        docker pull "$t"
    done
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
