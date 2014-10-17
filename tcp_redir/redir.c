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

int server_run(short iport, short oport) {

    int issock; /* input server socket */
    int ossock; /* output server socket */
    struct clients *icli = NULL; /* input client list */
    struct clients *ocli = NULL; /* output client list */
    struct clients *tmp = NULL;
    struct clients *tmp2 = NULL;
    struct sockaddr_in isin;
    struct sockaddr_in osin;
    char buffer[BUFF_SIZE] = {0};
    fd_set rfd;
    int max, maxtmp, ret;

    /* Socket creation */
    issock = socket(AF_INET, SOCK_STREAM, 0);
    ossock = socket(AF_INET, SOCK_STREAM, 0);
    if (issock == 0 || ossock == 0) {
        perror("socket");
        return -1;
    }

    isin.sin_family = AF_INET;
    isin.sin_port = htons(iport);
    isin.sin_addr.s_addr = htonl(INADDR_ANY);
    osin.sin_family = AF_INET;
    osin.sin_port = htons(oport);
    osin.sin_addr.s_addr = htonl(INADDR_ANY);
    
    if (bind(issock, (struct sockaddr *)&isin, sizeof(isin)) == -1 ||
        bind(ossock, (struct sockaddr *)&osin, sizeof(osin)) == -1) {
        perror("bind");
        return -1;
    }
    if (listen(issock, BACKLOG) != 0 ||
        listen(ossock, BACKLOG) != 0) {
        perror("listen");
        return -1;
    }

    while (run) {

        /* Select initialization */
        FD_ZERO(&rfd);
        FD_SET(issock, &rfd);
        FD_SET(ossock, &rfd);
        max = set_fds(icli, &rfd);
        maxtmp = set_fds(ocli, &rfd);
        max = (maxtmp > max) ? maxtmp : max;
        if (issock > max)
            max = issock;
        if (ossock > max)
            max = ossock;

        /* Select */
        if ((select(max + 1, &rfd, NULL, NULL, NULL)) == -1) {
            perror("select");
        }

        /* Check fds */
        if (FD_ISSET(issock, &rfd) != 0) 
            add_node(issock, &icli); 
        if (FD_ISSET(ossock, &rfd) != 0) 
           add_node(ossock, &ocli);

        /* remove output clients that have closed their connexions */
        tmp = ocli;
        while (tmp) {
            if (FD_ISSET(tmp->_fd, &rfd) != 0) {
                ret = read(tmp->_fd, buffer, 1);
                if (ret == 0)
                    rm_node(&ocli, tmp);
            }
            tmp = tmp->_next;
        }

        /* copy input to output */
        tmp = icli;
        while (tmp) {
            if (FD_ISSET(tmp->_fd, &rfd) != 0) {
                tmp2 = ocli;
                ret = read(tmp->_fd, buffer, sizeof(buffer));
                if (ret <= 0) {
                   rm_node(&icli, tmp);
                }
                while (tmp2) {
                    write(tmp2->_fd, buffer, ret);
                    tmp2 = tmp2->_next;
                }
            }
            tmp = tmp->_next;
        }
    }

    free_list(icli);
    free_list(ocli);
    return 0;
}

int main(int argc, char *argv[]) {

    short iport, oport;

    if (argc != 3) {
        fprintf(stderr, "Usage: %s iport oport\n", *argv);
        fprintf(stderr, "\tiport\tthe port to listen input\n");
        fprintf(stderr, "\toport\tthe port for output stream\n");
        return 1;
    }    

    iport = atoi(argv[1]);
    oport = atoi(argv[2]);
    signal(SIGINT, &siginthdlr);
    if (server_run(iport, oport) == -1)
        return 1;
    return 0;
}
