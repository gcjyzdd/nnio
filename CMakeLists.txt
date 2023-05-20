cmake_minimum_required(VERSION 3.15)
project(my_project)

set(CMAKE_EXPORT_COMPILE_COMMANDS ON)

# it has to find protobuf first otherwise it won't find grpc
find_package(Protobuf REQUIRED)
find_package(gRPC CONFIG REQUIRED)

add_executable(my_exe src/main.cpp
cppMsg/msg.pb.cc)
target_link_libraries(my_exe grpc++)
target_include_directories(my_exe PUBLIC cppMsg)
