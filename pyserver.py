from concurrent import futures
import logging
import grpc

import msg_pb2
import msg_pb2_grpc


class InferenceServerTest(msg_pb2_grpc.InferenceSamTestServicer):
    def Inference(self, request: msg_pb2.ImageRequest, context):
        print('first pixel %d' % request.data[0])
        return msg_pb2.MaskReplyTest(length=10)


def serve():
    port = '50051'
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    msg_pb2_grpc.add_InferenceSamServicer_to_server(
        InferenceServerTest(), server)
    rp = '[::]:' + port
    server.add_insecure_port(rp)
    server.start()
    print("Server started, listening on " + port)
    server.wait_for_termination()


if __name__ == '__main__':
    logging.basicConfig()
    serve()
