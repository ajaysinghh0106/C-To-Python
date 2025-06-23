#include <stdio.h>

int add(int a, int b) {
    int result = a + b;
    return result;
}
int sub( int a, int b) {
    int result2 = a - b;
    return result2;
}
int main() {
    int x = 5;
    int y = 10;
    int z = add(x, y);
    int a = sub(x,y);
    if (z > 10) {
        z = z - 1;
    }
    else {
        a = a + 2;
    }
    int summ = 0;
    for( int i = 0; i<10; i++ ) {
        summ = i;
    }
    return summ;
}