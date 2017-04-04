#include <iostream>
#include <string>
#include <stdio.h>
#include <time.h>
#include <sstream>
#include <fstream>
#include <algorithm>
#include <thread>
#include <iomanip>

std::string ZeroPadNumber(int num);

std::string getFileExt(const std::string& s);
int getFileNumber(const std::string& s);
std::string getFileName(const std::string& s);
std::string getPath2File(const std::string& s);
std::string getFileNamePrefix(const std::string& s);
std::string replaceInName(const std::string& s, std::string key, std::string replacement);
