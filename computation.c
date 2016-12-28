#include "computation.h"
#include "thread_pool.h"
#include "stdio.h"
#include "stdlib.h"
    
void thpool_submit_computation(struct ThreadPool *pool, struct Computation *computation, OnComputationComplete on_complete, void* on_complete_args){
	computation->comp_task.f = computation->f;
	computation->comp_task.arg = computation->args;
	computation->comp_on_complete = on_complete;
	computation->comp_on_complete_args = on_complete_args;

	pthread_mutex_init(&computation->mutex, NULL);
	pthread_cond_init(&computation->cond, NULL);
	thpool_submit(pool, &computation->comp_task);
}

void thpool_wait_computation(struct Computation *computation){

	pthread_mutex_lock(&computation->mutex);
	while(!computation->is_completed)
		pthread_cond_wait(&computation->cond, &computation->mutex);
	pthread_mutex_unlock(&computation->mutex);
	pthread_mutex_destroy(&computation->mutex);
	pthread_cond_destroy(&computation->cond);
	thpool_wait(&computation->comp_task);
}

void thpool_complete_computation(struct Computation *computation){
    pthread_mutex_lock(&computation->mutex);
	if(computation->comp_on_complete)
		computation->comp_on_complete(computation->comp_on_complete_args);
	pthread_mutex_unlock(&computation->mutex);
	pthread_cond_signal(&computation->cond);
	computation->is_completed = true;
}
