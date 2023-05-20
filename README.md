# Test Neural Networks IO using Flask and Flatbuffers

``` sh
mkdir build && cd build
cmake ../ext/flatbuffers
make flatc -j8
cd ..
# generate messages for python
./build/flatc -p -o pymsg msg.fbs
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

* [Install gRPC](https://grpc.io/blog/installation/)
