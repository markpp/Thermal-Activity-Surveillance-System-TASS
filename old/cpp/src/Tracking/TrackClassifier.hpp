#include <vector>
#include <iostream>
#include <string>
#include <stdio.h>
#include <time.h>
#include <sstream>
#include <fstream>

#ifndef _OBJECT
#define _OBJECT
#include "../Candidates/Object.hpp"
#endif

using namespace std;
class TrackClassifier
{
public:
	TrackClassifier();
  void classifyTrack(Object track);
  
  void createSurveillanceReport();

  ofstream outputFileStream;

private:
	string pathString;
	stringstream trackOutputStream;
  string separator = ";";
};