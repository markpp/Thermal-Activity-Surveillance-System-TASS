cmake_minimum_required(VERSION 2.8)
project(main)


add_definitions(-DDLIB_PNG_SUPPORT)

include(libs/dlib191/dlib/cmake)

# use sse3 instruction set
SET(CMAKE_CXX_FLAGS "-msse3")

find_package(OpenCV REQUIRED)
include(FindPNG)
#find_package(dlib REQUIRED)
#message(STATUS "Using dlib-${dlib_VERSION}")

include_directories(${OpenCV_INCLUDE_DIRS})
ADD_EXECUTABLE(main
			         main.cpp
               src/Tools/FileHandler.cpp
							 src/Detectors/dlib_fhog.cpp
              )
target_link_libraries(main dlib ${OpenCV_LIBS} ${PNG_LIBRARY})



ADD_DEFINITIONS(
    -std=c++11 # Or -std=c++0x
		-DLIB_PNG_SUPPORT
    # Other flags
)
