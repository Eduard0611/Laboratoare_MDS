#define OPENSSL_SUPPRESS_DEPRECATED
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <pthread.h>
#include <openssl/sha.h>

#define ITERS 2000000

const char* files[4] = {"a.html", "b.html", "c.html", "d.html"};
unsigned long results[4];

unsigned long stretch_hash(const char* path) {
    FILE* f = fopen(path, "r");
    if (!f) { perror("Failed to open file"); exit(1); }
    
    fseek(f, 0, SEEK_END);
    long sz = ftell(f);
    fseek(f, 0, SEEK_SET);
    
    unsigned char* buf = malloc(sz);
    fread(buf, 1, sz, f);
    fclose(f);
    
    unsigned char digest[32];
    SHA256_CTX ctx;
    SHA256_Init(&ctx);
    SHA256_Update(&ctx, buf, sz);
    SHA256_Final(digest, &ctx);
    free(buf);
    
    for (int i = 0; i < ITERS; i++) {
        SHA256_Init(&ctx);
        SHA256_Update(&ctx, digest, 32);
        SHA256_Final(digest, &ctx);
    }
    
    unsigned long sum = 0;
    for (int i = 0; i < 32; i++) sum += digest[i];
    return sum;
}

// Thread routine: the argument is an integer representing the file index (0 to 3)
void* thread_routine(void* arg) {
    int file_idx = *(int*)arg;
    results[file_idx] = stretch_hash(files[file_idx]);
    return NULL;
}

int main(int argc, char** argv) {
    int use_threads = 0;
    
    // Simple way to choose mode: pass "threads" as argument
    if (argc > 1 && strcmp(argv[1], "threads") == 0) {
        use_threads = 1;
    }

    if (!use_threads) {
        // SINGLE-THREADED VERSION
        for (int i = 0; i < 4; i++) {
            results[i] = stretch_hash(files[i]);
        }
    } else {
        // MULTI-THREADED VERSION
        pthread_t threads[4];
        int ids[4] = {0, 1, 2, 3}; // We must pass distinct memory locations to each thread
        
        for (int i = 0; i < 4; i++) {
            pthread_create(&threads[i], NULL, thread_routine, &ids[i]);
        }
        
        for (int i = 0; i < 4; i++) {
            pthread_join(threads[i], NULL);
        }
    }

    // Print results to verify correctness
    for(int i=0; i<4; i++){
        printf("%s: %lu\n", files[i], results[i]);
    }

    return 0;
}