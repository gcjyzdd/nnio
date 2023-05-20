# Test Neural Networks IO using gRPC and Protobuffers

## Build Protobuf

We could skip this step because gRPC automatically builds protobuf.

``` sh
export MY_INSTALL_DIR=$HOME/grpc
mkdir -p $MY_INSTALL_DIR
mkdir buildProto && cd buildProto
cmake ../ext/protobuf -Dprotobuf_BUILD_TESTS=OFF
make protoc -j8
make install
```

Generate messages:

``` sh
mkdir cppMsg && mkdir pyMsg
./buildProto/protoc --proto_path=. --cpp_out=cppMsg --python_out=pyMsg msg.proto
```

## Install gRPC

``` sh
export MY_INSTALL_DIR=$HOME/grpc
mkdir -p $MY_INSTALL_DIR
cd ~/Download
git clone --recurse-submodules -b v1.55.0 --depth 1 --shallow-submodules https://github.com/grpc/grpc
cd grpc
mkdir -p cmake/build
cd cmake/build
cmake -DgRPC_INSTALL=ON \
      -DgRPC_BUILD_TESTS=OFF \
      -DCMAKE_INSTALL_PREFIX=$MY_INSTALL_DIR \
      ../..
make -j 12
make install
```

## Build


``` sh
mkdir build && cd build
cmake -DCMAKE_PREFIX_PATH=$MY_INSTALL_DIR ..
```

[Install gRPC](https://github.com/grpc/grpc/blob/v1.55.0/src/cpp/README.md).

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
