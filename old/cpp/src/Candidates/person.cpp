#include "person.hpp"

size_t Person::NextDetectionID=0;
// ---------------------------------------------------------------------------
// Track constructor.
// The track begins from initial point (pt)
// ---------------------------------------------------------------------------
Person::Person(cv::Rect candidate_rect)
{
  detection_id = NextDetectionID;
  rect_detection = candidate_rect;
  p_detection = cv::Point(rect_detection.x+rect_detection.width/2, rect_detection.y+rect_detection.height/2);
  NextDetectionID++;
  // Every track have its own Kalman filter,
  // it user for next point position prediction.
  KF = new TKalmanFilter(p_detection, 0.9, 0.5);
  // Here stored points coordinates, used for next position prediction.
  p_prediction = p_detection;
  skipped_frames=0;
}

bool Person::locateTrack()
{
  //bool insideFrame = true;
  if(trace[trace.size()-1].x > IMAGEWIDTH_SCALE-10)
  {
    departureLocation = "r";
    return false;
  }
  if(trace[trace.size()-1].x < 0)
  {
    departureLocation = "l";
    return false;
  }
  if(trace[trace.size()-1].y > IMAGEHEIGHT_SCALE-10)
  {
    departureLocation = "b";
    return false;
  }
  if(trace[trace.size()-1].y < 0)
  {
    departureLocation = "t";
    return false;
  }

  return true;
}

bool Person::classify()
{
  //Point2f diff=(trace.back()-trace.front());
  //float dist=sqrtf(diff.x*diff.x+diff.y*diff.y);
  //std::cout << dist << std::endl;
  int margin = 20;
  //bool insideFrame = true;
  if(trace[trace.size()-1].x > IMAGEWIDTH_SCALE-margin)
  {
    departureLocation = "right";
    return false;
  }
  if(trace[trace.size()-1].x < margin)
  {
    departureLocation = "left";
    return false;
  }
  if(trace[trace.size()-1].y > IMAGEHEIGHT_SCALE-margin)
  {
    departureLocation = "bottom";
    return false;
  }
  if(trace[trace.size()-1].y < margin)
  {
    departureLocation = "top";
    return false;
  }

  return true;
}
