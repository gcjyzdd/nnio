#include "msg.grpc.pb.h"
#include "msg.pb.h"
#include <grpcpp/grpcpp.h>
#include <iostream>

using grpc::Channel;
using grpc::ClientContext;
using grpc::Status;

class InferenceClientTest {
public:
  explicit InferenceClientTest(std::shared_ptr<Channel> channel)
      : m_stub(InferenceSamTest::NewStub(channel)) {}

  MaskReplyTest const &query(std::string const &data) {
    ImageRequest req;
    req.set_width(100);
    req.set_height(100);
    // assign the image
    req.set_data(data);

    if (Status status = m_stub->Inference(&m_context, req, &m_reply);
        !status.ok()) {
      throw std::invalid_argument(
          "Cannot inference via gRPC! Check if the server is running.");
    }
    return m_reply;
  }

private:
  ClientContext m_context;
  std::unique_ptr<InferenceSamTest::Stub> m_stub;

  MaskReplyTest m_reply;
};

int main() {
  InferenceClientTest client(grpc::CreateChannel(
      "localhost:50051", grpc::InsecureChannelCredentials()));
  std::string img(3, ' ');
  img[0] = 0xFF;
  img[1] = 155U;
  img[2] = 10U;
  const auto &result = client.query(img);
  std::cout << "Mask length = " << result.length() << std::endl;
  return 0;
}
