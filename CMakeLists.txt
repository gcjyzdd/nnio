cmake_minimum_required(VERSION 3.15)
project(my_project)

add_subdirectory(ext/grpc EXCLUDE_FROM_ALL)

add_executable(my_exe src/main.cpp
cppMsg/msg.grpc.fb.cc)
target_link_libraries(my_exe grpc++)
target_include_directories(my_exe PUBLIC cppMsg)
