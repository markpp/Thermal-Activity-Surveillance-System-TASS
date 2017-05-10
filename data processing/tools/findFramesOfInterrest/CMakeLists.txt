cmake_minimum_required(VERSION 2.8)
project(main)

# use sse3 instruction set
SET(CMAKE_CXX_FLAGS "-msse3")

find_package(OpenCV REQUIRED)

include_directories( ${OpenCV_INCLUDE_DIRS})
ADD_EXECUTABLE(main
			main.cpp 
            )
target_link_libraries(main ${OpenCV_LIBS})

ADD_DEFINITIONS(
    -std=c++11 # Or -std=c++0x
    # Other flags
)

