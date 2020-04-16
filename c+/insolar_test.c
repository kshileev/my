/*
gcc test.c -o test

$ nc 127.0.0.1 8080
Your name, please?
Alex
Hi, Alex!
*/

#include <errno.h>
#include <string.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <arpa/inet.h>
#include <netinet/in.h>
#include <sys/socket.h>
#include <sys/types.h>

void err(char* err_fun) {
  printf("%s %d", err_fun, errno);
  exit(1);
}

void chld(int sock) {
  size_t nl;
  char m[] = "Your name, please?\n";
  char n[256];
  char f[256];
  write(sock, m, sizeof(m));
  nl = read(sock, n, sizeof(n));
  if(-1 == nl) {
    err("read");
  }
  while(nl > 0 &&
      ( '\n' == n[nl-1]  ||
        '\r' == n[nl-1])) {
    nl--;
  }
  n[nl] = 0;
  sprintf(f, "Hi, %s!\n", n);
  write(sock, f, strlen(f));
  close(sock);
  exit(0);
}

int main() {
  struct sockaddr_in addr;
  int sckt;
  int pid;
  int lstn = socket(AF_INET, SOCK_STREAM, 0);
  if(-1 == lstn) {
    err("socket");
  }

  addr.sin_family = AF_INET;
  addr.sin_port = htons(8080);
  addr.sin_addr.s_addr = inet_addr("127.0.0.1");
  if(-1 == bind(lstn, (struct sockaddr*)&addr, sizeof(addr))){
    err("bind");
  }

  if(-1 == listen(lstn, 100)) {
    err("listen");
  }

  for(;;) {
    sckt = accept(lstn, 0, 0);
    if(-1 == sckt) {
      err("accept");
    }

    pid = fork();
    if(-1 == pid) {
      err("fork");
    } else if(0 == pid) {
      close(lstn);
      chld(sckt);
    } else {
      close(sckt);
    }
  }
  exit(0);
}