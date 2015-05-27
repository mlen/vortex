#include <stdlib.h>
#include <unistd.h>

int main(int argc, char **argv) {
    if (argc != 3) {
        exit(1);
    }

    char *argp[] = { NULL };
    char *envp[] = { "", "", argv[2], NULL };
    execve(argv[1], argp, envp);
}
