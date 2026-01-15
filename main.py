from concurrent import futures
import grpc
import logging

from db import db
from services.rec import RecommendationService
from generated import rec_pb2, rec_pb2_grpc
from grpc_reflection.v1alpha import reflection

logging.basicConfig(
    level=logging.INFO,
    format="{asctime} [{levelname}] {message}",
    style="{",
)


def serve():
    db.QDRANT_CLIENT = db.qdrant_client_connect()
    db.ensure_collections(db.QDRANT_CLIENT)

    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

    rec_pb2_grpc.add_RecommendationServiceServicer_to_server(
        RecommendationService(), server
    )

    SERVICE_NAMES = (
        rec_pb2.DESCRIPTOR.services_by_name["RecommendationService"].full_name,
        reflection.SERVICE_NAME,
    )

    reflection.enable_server_reflection(SERVICE_NAMES, server)

    server.add_insecure_port("[::]:8050")
    server.start()
    logging.info("[gRPC rec] The recommendation service is up and running on port 8050")
    server.wait_for_termination()


serve()
