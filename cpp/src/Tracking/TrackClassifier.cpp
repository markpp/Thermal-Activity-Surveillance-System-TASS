#include "TrackClassifier.hpp"

using namespace std;

TrackClassifier::TrackClassifier()
{
  trackOutputStream << "/Users/markpp/Desktop/code/VAPprojects/data/watchDog/tracks.csv";
  pathString = trackOutputStream.str();
  outputFileStream.open(pathString);
}

void TrackClassifier::classifyTrack(Object track)
{
  // BB ratio check for determining if biker or walker
  //if(track.calcMeanBBRatio() > 0.6) //close to 1 -> bike
  //{
    string bikeString = "biker" + separator + "trackedFrom_" + std::to_string(track.firstFrame) + separator + "trackLifetime_" + std::to_string(track.lifetime) + separator + "trackid_" + std::to_string(track.track_id) + separator + "departure_" + track.departureLocation + separator + "speed_" + std::to_string(track.calcMeanSpeed()) + separator + "BBratio_" + std::to_string(track.calcMeanBBRatio()) + "\r\n";
    outputFileStream << bikeString;
    cout << bikeString << endl;
  //}
  /*
  else   
  {
    string walkString = "walker" + separator + "trackid_" + std::to_string(track.track_id) + separator + "departure_" + track.departureLocation + separator + "speed_" + std::to_string(track.calcMeanSpeed()) + "\r\n";
    outputFileStream << walkString;
    cout << walkString << endl;
  }
   */
}




void TrackClassifier::createSurveillanceReport()
{
  /*
  for(int k=0;k<myvehicles.size();k++)
  {
    if(myvehicles[k].lifeTime > minLifeTime)
    {
      myvehicles[k].calcAvgDist();
      oldvehicles.push_back(myvehicles[k]);
      classifyMovement((oldvehicles.size()-1));
    }
  }
  
  int sumOfVehicles = 0;
  for(int k=0;k<foundVehiclesInframe.size();k++)
  {
    sumOfVehicles += foundVehiclesInframe[k];
  }
  
  cout << "Avg number of cars in video clip: " << (float)sumOfVehicles/foundVehiclesInframe.size() << endl;
  cout << "oldvehicles.size(): " << oldvehicles.size() << endl;
  
  for(int k=0;k<oldvehicles.size();k++)
  {
    cout << "Car " << k << " did event: " << oldvehicles[k].bestMatchIndex << endl;
    eventScores[oldvehicles[k].bestMatchIndex]++;
  }
  
  for(int k=0; k<numberOfEvents; k++)
  {
    if (k==6)
    {
      cout << "Event 'could not be matched " << k << "' was registrated " << eventScores[k] << " times" << endl;
    }
    else
    {
      cout << "Event: " << movementNames[k] << " was registrated " << eventScores[k] << " times" << endl;
    }
  }
  
  for(int k=0;k<oldvehicles.size();k++)
  {
    if (oldvehicles[k].centerCount > minCenterDetections)
    {
      cout << "Car " << k << " with avg distance of : " << oldvehicles[k].avgDist*distanceMultiplier-egoCarOfset << ", min distance of: " <<
      oldvehicles[k].minDist*distanceMultiplier-egoCarOfset << "m at frame: " << oldvehicles[k].minDistFoundAtFrame << ", was found to be in front" << endl;
    }
  }
   */
}
/*
void TrackClassifier::classifyMovement(int k)
{
  int sum=0;
  for(int i=0; i<numberOfMovementTypes; i++)
  {
    //cout << "bin " << i << " size: " << oldvehicles[k].movementType[i] << endl;
    sum += oldvehicles[k].movementType[i];
  }
  
  for(int i=0; i<numberOfMovementTypes; i++)
  {
    oldvehicles[k].movementType[i]=oldvehicles[k].movementType[i]/sum;
    //cout << "bin " << i << " size: " << oldvehicles[k].movementType[i] << endl;
  }
  
  for(int i=0; i<numberOfEvents-1; i++)
  {
    oldvehicles[k].result[i] = sqrt(
                                    pow(oldvehicles[k].movementType[0]-movementTypes[i][0],2)+pow(oldvehicles[k].movementType[0]-movementTypes[i][0],2)
                                    +pow(oldvehicles[k].movementType[1]-movementTypes[i][1],2)+pow(oldvehicles[k].movementType[2]-movementTypes[i][2],2)
                                    +pow(oldvehicles[k].movementType[3]-movementTypes[i][3],2)+pow(oldvehicles[k].movementType[4]-movementTypes[i][4],2)
                                    +pow(oldvehicles[k].movementType[5]-movementTypes[i][5],2)+pow(oldvehicles[k].movementType[6]-movementTypes[i][6],2)
                                    +pow(oldvehicles[k].movementType[7]-movementTypes[i][7],2)+pow(oldvehicles[k].movementType[8]-movementTypes[i][8],2));
  }
  
  int index = 0;
  for(int i = 0; i < numberOfEvents-1; i++)
  {
    if(oldvehicles[k].result[i] < oldvehicles[k].result[index])
    {
      index = i;
    }
    cout << "Car: " << k << " distance for: " << movementNames[i] << " was: " << oldvehicles[k].result[i] << endl;
  }
  if (oldvehicles[k].result[index] < 0.5)
  {
    oldvehicles[k].bestMatchIndex = index;
    cout << "This was car: " << k << " Best match was event: " << movementNames[index] << endl;
  }
  else
  {
    oldvehicles[k].bestMatchIndex = 6;
    cout << "It was not possilbe to match an event for this car: " << k << " Best match was: " << movementNames[index] << endl;
  }
 
}
*/