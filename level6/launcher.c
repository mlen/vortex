#include <stdlib.h>
#include <unistd.h>

int main(int argc, char **argv) {
    if (argc != 3) {
        exit(1);
    }

    char *argp[] = { argv[2], NULL };
    char *envp[] = { "", NULL };
    execve(argv[1], argp, envp);
}
