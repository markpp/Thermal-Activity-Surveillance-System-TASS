#include "CTracker.h"
using namespace cv;
using namespace std;

size_t CTracker::NextTrackID=0;

CTracker::CTracker()
{

}
// ---------------------------------------------------------------------------
//
// ---------------------------------------------------------------------------
void CTracker::Update(std::vector<Person> detections, size_t frameNumber, ofstream& csv_file)
{
	// -----------------------------------
	// If there is no tracks yet, then every point begins its own track.
	// -----------------------------------
	if(tracks.size()==0)
	{
		// If no tracks yet
		for(size_t i=0;i<detections.size();i++)
		{
      //CTrack* tr=new CTrack(detections[i].center2D,dt,Accel_noise_mag);
      //tracks.push_back(tr);
      detections[i].firstFrame = frameNumber;
      detections[i].track_id = NextTrackID;
      NextTrackID++;
      tracks.push_back(detections[i]);
		}
	}

	// -----------------------------------
	// Define cost Matrix
	// -----------------------------------
	size_t N=tracks.size();		// Number of existing tracks
	size_t M=detections.size();	// Number of detections to assign
  //cout << "N : " << N << "M : " << M << endl;
	//
	vector< vector<double> > Cost(N,vector<double>(M));
	vector<int> assignment; //

	// -----------------------------------
	// Calculate cost
	// -----------------------------------
	double dist;
	for(size_t i=0;i<tracks.size();i++)
	{
		// Point2d prediction=tracks[i]->prediction;
		// cout << prediction << endl;
		for(size_t j=0;j<detections.size();j++)
		{
			Point2f diff=(tracks[i].p_prediction-detections[j].p_detection);
			dist=sqrtf(diff.x*diff.x+diff.y*diff.y);
			Cost[i][j]=dist;
		}
	}
	// -----------------------------------
	// Solving assignment problem (tracks and predictions of Kalman filter)
	// -----------------------------------
  if(N>0)
  {
    AssignmentProblemSolver APS;
    APS.Solve(Cost,assignment,AssignmentProblemSolver::optimal);
  }
	// -----------------------------------
	// clean assignment from pairs with large distance
	// -----------------------------------
	// Not assigned tracks
	vector<size_t> not_assigned_tracks;

	for(size_t i=0;i<assignment.size();i++)
	{
		if(assignment[i]!=-1)
		{
			if(Cost[i][assignment[i]]>dist_thres)
			{
				assignment[i]=-1;
				// Mark unassigned tracks, and increment skipped frames counter,
				// when skipped frames counter will be larger than threshold, track will be deleted.
				not_assigned_tracks.push_back(i);
			}
		}
		else
		{
			// If track have no assigned detect, then increment skipped frames counter.
			tracks[i].skipped_frames++;
		}

	}

	// -----------------------------------
	// Search for unassigned detects
	// -----------------------------------
	vector<size_t> not_assigned_detections;
	vector<int>::iterator it;
	for(size_t i=0;i<detections.size();i++)
	{
		it=find(assignment.begin(), assignment.end(), i);
		if(it==assignment.end())
		{
			not_assigned_detections.push_back(i);
		}
	}

	// -----------------------------------
	// and start new tracks for them.
	// -----------------------------------
	if(not_assigned_detections.size()!=0)
	{
		for(size_t i=0;i<not_assigned_detections.size();i++)
		{
      //CTrack* tr=new CTrack(detections[not_assigned_detections[i]].center2D,dt,Accel_noise_mag);
      detections[i].firstFrame = frameNumber;
      detections[i].track_id = NextTrackID;
      NextTrackID++;
			tracks.push_back(detections[i]);
		}
	}

	// Update Kalman Filters state
	for(size_t i=0;i<assignment.size();i++)
	{
		// If track updated less than one time, then filter state is not correct.
		tracks[i].KF->GetPrediction();

		if(assignment[i]!=-1) // If we have assigned detect, then update using its coordinates,
		{
			tracks[i].skipped_frames=0;
      tracks[i].p_detection = detections[assignment[i]].p_detection;

      tracks[i].rect_detection = detections[assignment[i]].rect_detection;
      //tracks[i].traceRect.push_back(tracks[i].rect);
			tracks[i].p_prediction = tracks[i].KF->Update(detections[assignment[i]].p_detection, 1);
		}
    else				  // if not continue using predictions
		{
			tracks[i].p_prediction = tracks[i].KF->Update(Point2f(0,0), 0);
      //tracks[i].traceRect.push_back(tracks[i].rect);
		}


		if(tracks[i].trace.size() > max_trace_length)
		{
			tracks[i].trace.erase(tracks[i].trace.begin(),tracks[i].trace.end()-max_trace_length);
		}

    tracks[i].lifetime++;
		tracks[i].KF->LastResult=tracks[i].p_prediction;
	}

  for(size_t i=0;i<tracks.size();i++)
  {

    if(tracks[i].mtb_score < tracks[i].ped_score)
    {
      tracks[i].type_tag = "P";
    }
    else
    {
      tracks[i].type_tag = "B";
      //std::cout << tracks[i].p_detection << std::endl;
    }

		tracks[i].trace.push_back(tracks[i].p_prediction);

    bool remove = false;
    // -----------------------------------
    // If track didn't get detects long time, remove it.
    // -----------------------------------
    if(tracks[i].skipped_frames > maximum_allowed_skipped_frames)
    {
      if(tracks[i].lifetime > minLifetime)
      {
        //myTrackClassifier.classifyTrack(tracks[i]);
      }
      remove = true;
    }
    // -----------------------------------
    // If track moves outside of frame, classify and remove it.
    // -----------------------------------
    if(tracks[i].trace.size() > 0)
    {
      //std::cout << "tag: " << tracks[i].type_tag << std::endl;
      if(tracks[i].lifetime > minLifetime)
      {
        if(!tracks[i].classify())
        {
  					std::cout << "ID: " << tracks[i].track_id << "; exit: " <<
												 tracks[i].departureLocation << "; tag: " << tracks[i].type_tag << std::endl;
  					csv_file << frameNumber << ";"
						         << tracks[i].type_tag << ";"
										 << tracks[i].departureLocation << "\n";
            remove = true;
        }

      }
    }

    if(remove)
    {
      tracks.erase(tracks.begin()+i);
      assignment.erase(assignment.begin()+i);
      i--;
    }

  }

}
// ---------------------------------------------------------------------------
//
// ---------------------------------------------------------------------------
CTracker::~CTracker()
{
	for(size_t i=0;i<tracks.size();i++)
	{
    //delete tracks[i];
	}
	tracks.clear();
}
