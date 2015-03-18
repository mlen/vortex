#include <stdlib.h>
#include <unistd.h>

int main(int argc, char **argv) {
    if (argc < 4) {
        exit(1);
    }

    char *argp[] = { NULL };
    char *envp[] = { "a", "b", argv[3], argv[2], NULL };
    execve(argv[1], argp, envp);
}
