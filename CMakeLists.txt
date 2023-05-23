cmake_minimum_required(VERSION 3.22)
project(my_project)

set(CMAKE_EXPORT_COMPILE_COMMANDS ON)
set(CMAKE_VERBOSE_MAKEFILE OFF)

find_package(gRPC CONFIG REQUIRED)

add_executable(my_exe src/main.cpp cppMsg/msg.pb.cc cppMsg/msg.grpc.pb.cc)
target_link_libraries(my_exe PUBLIC gRPC::grpc++)
target_include_directories(my_exe PUBLIC cppMsg)
target_compile_features(my_exe PRIVATE cxx_std_17)
