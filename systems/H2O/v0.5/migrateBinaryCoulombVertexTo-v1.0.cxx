#include <iostream>
#include <fstream>
#include <vector>

int main(int argc, char **args) {
  char *srcName = args[1];
  char *dstName = args[2];
  std::ifstream src(srcName, std::ifstream::ate | std::ifstream::binary);
  size_t size(src.tellg());
  // header size for 3 dimensional object
  size_t headerSize = 32 + 8*3;
  size -= headerSize;
  src.seekg(headerSize, std::ifstream::beg);
  std::ofstream dst(dstName, std::ifstream::binary);
  std::vector<char> buffer(size);
  std::cout << "copying " << size << " bytes from " << srcName << " to " << dstName << std::endl;
  src.read(buffer.data(), buffer.size());
  dst.write(buffer.data(), buffer.size());
  return 0;
}


