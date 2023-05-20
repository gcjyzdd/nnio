# Test Neural Networks IO using Flask and Flatbuffers

``` sh
mkdir build && cd build
cmake ../ext/flatbuffers
make flatc -j8
cd ..
# generate messages for python
./build/flatc -p -o pymsg msg.fbs
```
