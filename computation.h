#include "thread_pool.h"
#include "stdlib.h"
#include "pthread.h"

typedef void (*OnComputationComplete)(void*);
struct Computation{
void (*f)(void*);
void *args;
pthread_mutex_t mutex;
pthread_cond_t cond;
Task comp_task;
bool is_completed;

OnComputationComplete comp_on_complete;
void* comp_on_complete_args;
};
void submit_computation(struct ThreadPool *pool, struct Computation *computation, OnComputationComplete on_complete, void* on_complete_arg);
void thpool_complete_computation(struct Computation *computation);
void thpool_wait_computation(struct Computation *computation);
