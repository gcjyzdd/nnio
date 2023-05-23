# Test Neural Networks IO using gRPC and Protobuffers

## Install gRPC via vcpkg

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

## Build the C++ client

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

Create a virtual python environment:

``` sh
# create a virtual environment
python3 -m venv venv
# activate the environment
source venv/bin/activate
# install packages
pip install -r requirements.txt
```

Then copy `pyserver.py` to folder pyMsg and run:

``` sh
ln pyserver.py pyMsg/pyserver.py
cd pyMsg
python pyserver.py
```

## Test with SAM


``` sh
# install pytorch with CPU
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
