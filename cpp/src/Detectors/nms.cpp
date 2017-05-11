/**
 * Fast non-maximum suppression in C, port from
 * http://quantombone.blogspot.com/2011/08/blazing-fast-nmsm-from-exemplar-svm.html
 *
 * @blackball (bugway@gmail.com)
 */

#include <stdio.h>
#include <stdlib.h>
#include <limits.h>

#import "nms.hpp"



static void
sort_idx(const drect *rects, int *idxes, int n) {
    /* sort indexes descending by scores */
    int i, j;
    for (i = 0; i < n; ++i) {
	for (j = i + 1; j < n; ++j) {
	    int ti = idxes[i], tj = idxes[j];
	    if ( rects[tj].score < rects[ti].score ) {
		idxes[i] = tj;
		idxes[j] = ti;
	    }
	}
    }
}

static int
sort_stable(int *arr, int n) {
    /* stable move all -1 to the end */
    int i = 0, j = 0;

    while (i < n) {
	if (arr[i] == -1) {
	    if (j  < i+1)
		j = i+1;
	    while (j < n) {
		if (arr[j] == -1) ++j;
		else {
		    arr[i] = arr[j];
		    arr[j] = -1;
		    j++;
		    break;
		}
	    }
	    if (j == n) return i;
	}
	++i;
    }
    return i;
}

#define fast_max(x,y) (x - ((x - y) & ((x - y) >> (sizeof(int) * CHAR_BIT - 1))))
#define fast_min(x,y) (y + ((x - y) & ((x - y) >> (sizeof(int) * CHAR_BIT - 1))))

void
fast_nms(drect *rects, int num, float overlap_th) {

    void *pmem = malloc(sizeof(int) * (num + num) + sizeof(float) * num);
    int *idxes = (int *)pmem;
    int *pick = idxes + num;
    float *invareas = (float *)(pick + num);
    int idx_count = num;
    int counter = 0, last_idx;
    int x0,y0,x1,y1;
    int tx0, ty0, tx1, ty1;

    for (int i = 0; i < num; ++i) idxes[i] = i;
    sort_idx(rects, idxes, num);

    for (int i = 0; i < num; ++i) {
	int ti = idxes[i];
	drect r = rects[ idxes[i] ];
	invareas[ti] = 1.0f / ((r.x1 - r.x0 + 1) * (r.y1 - r.y0 + 1));
    }

    while (idx_count > 0) {
	int tmp_idx = idx_count - 1;
	last_idx = idxes[ tmp_idx ];
	pick[counter++] = last_idx;

	x0 = rects[last_idx].x0;
	y0 = rects[last_idx].y0;
	x1 = rects[last_idx].x1;
	y1 = rects[last_idx].y1;

	idxes[ tmp_idx ] = -1;

	for (int i = tmp_idx-1; i != -1; i--) {

	    drect r = rects[ idxes[i] ];
	    tx0 = fast_max(x0, r.x0);
	    ty0 = fast_max(y0, r.y0);
	    tx1 = fast_min(x1, r.x1);
	    ty1 = fast_min(y1, r.y1);

	    tx0 = tx1 - tx0 + 1;
	    ty0 = ty1 - ty0 + 1;
	    if (tx0 > 0 && ty0 >0) {
		if (tx0 * ty0 * invareas[ idxes[i] ] > overlap_th) {
		    idxes[i] = -1;
		}
	    }
	}
	idx_count = sort_stable(idxes, idx_count);
    }

    /* just give the selected rects' indexes, modification needed for real use */
    for (int i = 0; i < counter; ++i) {
	printf("%d\n", pick[i]);
    }

    free(pmem);
}
