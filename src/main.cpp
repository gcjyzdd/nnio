#include "msg.grpc.pb.h"
#include "msg.pb.h"
#include <grpcpp/grpcpp.h>
#include <iostream>
#include <stb/stb_image.h>

using grpc::Channel;
using grpc::ClientContext;
using grpc::Status;

class InferenceClient
{
   public:
    explicit InferenceClient(std::shared_ptr<Channel> channel) : m_stub(InferenceSam::NewStub(channel))
    {
    }

    MaskReply const &query(int w, int h, std::string data)
    {
        ImageRequest req;
        req.set_width(w);
        req.set_height(h);
        // assign the image
        req.set_data(std::move(data));

        if (Status status = m_stub->Inference(&m_context, req, &m_reply); !status.ok())
        {
            throw std::invalid_argument("Cannot inference via gRPC! Check if the server is running.");
        }
        return m_reply;
    }

   private:
    ClientContext                       m_context;
    std::unique_ptr<InferenceSam::Stub> m_stub;

    MaskReply m_reply;
};

int main()
{
    grpc::ChannelArguments args{};
    args.SetMaxReceiveMessageSize(-1);
    // args.SetInt(GRPC_ARG_MAX_RECEIVE_MESSAGE_LENGTH, 64 * 1024 * 1024);

    InferenceClient client(grpc::CreateCustomChannel("localhost:50051", grpc::InsecureChannelCredentials(), args));

    int w{};
    int h{};
    int c{};

    auto       *data = stbi_load("./dog.jpg", &w, &h, &c, 3);
    std::string image(reinterpret_cast<const char *>(data), w * h * c);

    const auto &result = client.query(w, h, image);
    std::cout << "Mask length = " << result.masks_size() << std::endl;
    stbi_image_free(data);
    return 0;
}
