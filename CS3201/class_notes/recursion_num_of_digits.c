#include <stdio.h>

int countDigits(int n) {
    int sum = 0;	
    if (n == 0) return 0;
    sum += 1 + countDigits(n / 10);
    return sum;
}

int main() {
    int n = 123456;
    printf("Number of digits in %d is: %d\n", n, countDigits(n));
    return 0;
}

