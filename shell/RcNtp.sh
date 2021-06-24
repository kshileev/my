function kkntp
{
    echo Creating ntp config in /etc/ntp.conf
    cat > /etc/ntp.conf <<EOF
driftfile /var/lib/ntp/drift

restrict default kod nomodify notrap nopeer noquery
restrict -6 default kod nomodify notrap nopeer noquery

restrict 127.0.0.1
restrict -6 ::1

server dn11.kirshil.ru

includefile /etc/ntp/crypto/pw

keys /etc/ntp/keys
EOF
}