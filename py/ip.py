def is_valid_ipv4(ip):
    import socket

    if not ip:
        return False
    if ip.count('.') != 4:
        return False
    try:
        socket.inet_aton(ip)
        return True
    except socket.error:
        return False

if __name__ == '__main__':
    is_valid_ipv4('10.101.0.11')
