from concurrent import futures
import logging
import grpc

import msg_pb2
import msg_pb2_grpc

from segment_anything import SamAutomaticMaskGenerator, sam_model_registry
import cv2
import numpy as np

MAX_MESSAGE_LENGTH = 64*1024*2014

model_type = "vit_b"

sam = sam_model_registry[model_type](checkpoint="./sam_vit_b_01ec64.pth")
mask_generator = SamAutomaticMaskGenerator(sam)


class InferenceServer(msg_pb2_grpc.InferenceSamServicer):
    def Inference(self, request: msg_pb2.ImageRequest, context):
        # image = cv2.imread('./dog.jpg')
        # image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image = np.frombuffer(request.data, dtype=np.uint8).reshape(
            (request.height, request.width, 3))

        logging.info("start inference")
        masks = mask_generator.generate(image)
        logging.info("end inference")
        logging.info('w={}, h={}, first pixel {}'.format(
            request.width, request.height, request.data[0]))

        reply = msg_pb2.MaskReply()
        reply.w = request.width
        reply.h = request.height
        for m in masks:
            mask = reply.masks.add()
            mask.area = m['area']
            mask.bbox.x = m['bbox'][0]
            mask.bbox.y = m['bbox'][1]
            mask.bbox.w = m['bbox'][2]
            mask.bbox.h = m['bbox'][3]

            # append np.bool_ array
            for i in range(reply.h):
                mask.data.extend(
                    map(lambda x: x is np.bool_(True), m['segmentation'][i]))
            mask.iou = m['predicted_iou']
            # TODO: fill more data

        return reply


def serve():
    port = '50051'
    # https://stackoverflow.com/questions/42629047/how-to-increase-message-size-in-grpc-using-python
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=4),
                         options=[
        ('grpc.max_send_message_length', MAX_MESSAGE_LENGTH),
        ('grpc.max_receive_message_length', MAX_MESSAGE_LENGTH),
    ],)
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
