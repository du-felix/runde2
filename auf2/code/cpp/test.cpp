#include <bitset>
#include <iostream>
int main(int argc, char const *argv[])
{
    std::vector<bool> flags;
    flags.resize(10, false);
    for (size_t i = 0; i < flags.size(); i++)
    {
        flags[i] = true;
    }
    
    for (auto flag: flags) {
        std::cout << flag << " ";
    }
    return 0;
}
