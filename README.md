# Test Neural Networks IO using gRPC and Protobuffers

Integration of gRPC in python is very straightforward via pip.
But it becomes tricky to integrate gRPC in a C++ project that works cross-platform.
Compiling gRPC from source and linking it properly takes a lot of time and there are tons of errors related to CMake and protobuffers.

In this project, there are two ways to build the C++ client: install gRPC via vcpkg or conan.
The former is very easy to setup and it takes a while (10~30 min) because vcpkg will build gRPC from source.
The later just downloads binaries from conan-center and you don't need to build the libraries from source.
So it's fast; but it may take a few minutes to set conan up on your machine.

**NOTE**: If you choose to install gRPC via vcpkg, please change version of grpcio and grpcio-tools to `1.54.2` in [requirements.txt](./requirements.txt).
You have to do that because vcpkg cannot **easily** control the version of libraries.
In this case, vcpkg always install gRPC v1.54.2 and we have to adapt the python libraries so they could communicate.

Create a virtual python environment for this project since we need some tools:

``` sh
# create a virtual environment
python3 -m venv venv
# activate the environment
source venv/bin/activate
# install packages
pip install -r requirements.txt
```

## Build the C++ client with conan 1.X

With conan version 1.60, we don't need to use vcpkg to build gRPC which will take a while.
On windows, the build time could be even longer.
Even that build only happens once per machine, I still like to avoid it.

If you use conan for the first time, you need to configure it:

``` sh
# create a default profile
conan profile new --detect default
# change cxx abi for gcc
conan profile update settings.compiler.libcxx=libstdc++11 default
```

See [the profile of my Linux machine](./profile_gcc_11).

Release build:

``` sh
# install libraries for your profile using conan
conan install . -pr:b ./profile_gcc_11 --install-folder=buildRelease
# setup protoc and the plugins to generate messages. You may need to change the path based on yours.
export PROTOC=/home/changjie/.conan/data/protobuf/3.20.0/_/_/package/2dbf65f76c0469903ce48756c39d50cd4e721678/bin/protoc
export GRPC_BIN_DIR=$HOME/.conan/data/grpc/1.40.0/_/_/package/2fcd67741f0ce04977353aa7a750d8f3b68efb6a/bin/
mkdir cppMsg && mkdir pyMsg
# generate messages using protoc from vcpkg
$PROTOC --proto_path=. --grpc_out=cppMsg \
  --plugin=protoc-gen-grpc=$GRPC_BIN_DIR/grpc_cpp_plugin \
  --cpp_out=cppMsg msg.proto
# generate messages for python
$PROTOC --proto_path=. --grpc_python_out=pyMsg \
  --plugin=protoc-gen-grpc_python=$GRPC_BIN_DIR/grpc_python_plugin \
  --python_out=pyMsg msg.proto
cmake --preset release -B buildRelease
cmake --build buildRelease
```

Debug build:

``` sh
conan install . -pr:b ./profile_gcc_11 -s build_type=Debug --install-folder=buildDebug
cmake --preset debug -B buildDebug
cmake --build buildDebug
```

On Windows it should work similarly, except for the profile.

## Build the C++ client with vcpkg

### Install gRPC via vcpkg

``` sh
export VCPKG_DIR=$HOME/Documents/vcpkg
cd ~/Documents
git clone https://github.com/Microsoft/vcpkg.git
cd vcpkg
./bootstrap-vcpkg.sh
./vcpkg install grpc
```

On Windows, install gRPC:

``` bat
.\vcpkg install grpc:x64-windows
```

### Build the C++ client with vcpkg

``` sh
mkdir cppMsg && mkdir pyMsg
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

On Windows:

``` bat
set VCPKG_DIR=C:\sw\vcpkg-2023.04.15
mkdir cppMsg && mkdir pyMsg
%VCPKG_DIR%/installed/x64-windows/tools/protobuf/protoc --proto_path=. --grpc_out=cppMsg ^
  --plugin=protoc-gen-grpc=%VCPKG_DIR%/installed/x64-windows/tools/grpc/grpc_cpp_plugin.exe ^
  --cpp_out=cppMsg msg.proto
%VCPKG_DIR%/installed/x64-windows/tools/protobuf/protoc --proto_path=. --grpc_python_out=pyMsg ^
  --plugin=protoc-gen-grpc_python=%VCPKG_DIR%/installed/x64-windows/tools/grpc/grpc_python_plugin.exe ^
  --python_out=pyMsg msg.proto
mkdir build && cd build
cmake -DCMAKE_TOOLCHAIN_FILE=%VCPKG_DIR%/scripts/buildsystems/vcpkg.cmake ..
cmake --build . --config Release
cmake --build . --config Debug
```

## Python Server

Copy `pyserver.py` to folder pyMsg and run:

``` sh
ln pyserver.py pyMsg/pyserver.py
cd pyMsg
python pyserver.py
```

## Test with SAM


``` sh
# install pytorch with CPU. Feel free to use a different variant.
# see https://pytorch.org/get-started/locally/
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu
pip install git+https://github.com/facebookresearch/segment-anything.git
pip install opencv-python pycocotools matplotlib onnxruntime onnx
```

Download the [ViT-B SAM model](https://dl.fbaipublicfiles.com/segment_anything/sam_vit_b_01ec64.pth).

``` sh
ln  pyserverSAM.py pyMsg/pyserverSAM.py
python pyMsg/pyseverSAM.py
```

References:

* [Quickstart C++ gRPC](https://grpc.io/docs/languages/cpp/quickstart/)
* [Install gRPC](https://grpc.io/blog/installation/)
* [Announcing out-of-the-box support for gRPC in the Flatbuffers serialization library](https://grpc.io/blog/grpc-flatbuffers/)
* [git submodules - could not get a repository handle for submodule](https://stackoverflow.com/questions/75769128/git-submodules-could-not-get-a-repository-handle-for-submodule)
* [grpc can't find protobuf library](https://stackoverflow.com/questions/62245040/grpc-cant-find-protobuf-library)
* [What is a correct way to setup protobuf and grpc for cpp project?](https://stackoverflow.com/questions/70700592/what-is-a-correct-way-to-setup-protobuf-and-grpc-for-cpp-project)
