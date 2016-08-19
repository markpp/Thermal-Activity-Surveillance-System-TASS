#include "FileHandler.hpp"

std::vector<std::vector<std::string> > load_annotations(std::string annotation_path)
{
  std::vector<std::string> anno;
  std::vector<std::vector<std::string> > annotations;
  std::ifstream data(annotation_path);
  std::string line;
  std::getline(data,line); // Ignore header line
  while(std::getline(data,line))
  {
      std::stringstream  lineStream(line);
      std::string        cell;

      anno.clear();
      while(std::getline(lineStream, cell, ';'))
      {
          // You have a cell!!!!
          anno.push_back(cell);
          //std::cout << cell[0] << std::endl;
      }

      // Fix possible repeat of frames
      annotations.push_back(anno);




      //while (1) { }
  }
  return annotations;
}
