# Test Neural Networks IO using gRPC and Protobuffers

## Install vcpkg

``` sh
export VCPKG_DIR=$HOME/Documents/vcpkg
cd ~/Documents
git clone https://github.com/Microsoft/vcpkg.git
cd vcpkg
./bootstrap-vcpkg.sh
./vcpkg install grpc
```

## Build

``` sh
# generate messages using protoc from vcpkg
$VCPKG_DIR/installed/x64-linux/tools/protobuf/protoc --proto_path=. --grpc_out=cppMsg \
  --plugin=protoc-gen-grpc=$VCPKG_DIR/installed/x64-linux/tools/grpc/grpc_cpp_plugin \
  --cpp_out=cppMsg msg.proto
# generate messages for python
$VCPKG_DIR/installed/x64-linux/tools/protobuf/protoc --proto_path=. --grpc_python_out=pyMsg \
  --plugin=protoc-gen-grpc_python=$VCPKG_DIR/installed/x64-linux/tools/grpc/grpc_python_plugin \
  --python_out=pyMsg msg.proto

mkdir build && cd build
cmake -DCMAKE_TOOLCHAIN_FILE=$VCPKG_DIR/scripts/buildsystems/vcpkg.cmake ..
make
```

## Python Server

Create a virtual python environment:

``` sh
# create a virtual environment
python3 -m venv venv
# activate the environment
source venv/bin/activate
# install packages
pip install -r requirements.txt
```

References:

* [Quickstart C++ gRPC](https://grpc.io/docs/languages/cpp/quickstart/)
* [Install gRPC](https://grpc.io/blog/installation/)
* [Announcing out-of-the-box support for gRPC in the Flatbuffers serialization library](https://grpc.io/blog/grpc-flatbuffers/)
* [git submodules - could not get a repository handle for submodule](https://stackoverflow.com/questions/75769128/git-submodules-could-not-get-a-repository-handle-for-submodule)
* [grpc can't find protobuf library](https://stackoverflow.com/questions/62245040/grpc-cant-find-protobuf-library)
* [What is a correct way to setup protobuf and grpc for cpp project?](https://stackoverflow.com/questions/70700592/what-is-a-correct-way-to-setup-protobuf-and-grpc-for-cpp-project)
