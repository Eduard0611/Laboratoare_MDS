#include <stdio.h>
#include <pthread.h>
#include <stdatomic.h>

// Use an atomic integer
_Atomic int counter = 0; 

void* increment_loop(void* arg) {
    for (int i = 0; i < 100000; i++) {
        counter++; // Now atomic and thread-safe!
    }
    return NULL;
}

int main() {
    pthread_t t1, t2;
    pthread_create(&t1, NULL, increment_loop, NULL);
    pthread_create(&t2, NULL, increment_loop, NULL);
    pthread_join(t1, NULL);
    pthread_join(t2, NULL);
    
    printf("Final counter value (Expected 200000): %d\n", counter);
    return 0;
}