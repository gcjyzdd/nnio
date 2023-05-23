from concurrent import futures
import logging
import grpc

import msg_pb2
import msg_pb2_grpc

from segment_anything import SamAutomaticMaskGenerator, sam_model_registry
import cv2

model_type = "vit_b"

sam = sam_model_registry[model_type](checkpoint="./sam_vit_b_01ec64.pth")
mask_generator = SamAutomaticMaskGenerator(sam)


class InferenceServer(msg_pb2_grpc.InferenceSamServicer):
    def Inference(self, request: msg_pb2.ImageRequest, context):
        image = cv2.imread('./dog.jpg')
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        logging.info("start inference")
        masks = mask_generator.generate(image)
        logging.info("end inference")
        logging.info('first pixel %d' % request.data[0])
        return msg_pb2.MaskReply(length=10)


def serve():
    port = '50051'
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    msg_pb2_grpc.add_InferenceSamServicer_to_server(InferenceServer(), server)
    rp = '[::]:' + port
    server.add_insecure_port(rp)
    server.start()
    logging.info("Server started, listening on " + port)
    server.wait_for_termination()


if __name__ == '__main__':
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[
            logging.FileHandler("debug.log"),
            logging.StreamHandler()
        ]
    )
    serve()
