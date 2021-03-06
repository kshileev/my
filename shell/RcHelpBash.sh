function kkhelp-docker(){
    _section docker
    echo 'list all running ctn:  docker ps'
    echo 'inspect container   :  docker inspect name_or_id'
}
function kkhelp-vim()
{
    _section vim
    echo 'vim "+e ++enc=utf8"'   with russian support cp1251 utf8  koi8r cp866
    echo 'gf <C-w>f <C-w>gf'     open file under cursor
    echo '<C-]> <C-T> <C-O>'     go forth and back
    echo ':%s/patter/string/cg'  substitute
    echo ':e file_name'		 edit file
    echo 'vim -c :10d'           delete line 10
    echo '$'			 to end of line
}
function kkhelp_if_then()
{
    if [ ! -z "$CENTRAL_SETUP_for_UPLOAD" ]; then
        local_setup=$CENTRAL_SETUP_for_UPLOAD
        mv CENTRAL_SETUP_for_UPLOAD $local_setup
    elif [ ! -z "$CENTRAL_SETUP_in_REPO" ]; then
        if [ ! -d /tmp/mercury_repo ]; then
            git clone https://cloud-review.cisco.com/mercury/mercury /tmp/mercury_repo
        fi
        cd /tmp/mercury_repo
        git pull
        cd -
        cp /tmp/mercury_repo/testbeds/$CENTRAL_SETUP_in_REPO .
        local_setup=$(echo $CENTRAL_SETUP_in_REPO | cut -d '/' -f2)
    else
        error No central setup specified
    fi
}
function kkhelp-bash()
{
    echo 'virsh list | grep running | cut -d " " -f2,7 | while read id; do [ -n "$id" ] && echo virsh save $id.save; done'
    echo 'while grep resync /proc/mdstat; do echo resync in file; sleep 5; done	# while ("string resync" in file'

    local help_cmd=$(_get_input 'file_path file_status for_loop if1 if2 if3 while_loop substring_in_string inifinite_loop')
    case ${help_cmd} in
         file_path)
            echo '$(dirname /a/b/c) produces:' "$(dirname /a/b/c)"
            echo '$(basename /a/b/c) produces:' "$(basename /a/b/c)"
	     ;;
	     file_status)
            echo '[[ -n ~/.bashrc ]] && echo not empty produces:'
            [[ -n ~/.bashrc ]] && echo not empty
	     ;;
	     "if1")
            echo 'git status && echo in repo || echo out of repo produces:'
            git status && echo in repo || echo out of repo
          ;;
	     'if2')
            echo 'if [ -z $Host ]; then echo ok; fi' produces $(if [ -z $Host ]; then echo ok; fi)
          ;;
	     'if3')
            echo '[ "$HOTNAME" == "false" ] && echo ok $HOSTNAME || echo noc $HOTNAME' produces [ "$HOSTNAME" == "false" ] && echo ok $HOSTNAME || echo noc $HOSTNAME
          ;;
         while_loop)
            echo 'ls | while read x; do echo element $x; done produces:'
            ls | while read x; do echo element $x; done
          ;;
	     for_loop)
            echo 'for _ in "p 1" "p 2"; do echo $_ ; done produces:'
            for _ in "p 1" "p 2"; do echo $_ ; done
	     ;;
         inifinite_loop)
            echo 'while true ; do echo 123 ; done produces infinite loop (WARNING)'
            while true ; do echo 123 ; done
         ;;
         substring_in_string)
             echo '[[ 'This is super text' == *super* ]] && echo text contains super produces:'
             [[ 'This is super text' == *super* ]] && echo text contains super
         ;;
    esac
}
function kkhelp-grep()
{
    _section grep
    echo 'find bar foe -name *.c[              # how to find all *.c and *. in ~ bar and foe dirs'
    echo 'grep -A 2 -B 3 -E "foo|bar" file     # how to grep foo or bar and print 2 lines before and 3 lines after in file file'
    echo 'grep -RE "foo|bar" dir --include pat # how to grep foo or bar recursevely in dir for files p'
}
function kkhelp-grub()
{
    _section grub
    echo 'savedefault --default=1 --once | grub' #say grub to reboot once
    echo 'kernel XXXX ro root=LABEL=/ debug oops=panic panic=1 console=ttyS0,115200 console=tty > /boot/grub/menu.lst' #reboot if panic
}
function kkhelp-cscope()
{
    _section cscope
    echo cscope -b -R          # build reference file
    echo cscope -b -q -k       # used
}
function kkhelp-rmp-dpkg()
{
    _section packages
    echo 'list all packages  rpm -qa                   dpkg -l'
    echo 'list files         rpm -ql name              dpkg -L name'
    echo 'show info          rpm -qi name              dpkg -s name'
    echo 'who owns the file  rpm -qf file              dpkg -S file'
    echo 'show scripts       rpm -q --scripts name     cat /var/lib/dpkg/info name.xxx'
    echo 'install package    rpm -ivh name             dpkg --force-architecture -i name'
    echo 'verify package     rpm -V name               dpkg -V name'
    echo 'key install        rpm --import key'
    echo 'show key ring      rpm -qa gpg-pubkey*'
}
function kkhelp-kernel()
{
    _section kernel
    echo 'syscall:	check include/asm/unistd.h for __NR_syscallname'
}
function kkhelp-mount()
{
    _section mount
    echo mount -o rw,remount /dev/sda1
}
function kkhelp-ps()
{
    _section ps
    echo ps -L -p pid # shows all threads for process
}
function kkhelp-diff()
{
    _section diff
    echo diff -pNU7 # p for function N
}
function kkhelp-watch()
{
    _section watch
    echo watch -d -n 5 ip a    # re-run ip a every 5 secs and highlight difference
}
function 9help() {
    local help_cmd=$(_get_input 'my.sh os ps grep rmp-dpkg cscope kernel mount')
    case ${help_cmd} in
         my.sh) kkhelp-bash ;;
         os) kkhelp-os ;;
         grep) kkhelp-grep ;;
    esac
}

echo $BASH_SOURCE loaded