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


class Graph {
public:
    int N;
    float p;
    std::vector<std::vector<int>> m;
    // don't know how to implement a conditional behaviour
    // so bool weighted = true;
    std::vector<std::vector<int>> m_randomfactor;

};


void producer(std::vector<int> &v, int N)
{

    for (int i=0; i < std::pow(N,2); ++i){
        v[i] = i;
    }
    std::random_device rd;  //Will be used to obtain a seed for the random number engine
    std::mt19937 gen(rd()); //Standard mersenne_twister_engine seeded with rd()

    std::shuffle(v.begin(), v.end(), gen);

    std::copy(v.begin(), v.end(), std::ostream_iterator<int>(std::cout, " "));
    std::cout << '\n';
}
