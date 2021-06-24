export MY_CSCOPE_DIR=${MY_TMP_DIR}/cscope		#tmp dir where cscope stores the output
export MY_CSCOPE_FILE_LIST=${MY_CSCOPE_DIR}/cscope.files	#file to list files to browse into db
export DISTCC_HOSTS='1.1.1.1 2.2.2.2 3.3.3.3'	#used by make -j
export ARTISTIC_STYLE_OPTIONS=${MY_DIR}/RcAstyle

alias fk="find . -name \"*.${USER}\""
alias grc='find . -name "*.[ch]pp" -o -name "*.[ch]" | xargs grep'
alias gdi="gendiff . .${USER} > ~/${MY_USER}.diff-xx-xxxx-`date +%Y%m%d`"
alias pt="patch -p1 -b -z .${USER}"
alias   0m64='make -j32 CC=distcc ARCH=x86_64'
alias   0mod="gcc -c -Wall -nostdinc -I/usr/src/linux/include"

function kkscope
{
    local what=$(_get_input 'devstack c-proj')
    echo Preparing CSCOPE to browse in $PWD
    mkdir -p ${MY_CSCOPE_DIR}
    case ${what} in
	devstack) find ${PWD} -name stack.sh -o -name functions -o -name neutron > ${MY_CSCOPE_FILE_LIST} && cd ${MY_CSCOPE_DIR} && cscope -b -q && cd -
	    ;;
	c-proj)   find ${PWD} -name "*.[ch]" -o -name "*.[ch]pp" | grep -v ut/ | grep -v utils/ > ${MY_CSCOPE_FILE_LIST} && cd ${MY_CSCOPE_DIR} && cscope -b -q -k && cd -
	    cscope -b -q -k
	    ;;
    esac
}
function kkdiff
{
    local diff_name=~/kshileev.diff.`date +%Y%m%d`
    local origs=`find . -name "*.kshileev"`
    rm -f $diff_name
    for orig in $origs ; do
        diff -uN $orig ${orig%.kshileev} >> $diff_name
    done
    echo see $diff_name
}
function kksizeof
{
	if [ "$#" == "0" ]; then
		echo Usage: $0 c1i1
		return
	fi

	for c in $1 ;  do
		echo ${c}
	done

	Class="class Class{char c; int i;};" #

	local TmpCode=$(mktemp -u).c++ #tmp file of type /tmp/tmp.XXXXXXXX.c++ -u: don't create it (unsafe)
	local TmpBin=${TmpCode/c++/exe}

	cat > ${TmpCode} <<EOF
#include <iostream>
using namespace std;

${Class}

int main()
{
	Class obj;
	cout<<"${Class} CLS="<<sizeof(Class)<<" obj="<<sizeof(obj)<<endl;
	return 0;
}
EOF

	g++ ${TmpCode} -o ${TmpBin}
	echo Platform `uname -m`
	${TmpBin}
	rm ${TmpCode} ${TmpBin}
}
function kkclass
{
    local Class=$(ksGetInput 'Class name' 'KirClass')
    local Base=$(ksGetInput 'Base name' 'KirBase')
    local Ext=$(ksGetInput 'C++ extention' '.c++')
    File=${Class}${Ext}
    Header=${Class}.h

    cat > ${Header} <<EOF
#ifndef ${Class}_h"
#define ${Class}_h"

#include <$Base.h>

class ${Class} : public ${Base}
{
public:
    ${Class}();
   ~${Class}();
protected:
  ClassDef(${Class},0)
};//class ${Class}
#endif//${Class}_h
EOF

	cat > ${File} << EOF
#include \"$Header\""             >>$File;                       echo >>$File
ClassImp(${Class})"                 >>${File};                       echo >>${File}
//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++" >>${File}
${Class}::${Class}()"                 >>${File}
{//ctor
  PrintDebugStart(\"ctor\");"     >>${File}
  PrintDebugStop(\"ctor\");"      >>${File}
  return;"                        >>${File}
}
//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
${Class}::~${Class}()
{//dtor
  PrintDebugStart("dtor");
  PrintDebugStop("dtor");
  return;
}
EOF
}
function kkgrepc
{
    [ -z "$1" ] && echo Usage $FUNCNAME symbol || echo $1 a\is in :
    find . -name *.[ch]pp | xargs grep $1
}
