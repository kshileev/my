function kklog()
{
    local log_file=$1
    local log_regex=$2
    local minutes=$3
    sed -n "/^$(date +%Y-%m-%d\ %H:%M --date="$minutes min ago")/, /^$(date +%Y-%m-%d\ %H:%M)/p" "$log_file" | grep -i "$log_regex"
}

function kksystem
{ # we're running on deb based or rpm based OS?
  local deb=/etc/debian_version
  local rpm=/etc/redhat-release
  [ -f ${deb} ] && { echo -n "It's DEBIAN version: " ; cat ${deb}; return 1; }
  [ -f ${rpm} ] && { echo -n "It's RPM version: "    ; cat ${rpm}; return 2; }
}
function kkrepo()
{
  local repo
  repo=$(_get_input 'os-sqe rally devstack tempest cisco-networking cisco-kloudbuster barracuda ovzctl ovzkernel')
  case ${repo} in
	  rally) git clone https://git.openstack.org/openstack/rally;;
	  devstack) git clone https://github.com/openstack-dev/devstack.git;;
	  tempest) git clone https://github.com/openstack/tempest.git;;
	  os-sqe) git clone https://github.com/CiscoSystems/os-sqe.git sqe;;
	  cisco-nvfbench) git clone http://gitlab.cisco.com/openstack-perf/nfvbench.git;;
	  cisco-kloudbuster) https://github.com/openstack/kloudbuster.git kloud;;
    cisco-networking) https://git.openstack.org/openstack/networking-cisco netcis;;
	  ovzctl) git clone git://git.openvz.org/pub/vzctl "$HOME"/vz/ovzctl ;;
	  ovzkernel) git clone  git://git.openvz.org/pub/linux-2.6.18-openvz "$HOME"/vz/18-ovz ;;
	  my) git clone git@github.com:kshileev/my.git ;;
  esac
}
function kkelk()
{
    local cmd=$(_get_input 'index indexR docker')
    case ${cmd} in
        index)
            curl -XGET 'localhost:9200/_cat/indices?v&pretty'

            # curl -H "Content-Type: application/json" -XPOST 'localhost:9200/resultnfvbench-2017.10.18/_bulk?pretty&refresh' --data-binary "@resultnfvbench-2017.10.18.json"
        ;;
        indexR)
            curl -XGET 'mgm.foxberry:9200/_cat/indices?v&pretty'
        ;;
        docker)
            docker run -d -p 9200:9200 -p 9300:9300 -it -h elasticsearch --name elasticsearch docker.elastic.co/elasticsearch/elasticsearch:6.0.0
            docker run -d -p 5601:5601 -h kibana --name kibana --link elasticsearch:elasticsearch -v "$HOME":/data docker.elastic.co/kibana/kibana:6.0.0
            # docker run -d -p 9500:9500 -h logstash --name logstash --link $name:$name --rm -v "$HOME":/data logstash -f /data/repo/my/logstash.conf
        ;;
    esac
}
function kkps()
{
    local name=$1
    local pid=$2
    ps -C "${name}" -o user,pid,ppid,cmd
    [[ -n ${pid} ]] && ps -p "${pid}" -o user,pid,ppid,cmd
}
function kkinfo(){   # shows useful info about unknown command provided as argument
    local cmd_name=$1
    local cmd_full_path
    cmd_full_path=$(which "${cmd_name}")
    file "${cmd_full_path}"
    dpkg -S "${cmd_full_path}"
}
function kkmorze()
{
cat <<EOF
01 Aa ._   alfa     А   01 А .-    ай-даа            A    01      alpha
02 Bb -... bravo    Б   02 Б -...  баа-ки-те-кут     B    02      beta
03 Cc -.-. charlie  Ц   03 В  .--  ви-даа-лаа        W    03      gamma
04 Dd -..  delta    Д   04 Г  --.  гоо-воо-ри        G    04      delta
05 Ee .    echo     Е   05 Д  -..  доо-ми-ки         D    05      epsilon
06 Ff ..-. foxtrot  Ф   06 Е  .    есть              E    06      zeta
07 Gg --.  golf     Г   07 Ё                              07      eta
08 Hh .... hotel    Х   08 Ж  ...- жи-ви-те-стоо     V    08      theta
09 Ii ..   india    И   09 З  --.. заа-каа-ти-ки     Z    09      iota
10 Jj .--- juliett  Й   10 И  ..   и-ди              I    10      kappa
11 Kk -.-  kilo     К   11 Й  .--- ку-даа-поо-шлаа   J    11      lambda
12 Ll .-.. lima     Л   12 К  -.-  каак-де-лаа       K    12      mu
13 Mm --   mike     М   13 Л  .-.. лу-наа-ти-ки      L    13      nu
14 Nn -.   november Н   14 М  --   маа-маа           M    14      xi
15 Oo ---  oskar    О   15 Н  -.   ноо-мер           N    15      omicron
16 Pp .--. papa     П   16 О  ---  оо-коо-лоо        O    16      pi
17 Qq --.- quebec   Щ   17 П  .--. пи-лаа-поо-ёт     P    17      rho
18 Rr .-.  romeo    Р   18 Р  .-.  ре-шаа-ет         R    18      sigma
19 Ss ...  sierra   С   19 С  ...  са-мо-лёт         S    19      tau
20 Tt -    tango    Т   20 Т  -    таак              T    20      upsilon
21 Uu ..-  uniform  У   21 У  ..-  у-нес-лаа         U    21      fi
22 Vv ...- victor   Ж   22 Ф  ..-. фи-ли-моон-чик    F    22      chi
23 Ww .--  whiskey  В   23 Х  .... хи-ми-чи-те       H    23      psi
24 Xx -..- x-ray    Ь   24 Ц  -.-. цаа-пли-цаа-пли   C    24      omega
25 Yy -.-- yankee   Ы   25 Ч
26 Zz --.. zulu     З   26 Ы  -.-- ыы-не-наа-доо     Y
                        27 Ш  ---- шаа-роо-ваа-рыы
                        28 Щ  --.- щаа-ваам-не-шаа   Q
                        29 Ь  -..- тоо-мяг-кий-знаак X
                        30 Ъ
                        31 Э  ..-..э-ле-роон-чи-ки
                        32 Ю  ..-- ю-ли-аа-наа
                        33 Я  .-.- я-маал-я-маал
EOF
}
function kkhex
{
    cat <<EOF
 hex table:
 0 0x0 0000
 1 0x1 0001
 2 0x2 0010
 3 0x3 0011
 4 0x4 0100
 5 0x5 0101
 6 0x6 0110
 7 0x7 0111
 8 0x8 1000
 9 0x9 1001
10 0xa 1010
11 0xb 1011
12 0xc 1100
13 0xd 1101
14 0xe 1110
15 0xf 1111
EOF
}
