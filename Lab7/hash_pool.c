#define OPENSSL_SUPPRESS_DEPRECATED
#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>
#include <openssl/sha.h>

#define ITERS 2000000

char** file_list;
unsigned long* results;
int num_files;
int num_threads;

// Shared variable to track which file is next
int current_file_idx = 0;
// Mutex to protect the shared variable
pthread_mutex_t lock;

unsigned long stretch_hash(const char* path) {
    // (Same implementation as Exercise 1)
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

void* worker_thread(void* arg) {
    while (1) {
        int my_file_idx;
        
        // --- Critical Section: Getting the next file index ---
        pthread_mutex_lock(&lock);
        my_file_idx = current_file_idx;
        if (current_file_idx < num_files) {
            current_file_idx++;
        }
        pthread_mutex_unlock(&lock);
        // -----------------------------------------------------

        // If no more files are left, this thread is done
        if (my_file_idx >= num_files) {
            break;
        }

        // Process the file outside the lock so other threads aren't blocked
        results[my_file_idx] = stretch_hash(file_list[my_file_idx]);
    }
    return NULL;
}

int main(int argc, char** argv) {
    if (argc < 3) {
        printf("Usage: %s <num_threads> <file1> <file2> ...\n", argv[0]);
        return 1;
    }

    num_threads = atoi(argv[1]);
    num_files = argc - 2;
    file_list = &argv[2];
    
    results = malloc(num_files * sizeof(unsigned long));
    pthread_mutex_init(&lock, NULL);

    pthread_t* threads = malloc(num_threads * sizeof(pthread_t));

    for (int i = 0; i < num_threads; i++) {
        pthread_create(&threads[i], NULL, worker_thread, NULL);
    }

    for (int i = 0; i < num_threads; i++) {
        pthread_join(threads[i], NULL);
    }

    for(int i=0; i<num_files; i++){
        printf("%s: %lu\n", file_list[i], results[i]);
    }

    free(threads);
    free(results);
    pthread_mutex_destroy(&lock);
    return 0;
}