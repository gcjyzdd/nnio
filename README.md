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

Then start the C++ client:

``` sh
./buildRelease/bin/sam_client
```

References:

* [Quickstart C++ gRPC](https://grpc.io/docs/languages/cpp/quickstart/)
* [Install gRPC](https://grpc.io/blog/installation/)
* [Announcing out-of-the-box support for gRPC in the Flatbuffers serialization library](https://grpc.io/blog/grpc-flatbuffers/)
* [git submodules - could not get a repository handle for submodule](https://stackoverflow.com/questions/75769128/git-submodules-could-not-get-a-repository-handle-for-submodule)
* [grpc can't find protobuf library](https://stackoverflow.com/questions/62245040/grpc-cant-find-protobuf-library)
* [What is a correct way to setup protobuf and grpc for cpp project?](https://stackoverflow.com/questions/70700592/what-is-a-correct-way-to-setup-protobuf-and-grpc-for-cpp-project)
