cmake_minimum_required(VERSION 3.22)
project(my_project)

set(CMAKE_EXPORT_COMPILE_COMMANDS ON)
set(CMAKE_VERBOSE_MAKEFILE OFF)

find_package(gRPC CONFIG REQUIRED)

add_executable(my_test src/test.cpp cppMsg/msg.pb.cc cppMsg/msg.grpc.pb.cc)
target_link_libraries(my_test PUBLIC gRPC::grpc++)
target_include_directories(my_test PUBLIC cppMsg)
target_compile_features(my_test PRIVATE cxx_std_17)

add_executable(sam_client src/main.cpp cppMsg/msg.pb.cc cppMsg/msg.grpc.pb.cc ext/stb/stb_image.cpp)
target_link_libraries(sam_client PUBLIC gRPC::grpc++)
target_include_directories(sam_client PUBLIC cppMsg ext)
target_compile_features(sam_client PRIVATE cxx_std_17)
