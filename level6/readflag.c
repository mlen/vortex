#include <stdlib.h>
#include <stdio.h>
#include <unistd.h>

int main() {
    int c;
    FILE *f;

    f = fopen("/etc/vortex_pass/vortex7", "r");
    while ((c = fgetc(f)) != EOF) putchar(c);
    fclose(f);

    return 0;
}
