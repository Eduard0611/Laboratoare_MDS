#include <iostream>
#include <vector>
#include <set>
#include <map>
#include <string>

int main() {
    std::map<std::string, std::vector<std::string>> deps = {
        {"curl", {"openssl", "nghttp2"}},
        {"openssl", {"zlib", "libcrypt"}},
        {"nghttp2", {"zlib"}},
        {"python", {"zlib", "libffi", "readline"}},
    };
    
    std::cout << "Resolving dependencies...\n";
    std::vector<std::string> to_install = {"curl", "python", "vim"};
    std::set<std::string> seen(to_install.begin(), to_install.end());
    
    // BUG: Iterating over a vector using a range-based for loop while modifying it inside the loop!
    for (const auto& pkg : to_install) {
        if (deps.count(pkg)) {
            for (const auto& dep : deps[pkg]) {
                if (seen.insert(dep).second) {
                    to_install.push_back(dep); // Error: this might reallocate to_install, invalidating the iterator for the outer loop
                }
            }
        }
    }
    
    std::cout << "Packages to install: " << to_install.size() << " packages" << std::endl;
    for (const auto& pkg : to_install) {
        std::cout << "installing " << pkg << std::endl;
    }
    std::cout << "done." << std::endl;
    return 0;
}