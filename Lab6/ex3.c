#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct {
    char* name;
    int* grades;
    int count;
} Student;

Student* new_student(const char* name, int grades[], int n) {
    Student* s = malloc(sizeof(Student));
    
    // BUG 1: Not allocating enough space for the null terminator (+1)
    s->name = malloc(strlen(name) + 1); 
    strcpy(s->name, name);
    
    s->grades = malloc(n * sizeof(int));
    memcpy(s->grades, grades, n * sizeof(int));
    s->count = n;
    return s;
}

float average(Student* s) {
    int sum = 0;
    // BUG 2: Out of bounds access. Should be i < s->count, not <=
    for (int i = 0; i < s->count; i++) { 
        sum += s->grades[i];
    }
    return (float)sum / s->count;
}

void free_student(Student* s) {
    free(s->name);
    // BUG 3: Memory leak! The grades array was never freed.
    free(s->grades); 
    free(s);
}

int main() {
    int grades[] = {85, 90, 78, 92};
    Student* alice = new_student("Alice", grades, 4);
    printf("%s: avg = %.1f\n", alice->name, average(alice));
    free_student(alice);
    return 0;
}