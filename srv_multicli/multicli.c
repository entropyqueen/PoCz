#include <stdio.h>
#include <stdlib.h>
#include <signal.h>
#include <string.h>
#include <unistd.h>
#include <sys/select.h>
#include <sys/socket.h>
#include <arpa/inet.h>

#define BUFF_SIZE 4096
#define BACKLOG 20

struct clients {
    int _fd;
    struct clients *_next;
};

static int run = 1;

void siginthdlr(int __attribute__((unused)) sig) {
    run = 0;
}

int set_fds(struct clients *cli, fd_set *rfd) {

    struct clients *tmp = cli;
    int max = 0;

    while (tmp != NULL) {
        if (tmp->_fd > max)
            max = tmp->_fd;
        FD_SET(tmp->_fd, rfd);
        tmp = tmp->_next;
    }
    return max;
}

int add_node(int sock, struct clients **list) {
 
    struct clients *node = NULL;

    node = malloc(sizeof(*node));
    if (node == NULL)
        return -1;
    node->_fd = accept(sock, NULL, NULL);

    node->_next = NULL;
    if (*list)
        node->_next = *list;
    *list = node;
    return 0;
}

/* because lazy to do better */
void rm_node(struct clients **cli, struct clients *node) {

    struct clients *tmp = *cli;   

    close(node->_fd);
    if (node == *cli) {
        *cli = node->_next;
        free(node);
        return;
    }

    while (tmp && tmp->_next != node) {
        tmp = tmp->_next;
    }
    tmp->_next = node->_next;
    free(node);
}

void free_list(struct clients *lst) {
    if (lst->_next)
        free_list(lst->_next);
    free(lst);
}

int server_run(short port) {

    int ssock;
    struct clients *cli = NULL;
    struct clients *tmp = NULL;
    struct sockaddr_in ssin;
    char buffer[BUFF_SIZE] = {0};
    fd_set rfd;
    int max, ret;

    ssock = socket(AF_INET, SOCK_STREAM, 0);
    if (ssock == 0) {
        perror("socket");
        return -1;
    }

    ssin.sin_family = AF_INET;
    ssin.sin_port = htons(port);
    ssin.sin_addr.s_addr = htonl(INADDR_ANY);

    if (bind(ssock, (struct sockaddr *)&ssin, sizeof(ssin)) == -1) {
        perror("bind");
        return -1;
    }
    if (listen(ssock, BACKLOG) != 0) {
        perror("listen");
        return -1;
    }

    while (run) {

        /* Select initialization */
        FD_ZERO(&rfd);
        FD_SET(ssock, &rfd);
        FD_SET(0, &rfd); /* fd for read on stdin */
        max = set_fds(cli, &rfd);
        if (ssock > max)
            max = ssock;

        /* Select */
        if ((select(max + 1, &rfd, NULL, NULL, NULL)) == -1) {
            perror("select");
        }

        /* Check fds */
        if (FD_ISSET(ssock, &rfd) != 0) 
            add_node(ssock, &cli); 

        if (FD_ISSET(0, &rfd) != 0) {
            ret = read(0, buffer, sizeof(buffer));
            if (ret < 0)
                perror("read");
            else if (ret == 0) 
                run = 0;
            tmp = cli;
            while (tmp) {
                write(tmp->_fd, buffer, ret);
                tmp = tmp->_next;
            }
        }

       /* copy input to output */
        tmp = cli;
        while (tmp) {
            if (FD_ISSET(tmp->_fd, &rfd) != 0) {
                ret = read(tmp->_fd, buffer, sizeof(buffer));
                if (ret <= 0) {
                   rm_node(&cli, tmp);
                   continue;
                }
                write(1, buffer, ret);
            }
            tmp = tmp->_next;
        }
    }
    close(ssock);
    free_list(cli);
    return 0;
}

int main(int argc, char *argv[]) {

    short port;

    if (argc != 2) {
        fprintf(stderr, "Usage: %s port\n", *argv);
        return 1;
    }    

    port = atoi(argv[1]);
    signal(SIGINT, &siginthdlr);
    if (server_run(port) == -1)
        return 1;
    return 0;
}
