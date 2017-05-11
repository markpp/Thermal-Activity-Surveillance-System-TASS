#include "presenter.hpp"

Presenter::Presenter()
{}

cv::Mat Presenter::draw_frame_number(Mat input_img, int frameNumber)
{
  cv::Mat output_img = input_img.clone();

  stringstream frameNrStream;
  frameNrStream << frameNumber;
  string frameNrString = frameNrStream.str();
  putText(output_img, frameNrString, cv::Point(12,20), CV_FONT_HERSHEY_PLAIN, 1, cv::Scalar(255,255,255), 1, 1);

  return output_img;
}

cv::Mat Presenter::draw_detections(Mat input_img, std::vector<Person> dets)
{
  cv::Mat output_img = input_img.clone();
  //for(auto & anno: annotations) {
  if(dets.size()>0)
  {
    for(size_t i=0;i<dets.size();i++)
    {
      cv::circle(output_img, dets[i].p_detection, 6, cv::Scalar(255,255,255), 1, 8);
      //rectangle(output_img, dets[i].rect_detection, cv::Scalar(255,255,255), 1, 8);
    }
  }
  return output_img;
}

cv::Mat Presenter::draw_tracks(Mat input_img, std::vector<Person> tracks)
{
  cv::Mat output_img;
  //cv::resize(input_img, output_img, cv::Size(IMAGEWIDTH_SCALE, IMAGEHEIGHT_SCALE), CV_INTER_LINEAR);
  cv::cvtColor(input_img, output_img, cv::COLOR_GRAY2BGR);

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

  if(tracks.size()>0)
  {
    for(size_t i=0;i<tracks.size();i++)
    {
      ///*
      stringstream trackIdStream;
      trackIdStream << tracks[i].track_id;
      string trackIdString = trackIdStream.str();
      putText(output_img, trackIdString, tracks[i].p_prediction, CV_FONT_HERSHEY_PLAIN, 1, cv::Scalar(255,255,255), 1,1);
      //*/
      if(tracks[i].mtb_score < tracks[i].ped_score)
      {
        tracks[i].type_tag = "P";
        putText(output_img, "P", cv::Point(tracks[i].p_prediction.x, tracks[i].p_prediction.y-20), CV_FONT_HERSHEY_PLAIN, 1, Colors[tracks[i].track_id%7], 1, 1);
      }
      else
      {
        tracks[i].type_tag = "B";
        putText(output_img, "B", cv::Point(tracks[i].p_prediction.x, tracks[i].p_prediction.y-20), CV_FONT_HERSHEY_PLAIN, 1, Colors[tracks[i].track_id%7], 1, 1);
      }

      cv::circle(output_img, tracks[i].p_prediction, 16, Colors[tracks[i].track_id%7], 2, 8);

      //rectangle(output_img, tracks[i].rect_detection, Colors[tracks[i].track_id%7], 1, 8);

/*
      if(tracks[i].trace.size()>2)
      {
        for(size_t j=0;j<tracks[i].trace.size()-1;j++)
        {
          line(output_img, cv::Point(tracks[i].trace[j].x, tracks[i].trace[j].y) ,cv::Point(tracks[i].trace[j+1].x, tracks[i].trace[j+1].y), Colors[tracks[i].track_id%7]*Scalar(0.2*j,0.2*j,0.2*j),2,CV_AA);
          //cout << myCTracker.tracks[i]->trace[j] << endl;
        }

        line(output_img, cv::Point(tracks[i].trace[tracks[i].trace.size()-1].x, tracks[i].trace[tracks[i].trace.size()-1].y), cv::Point((tracks[i].rect_detection.x+(tracks[i].rect_detection.width/2)), (tracks[i].rect_detection.y+(tracks[i].rect_detection.height/2))), Colors[tracks[i].track_id%7]*Scalar(255,255,255),2,CV_AA);

      }
      */
    }
  }
  return output_img;
}
