# shell login interactive shell: /etc/shell then ~/.bash_profile
# shell Non-log shell: execute ~/.bashrc only
# shell Non-interactive shell: execute script pointed by $ENV, nothing if $ENV = ""

THIS_FILE_PATH=$(find ~/repo ~/.kir -name my.sh 2>/dev/null)
MY_SHELL_DIR=$(dirname "$THIS_FILE_PATH")
export MY_TMP_DIR=/tmp/${USER}
export TZ='Europe/Moscow'
mkdir -p "${MY_TMP_DIR}"

[[ "$SHELL" == *zsh ]] && PROMPT='%F{green}%2~%f '
[[ "$SHELL" == *zsh ]] && ln -fs "$THIS_FILE_PATH" ~/.zshrc || ln -fs "$THIS_FILE_PATH" ~/.bash_aliases
[[ "$SHELL" == *zsh ]] && alias src=". ~/.zshrc" || alias src=". ~/.bash_aliases"

alias a='alias'
alias df='df -h'
alias du='du -h'
alias e='echo'
alias h='history'
alias l='ls -F'
alias l.='ls -dh .*'
alias ll='ls -Flih'
alias ll.='ls -Fldih .*'
alias ld='ls -lad'
alias m='less'

function 0read() {  # 0read prompt_text default_value
  local usr_val=${2-default_user_value}
  local txt
  txt="${1-Enter value} [default=${usr_val}]: "
  [[ "$SHELL" == *zsh ]] && read -r "usr_val?$txt?" || read -p "$txt" usr_val
  [[ -z $usr_val ]] && usr_val=$2
  echo "$usr_val"
}
function 0script_exe() { # source script from my/shell folder
  local path=$MY_SHELL_DIR/${1-'default'}
  [[ -f $path ]] || return
  source $path
  echo "$path" loaded
}
function 1init()  { # deploy starting my.sh scripts
  local host

	grep 'Host ' ~/.ssh/config
	host=$(0read 'Choose remote for deploy' 'NoNode')
	echo "Deploying to ${host}:"
	ssh-copy-id "$host"
	ssh "${host}" rm -rf .kir
	scp -r "${MY_SHELL_DIR}" "${host}":.kir
	scp "${MY_SHELL_DIR}/../cnUPF/RcUpf.sh"  "${host}":.kir/
	ssh "${host}" . .kir/my.sh
	ssh "${host}"
}

0script_exe RcK8.sh
0script_exe RcHelm.sh
0script_exe RcMisc.sh
0script_exe RcUpf.sh

#source ${MY_BASH_DIR}/RcNet
#source ${MY_BASH_DIR}/RcIp
#source ${MY_BASH_DIR}/RcSs
#source ${MY_BASH_DIR}/RcOvs
#source ${MY_BASH_DIR}/RcSsh
#source ${MY_BASH_DIR}/RcTcpdump
#source ${MY_BASH_DIR}/RcRepo
#source ${MY_BASH_DIR}/RcPython
#source ${MY_BASH_DIR}/RcC++.sh
#source ${MY_BASH_DIR}/RcOpenstack
#source ${MY_BASH_DIR}/RcVirsh
#source ${MY_BASH_DIR}/RcOvz
#source ${MY_BASH_DIR}/RcKernel
#source ${MY_BASH_DIR}/RcAfs
#source ${MY_BASH_DIR}/RcDocker


# kk_add_line_once "[ -f ${MY_BASH_DIR}/bash ] && . ${MY_BASH_DIR}/bash" ~/.bashrc
# [[ -f /etc/bash_completion ]] && . /etc/bash_completion
