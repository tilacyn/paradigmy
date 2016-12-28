#ifndef __COMPUTATION_H__
#define __COMPUTATION_H__

#include "thread_pool.h"
#include <stdlib.h>
#include <pthread.h>

typedef void (*OnComputationComplete)(void*);
struct Computation{
	void (*f)(void*);
	void *arg;
	pthread_mutex_t mutex;
	pthread_cond_t cond;
	struct Task task;
	bool is_completed;

	OnComputationComplete on_complete;
	void* on_complete_args;
};
void thpool_submit_computation(struct ThreadPool *pool, struct Computation *computation, OnComputationComplete on_complete, void* on_complete_arg);
void thpool_complete_computation(struct Computation *computation);
void thpool_wait_computation(struct Computation *computation);

#endif
