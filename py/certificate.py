import os.path

cert_folder_path = os.path.expanduser('~/cert')
cert_name = 'kirill.private.me'

cmds = [f'mkdir -p {cert_folder_path}',
        f'cd {cert_folder_path}',
        f'openssl genrsa -out for_req_cert.key 2048',
        f'openssl req -new -key for_req_cert.key -out req_of_cert.csr -subj "/C=RU/ST=MSK/L=Moscow/O=My Private Inc./CN={cert_name}"',
        f'openssl genrsa -out for_sign_cert.key 2048',
        f'openssl x509 -req -days 365 -in req_of_cert.csr -signkey for_sign_cert.key -text -out {cert_name}.cer',
        f'ls {cert_folder_path}',
        f'cat {cert_folder_path}/{cert_name}.cer'
        ]

print(cmds)

os.system(' && '.join(cmds))
# os.system('cp -f {cert_dir}/{reg_name}.cer /etc/pki/ca-trust/source/anchors/ca.crt'.format(cert_dir=cert_dir, reg_name=reg_name))
# os.system('cp -f {cert_dir}/{reg_name}.cer /etc/docker/certs.d/{reg_name}/ca.crt'.format(cert_dir=cert_dir, reg_name=reg_name))
# os.system('update-ca-trust extract')
