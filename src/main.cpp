#include "msg.grpc.pb.h"
#include "msg.pb.h"
#include <grpcpp/grpcpp.h>
#include <iostream>

using grpc::Channel;
using grpc::ClientContext;
using grpc::Status;

class InferenceClient {
public:
  explicit InferenceClient(std::shared_ptr<Channel> channel)
      : m_stub(InferenceSam::NewStub(channel)) {}

  MaskReply const &query() {
    ImageRequest req;
    req.set_width(100);
    req.set_height(100);
    // assign the image
    // req.set_allocated_data();

    if (Status status = m_stub->Inference(&m_context, req, &m_reply);
        !status.ok()) {
      throw std::invalid_argument(
          "Cannot inference via gRPC! Check if the server is running.");
    }
    return m_reply;
  }

private:
  ClientContext m_context;
  std::unique_ptr<InferenceSam::Stub> m_stub;

  MaskReply m_reply;
};

int main() {
  InferenceClient client(grpc::CreateChannel(
      "testChannel555", grpc::InsecureChannelCredentials()));
  const auto &result = client.query();
  std::cout << "Mask length = " << result.length() << std::endl;
  return 0;
}
