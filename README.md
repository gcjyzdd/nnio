# Test Neural Networks IO using gRPC and Protobuffers

## Build Protobuf

``` sh
mkdir buildProto && cd buildProto
cmake ../ext/protobuf -Dprotobuf_BUILD_TESTS=OFF
make protoc -j8
```

Generate messages:

``` sh
mkdir cppMsg && mkdir pyMsg
./buildProto/protoc --proto_path=. --cpp_out=cppMsg --python_out=pyMsg msg.proto
```

## Build


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

* [Install gRPC](https://grpc.io/blog/installation/)
* [Announcing out-of-the-box support for gRPC in the Flatbuffers serialization library](https://grpc.io/blog/grpc-flatbuffers/)
