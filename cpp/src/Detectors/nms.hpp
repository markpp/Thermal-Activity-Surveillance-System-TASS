#include <iostream>
#include <sstream>
#include <fstream>
#include <string>
#include <stdio.h>
#include <vector>


typedef struct {
    int x0, y0, x1, y1;
    float score;
} drect;

void fast_nms(drect *rects, int num, float overlap_th);
