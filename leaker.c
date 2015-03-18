#include <stdio.h>
int main(int argc, char **argv) {
    if (argc) return 1;
    printf("%08x", argv[4]);
    return 0;
}
