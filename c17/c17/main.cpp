//
//  main.cpp
//  c17
//
//  Created by kshileev on 9/26/18.
//  Copyright © 2018 kshileev. All rights reserved.
//

#include <iostream>
#include <vector>
#include <map>

int main(int argc, const char * argv[]) {
    std::vector<int> v = {1,2,3,4,5};
    int number = 1'000'000;
    for (auto i: v)
        std::cout << i << ' ';
    std::cout << number << std::endl;
    return 0;
}
