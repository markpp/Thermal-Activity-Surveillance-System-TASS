#include "Presentation.hpp"

Presentation::Presentation()
{
  //myCTracker.CenterTrackerInit(0.2,0.5,60.0,10,10);
  //CenterTracker myCTracker(0.2,0.5,60.0,10,10);
} 

cv::Mat Presentation::colorPresentation(Mat img16, int frameNumber, int scale)
{ 
    //cv::normalize(img16, normalizedRepresentation, 0, 255, NORM_MINMAX, CV_8UC1);
    //cvtColor(normalizedRepresentation, normalizedRepresentation, CV_BGR2GRAY);
  //Mat img16Thresh;

  int maxValue = 0;
  int minValue = 65535;
  // Find max and min value
  for (int i = 0; i < img16.rows; i++)
  {
      for (int j = 0; j < img16.cols; j++)
      {
        int value = img16.at<uint16_t>(i, j);
        if(maxValue < img16.at<uint16_t>(i, j)) maxValue = value;
        if(minValue > img16.at<uint16_t>(i, j)) minValue = value;

  /*
        if(img16.at<uint16_t>(i, j) > 8000)
        {
          //img16.at<uint16_t>(i, j) = gradientInX;
        }
        else
        {
          img16.at<uint16_t>(i, j) = 0;
        }
   */
      }
  }
  if(GlobMaxValue < maxValue) GlobMaxValue = maxValue;
  if(GlobMinValue > minValue) GlobMinValue = minValue;
  
  //cout << "minValue: " << minValue << endl;
  //cout << "maxValue: " << maxValue << endl;
  int diff = maxValue - minValue + 1;
  for (int i = 0; i < img16.rows; i++)
  {
      for (int j = 0; j < img16.cols; j++)
      {
        int baseValue = img16.at<uint16_t>(i, j); // take input value in [0, 65536)
        int scaledValue = 256*(baseValue - minValue)/diff; // map value to interval [0, 256), and set the pixel to its color value above
        //int scaledValue = 256*(baseValue - 6300)/1200; // map value to interval [0, 256), and set the pixel to its color value above
        colorRepresentation.at<Vec3b>(i,j)[2] = colormap[3*scaledValue];
        colorRepresentation.at<Vec3b>(i,j)[1] = colormap[3*scaledValue+1];
        colorRepresentation.at<Vec3b>(i,j)[0] = colormap[3*scaledValue+2];
      }
  }
  cv::resize(colorRepresentation,colorRepresentationBig,cv::Size(IMAGEWIDTH*scale,IMAGEHEIGHT*scale),CV_INTER_LINEAR);

  stringstream frameNumberStream;
  frameNumberStream << frameNumber;
  string frameNumberString = frameNumberStream.str();
  //putText(normalizedRepresentationBig, frameNumberString, cv::Point(12,20), CV_FONT_HERSHEY_PLAIN, 1, cv::Scalar(255,255,255), 1,1);
  putText(colorRepresentationBig, frameNumberString, cv::Point(12,20), CV_FONT_HERSHEY_PLAIN, 1, cv::Scalar(255,255,0), 1,1);

  return colorRepresentationBig;
}

cv::Mat Presentation::enlargeAndPresent(Mat maskImg, int frameNumber, int scale)
{
  cv::Mat intensityRepresentationBig;
  
  cv::cvtColor(maskImg,intensityRepresentationBig,cv::COLOR_GRAY2BGR);
  
  /*
  for (int i = 0; i < maskImg.rows; i++)
  {
    for (int j = 0; j < maskImg.cols; j++)
    {
      int baseValue = maskImg.at<uchar>(i, j)-80; // take input value in [0, 65536)
    
      intensityRepresentationBig.at<Vec3b>(i,j)[2] = colormap[3*baseValue];
      intensityRepresentationBig.at<Vec3b>(i,j)[1] = colormap[3*baseValue+1];
      intensityRepresentationBig.at<Vec3b>(i,j)[0] = colormap[3*baseValue+2];
    }
  }
  */
  cv::resize(intensityRepresentationBig, intensityRepresentationBig, cv::Size(IMAGEWIDTH*scale,IMAGEHEIGHT*scale), CV_INTER_LINEAR);
  
  stringstream frameNrStream;
  frameNrStream << frameNumber;
  string frameNrString = frameNrStream.str();
  putText(intensityRepresentationBig, frameNrString, cv::Point(12,20), CV_FONT_HERSHEY_PLAIN, 1, cv::Scalar(255,255,255), 1,1);
  
  return intensityRepresentationBig;
}

cv::Mat Presentation::intensityPresentationAlt(Mat maskImg, int frameNumber, std::vector<Object> tracksVector, int scale)
{
  cv::Mat intensityRepresentationBig;
  
  cv::cvtColor(maskImg,intensityRepresentationBig,cv::COLOR_GRAY2BGR);
  
  /*
  for (int i = 0; i < maskImg.rows; i++)
  {
    for (int j = 0; j < maskImg.cols; j++)
    {
      int baseValue = maskImg.at<uchar>(i, j)-80; // take input value in [0, 65536)
    
      intensityRepresentationBig.at<Vec3b>(i,j)[2] = colormap[3*baseValue];
      intensityRepresentationBig.at<Vec3b>(i,j)[1] = colormap[3*baseValue+1];
      intensityRepresentationBig.at<Vec3b>(i,j)[0] = colormap[3*baseValue+2];
    }
  }
  */
  cv::resize(intensityRepresentationBig, intensityRepresentationBig, cv::Size(IMAGEWIDTH*scale,IMAGEHEIGHT*scale), CV_INTER_LINEAR);
  
  stringstream frameNrStream;
  frameNrStream << frameNumber;
  string frameNrString = frameNrStream.str();
  putText(intensityRepresentationBig, frameNrString, cv::Point(12,20), CV_FONT_HERSHEY_PLAIN, 1, cv::Scalar(255,255,255), 1,1);
  /*
  if(tracksVector.size()>0)
  {
    //myCTracker.Update(centers);
    
    for(size_t i=0;i<tracksVector.size();i++)
    {
      //rectangle(intensityRepresentationBig, Rect(tracksVector[i].rect.x*scale, tracksVector[i].rect.y*scale, tracksVector[i].rect.width*scale, tracksVector[i].rect.height*scale), Colors[tracksVector[i].track_id%6], 1, 8 );
      //cout << tracksVector[i].track_id << endl;
      stringstream trackIdStream;
      trackIdStream << tracksVector[i].track_id;
      string trackIdString = trackIdStream.str();
      //putText(intensityRepresentationBig, trackIdString, cv::Point(12,20), CV_FONT_HERSHEY_PLAIN, 1, cv::Scalar(255,255,255), 1,1);
      if(tracksVector[i].trace.size()>2)
      {
        for(size_t j=0;j<tracksVector[i].trace.size()-1;j++)
        {
          line(intensityRepresentationBig, cv::Point(tracksVector[i].trace[j].x*scale, tracksVector[i].trace[j].y*scale) ,cv::Point(tracksVector[i].trace[j+1].x*scale, tracksVector[i].trace[j+1].y*scale), Colors[tracksVector[i].track_id%7]*Scalar(0.2*j,0.2*j,0.2*j),2,CV_AA);
          //cout << myCTracker.tracks[i]->trace[j] << endl;
        }
        line(intensityRepresentationBig, cv::Point(tracksVector[i].trace[tracksVector[i].trace.size()-1].x*scale, tracksVector[i].trace[tracksVector[i].trace.size()-1].y*scale), cv::Point((tracksVector[i].rect.x+(tracksVector[i].rect.width/2))*scale, (tracksVector[i].rect.y+(tracksVector[i].rect.height/2))*scale), Colors[tracksVector[i].track_id%7]*Scalar(255,255,255),2,CV_AA);
      }
    }
  }
  */
  return intensityRepresentationBig;
}

cv::Mat Presentation::showContour(Mat maskImg, std::vector<Object> candidateVector, int scale)
{
  RNG rng(12345);
  cv::Mat out;
  cv::cvtColor(maskImg,out,cv::COLOR_GRAY2BGR);
  /*
  for (int i = 0; i < maskImg.rows; i++)
  {
    for (int j = 0; j < maskImg.cols; j++)
    {
      if (maskImg.at<uchar>(i, j)>80)
      {
        int baseValue = maskImg.at<uchar>(i, j)-80; // take input value in [0, 65536)
        
        out.at<Vec3b>(i,j)[2] = colormap[3*baseValue];
        out.at<Vec3b>(i,j)[1] = colormap[3*baseValue+1];
        out.at<Vec3b>(i,j)[0] = colormap[3*baseValue+2];
      }
    }
  }
  */
  if (scale > 1) 
  {
    cv::resize(out, out, cv::Size(IMAGEWIDTH*scale,IMAGEHEIGHT*scale), CV_INTER_LINEAR);
  }
  /*
  std::vector<cv::Point> scaledContour;
  for(size_t i=0;i<candidateVector.size();i++)
  {
    Scalar rngColor = Scalar( rng.uniform(0, 255), rng.uniform(0,255), rng.uniform(0,255) );

    circle(out, cv::Point(candidateVector[i].center2D.x*scale, candidateVector[i].center2D.y*scale), 3, rngColor, 1, CV_AA);
    
    if (scale < 2) {
      cv::polylines(out, candidateVector[i].contour, true, rngColor);
    }
    else if (scale < 4){
      add(candidateVector[i].contour, candidateVector[i].contour, scaledContour);
      cv::polylines(out, scaledContour, true, rngColor);
    }
    else{
      add(candidateVector[i].contour, candidateVector[i].contour, scaledContour);
      add(scaledContour, scaledContour, scaledContour);
      cv::polylines(out, scaledContour, true, rngColor);
    }
    

  }
*/
  return out;
}
/*

cv::Mat Presentation::intensityPresentation(Mat maskImg, std::vector<Person> trackedVector,  int scale, int color)
{
  cv::Mat intensityRepresentationBig;
  cv::resize(maskImg, intensityRepresentationBig, cv::Size(IMAGEWIDTH*scale,IMAGEHEIGHT*scale), CV_INTER_LINEAR);

  for( size_t i = 0; i < trackedVector.size(); i++ )
  {
    //cv::Rect scaledRect = cv::Rect(trackedVector[i].ROI.x*scale, trackedVector[i].ROI.y*scale, trackedVector[i].ROI.width*scale, trackedVector[i].ROI.height*scale);
    //rectangle(intensityRepresentationBig, scaledRect, cv::Scalar(color, color, color), 1, 1 );
    
    stringstream idNumberStream;
    idNumberStream << trackedVector[i].id;
    string idNumberString = idNumberStream.str();
    //putText(normalizedRepresentationBig, frameNumberString, cv::Point(12,20), CV_FONT_HERSHEY_PLAIN, 1, cv::Scalar(255,255,255), 1,1);
    putText(intensityRepresentationBig, idNumberString,  cv::Point(trackedVector[i].center2D.x*scale, trackedVector[i].center2D.y*scale), CV_FONT_HERSHEY_PLAIN, 1, cv::Scalar(255,255,0), 1,1);
    
    line( intensityRepresentationBig, cv::Point(trackedVector[i].center2D.x*scale, trackedVector[i].center2D.y*scale-5), cv::Point(trackedVector[i].center2D.x*scale, trackedVector[i].center2D.y*scale+5), Scalar(color, color, color),  1, 8 );
    line( intensityRepresentationBig, cv::Point(trackedVector[i].center2D.x*scale-5, trackedVector[i].center2D.y*scale), cv::Point(trackedVector[i].center2D.x*scale+5, trackedVector[i].center2D.y*scale), Scalar(color, color, color),  1, 8 );
    
    line( intensityRepresentationBig, cv::Point(trackedVector[i].kalman2Dposition.x*scale-5, trackedVector[i].kalman2Dposition.y*scale-5), cv::Point(trackedVector[i].kalman2Dposition.x*scale+5, trackedVector[i].kalman2Dposition.y*scale+5), Scalar(color, color, color),  1, 8 );
    line( intensityRepresentationBig, cv::Point(trackedVector[i].kalman2Dposition.x*scale-5, trackedVector[i].kalman2Dposition.y*scale+5), cv::Point(trackedVector[i].kalman2Dposition.x*scale+5, trackedVector[i].kalman2Dposition.y*scale-5), Scalar(color, color, color),  1, 8 );
  }
  return intensityRepresentationBig;
}

void Presentation::enlargeDetections(Mat maskImg, std::vector<Person> trackedVector, int scale)
{
  
  for( size_t i = 0; i < trackedVector.size(); i++ )
  {
    cv::Mat tempDetection = maskImg(trackedVector[i].ROI);
    cv::resize(tempDetection, tempDetection, cv::Size(trackedVector[i].ROI.width*scale, trackedVector[i].ROI.height*scale), CV_INTER_LINEAR);

    stringstream ss;
    ss << trackedVector[i].id; //std::to_string()
    string str = "Detection: " + ss.str();
    
    cv::namedWindow(str);
    cv::moveWindow(str, -200, -400+10*(int)i);
    cv::imshow(str, tempDetection);
  }
}
*/