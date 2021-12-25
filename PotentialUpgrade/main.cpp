#include "Graph.h"
#include "Aux.h"
#include <vector>
//#include <armadillo>

int main() {
    int N = 3;

    std::vector<int> v(N*N, 0);
    producer(v, N);
    std::vector<std::vector<int>> v_new = resizer(v, N);
    show_matrix(v_new);

    return 0;
}
