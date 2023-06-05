cmake_minimum_required(VERSION 3.22)
project(my_project)

set(CMAKE_EXPORT_COMPILE_COMMANDS ON)
set(CMAKE_VERBOSE_MAKEFILE OFF)

find_package(gRPC CONFIG REQUIRED)

file(MAKE_DIRECTORY ${CMAKE_CURRENT_LIST_DIR}/pyMsg)
file(MAKE_DIRECTORY ${CMAKE_CURRENT_LIST_DIR}/cppMsg)

set(OUT_SOURCES ${CMAKE_CURRENT_LIST_DIR}/cppMsg/msg.pb.cc
                ${CMAKE_CURRENT_LIST_DIR}/cppMsg/msg.grpc.pb.cc)
add_custom_command(
  OUTPUT ${OUT_SOURCES}
  COMMAND
    ${Protobuf_PROTOC_EXECUTABLE} --proto_path=${CMAKE_CURRENT_LIST_DIR}
    --grpc_out=${CMAKE_CURRENT_LIST_DIR}/cppMsg
    --plugin=protoc-gen-grpc=${GRPC_CPP_PLUGIN_PROGRAM}
    --cpp_out=${CMAKE_CURRENT_LIST_DIR}/cppMsg msg.proto
  DEPENDS ${CMAKE_CURRENT_LIST_DIR}/msg.proto
  VERBATIM)

add_custom_target(gen_cpp_msg DEPENDS ${OUT_SOURCES})

add_custom_target(
  gen_py_msg
  COMMAND
    ${Protobuf_PROTOC_EXECUTABLE} --proto_path=${CMAKE_CURRENT_LIST_DIR}
    --grpc_out=${CMAKE_CURRENT_LIST_DIR}/pyMsg --plugin=protoc-gen-grpc_python=
    --plugin=protoc-gen-grpc=${GRPC_PYTHON_PLUGIN_PROGRAM}
    --python_out=${CMAKE_CURRENT_LIST_DIR}/pyMsg msg.proto
  DEPENDS ${CMAKE_CURRENT_LIST_DIR}/msg.proto)

add_executable(my_test src/test.cpp cppMsg/msg.pb.cc cppMsg/msg.grpc.pb.cc)
target_link_libraries(my_test PUBLIC gRPC::grpc++)
target_include_directories(my_test PUBLIC cppMsg)
target_compile_features(my_test PRIVATE cxx_std_17)
add_dependencies(my_test gen_cpp_msg gen_py_msg)

add_executable(sam_client src/main.cpp cppMsg/msg.pb.cc cppMsg/msg.grpc.pb.cc
                          ext/stb/stb_image.cpp)
target_link_libraries(sam_client PUBLIC gRPC::grpc++)
target_include_directories(sam_client PUBLIC cppMsg ext)
target_compile_features(sam_client PRIVATE cxx_std_17)
add_dependencies(sam_client gen_cpp_msg gen_py_msg)