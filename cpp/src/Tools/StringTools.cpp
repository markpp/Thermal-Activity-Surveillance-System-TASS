#include "StringTools.hpp"

std::string ZeroPadNumber(int num)
{
    std::ostringstream ss;
    ss << std::setw( 6 ) << std::setfill( '0' ) << num;
    return ss.str();
}

std::string getFileExt(const std::string& s) {

    size_t i = s.rfind('.', s.length());
    if (i != std::string::npos) {
        return(s.substr(i+1, s.length() - i));
    }

    return("");
}

int getFileNumber(const std::string& s) {

    size_t i = s.rfind('_', s.length());
    if (i != std::string::npos) {
        return(std::stoi(s.substr(i+1, s.length() - 4), nullptr));
    }

    return(0);
}

std::string getFileName(const std::string& s) {

    char sep = '/';

    size_t i = s.rfind(sep, s.length());
    if (i != std::string::npos) {
        return(s.substr(i+1, s.length() - i));
    }

    return("");
}

std::string getPath2File(const std::string& s) {

  char sep = '/';

  size_t i = s.rfind(sep, s.length());
  if (i != std::string::npos) {
    return(s.substr(0, i));
  }

  return("");
}

std::string getFileNamePrefix(const std::string& s) {

    char sep = '_';

    size_t i = s.rfind(sep, s.length());
    if (i != std::string::npos) {
        return(s.substr(i+1, s.length() - i));
    }

    return("");
}

std::string replaceInName(const std::string& s, std::string key, std::string replacement) {

    std::string str = s;

    std::size_t found = s.rfind(key);
    if (found != std::string::npos)
    {
        return(str.replace (found,key.length(),replacement));
    }

    return("");
}
