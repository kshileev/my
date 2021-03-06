ColorNormal="\\033[0;39m"
ColorBlack="\\033[0;30m";     ColorDarkGray="\\033[1;30m"
ColorBlue="\\033[0;34m";      ColorLightBlue="\\033[1;34m"
ColorGreen="\\033[0;32m";     ColorLightGreen="\\033[1;32m"
ColorCyan="\\033[0;36m";      ColorLightCyan="\\033[1;36m"
ColorRed="\\033[0;31m";       ColorLightRed="\\033[1;31m"
ColorPurple="\\033[0;35m";    ColorLightPurple="\\033[1;35m"
ColorBrown="\\033[0;33m";     ColorYellow="\\033[1;33m"
ColorLightGray="\\033[0;37m"; ColorWhite="\\033[1;37m"

setcolor_caption="echo -en \\033[1;34m"
setcolor_success="echo -en \\033[1;32m"
setcolor_failure="echo -en \\033[1;31m"
setcolor_normal="echo -en \\033[0;39m"

_ecount=0
function _e()
{
	_ecount=$((_ecount+1))
	${setcolor_caption}
	echo -n "Phase #$_ecount: $*..."
	${setcolor_normal}
	echo
}
function _eok()
{
	${setcolor_success}
	echo -n "DONE"
	${setcolor_normal}
	echo
}
function _enok()
{
	${setcolor_failure}
	echo -n "FAILED"
	${setcolor_normal}
	echo
}
function _section()
{
    printf "\n%-10s %0100s\n" $1
}
function kk_input_from_list()
{
    local commands=$1
    local command=$2
    [[ -n ${command} ]] && [[ ${commands} == *${command}* ]] && echo ${command} && return
    local default_command=$(echo ${commands} | cut -d ' ' -f1)
    local input
    read -p "choices: ${commands} [default=${default_command}]: " input
    [[ ${commands} != *${input}* ]] && echo Wrong choice: ${input} 1>&2 && return
    echo ${input:-${default_command}}
}
function kk_input_from_exe()
{   # exe command and divide output by space
    local cmd=$*
    local options=`$cmd`
    local default=`echo $options | cut -d " " -f1`
    local input
    read -p "choose from: ${options} [default=${default}]: " input
    [[ ${options} != *${input}* ]] && echo Wrong command ${input} 1>&2 && return
    echo ${input:-${default}}
}
function kk_add_line_once()
{
    local line=$1
    local file=$2
    [ -f ${file} ] || touch ${file}
    grep "${line}" ${file} 1>/dev/null || echo ${line} >> ${file}
}
function kk_exit_no_ping()
{
   ping -c 1 $1 > /dev/null 2>&1
   [ "$?" == "0" ] || { echo Node \"$1\" is off, aborting...; exit 1; }
}
function kk_timestamp()
{
    echo $(TZ='Europe/Moscow' date +%Z%d.%h%H:%M)
}
function cat_files()
{
	local dir=$1
	local files=$2
	for f in ${files}; do
		echo -e "\n$dir/$f:"
		cat ${dir}/${f}
		echo -e "<----\tend\t----"
	done
}
function kk_ssh_config_host(){
    grep -E ^Host ~/.ssh/config | grep -v '*' | cut -f2 -d ' '
}
function kk_os_check(){
    if [[ "$OSTYPE" == "linux-gnu" ]]; then
        lsb_release -a
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        echo MAC
    elif [[ "$OSTYPE" == "cygwin" ]]; then
        echo CYGWIN
    elif [[ "$OSTYPE" == "msys" ]]; then
        echo MSYS
    elif [[ "$OSTYPE" == "freebsd"* ]]; then
        echo BSD
    else
        echo UNKNOWN
    fi
}
echo $BASH_SOURCE loaded