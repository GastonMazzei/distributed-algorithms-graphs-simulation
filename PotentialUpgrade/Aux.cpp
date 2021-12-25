//
// Created by m4zz31 on 3/10/21.
//
#include "Graph.h"

#include <algorithm>
#include <cstdint>
#include <iostream>
#include <vector>
#include <random>
#include <iterator>

void show_matrix(std::vector<std::vector<int>> v){
    for (int i=0; i<v.size(); i++){
        std::copy(v[i].begin(), v[i].end(), std::ostream_iterator<int>(std::cout, " "));
        std::cout << '\n';
    }
}

std::vector<std::vector<int>> resizer(std::vector<int> v, int N){
    std::vector<std::vector<int>> v_new(N, std::vector<int>(N,0));
    for (int i=0; i<N; i++){
        for (int j=0; j<N; j++){
            v_new[i][j] = v[i+j*N];
        }
    }
    return v_new;
}
