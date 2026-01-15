import logging
import grpc
from db import db
from generated import rec_pb2
from generated.rec_pb2_grpc import RecommendationServiceServicer


class RecommendationService(RecommendationServiceServicer):
    def ProjectRecommendation(self, request, context):
        """Recommend projects for a user based on their embedding"""
        id = request.id
        try:
            client = db.get_qdrant_client()

            existing = client.retrieve(
                collection_name="users", ids=[id], with_vectors=True
            )
            if not existing:
                context.set_code(grpc.StatusCode.NOT_FOUND)
                context.set_details(f"User {id} does not exist")
                return rec_pb2.RecommendationResponse(success=False, ids=[])

            user_vector = existing[0].vector

            if isinstance(user_vector, dict):
                user_vector = list(user_vector.values())[0]

            logging.info(user_vector)

            response = client.query_points(
                collection_name="projects",
                query=user_vector,
                limit=15,
            )

            ids = []

            for point in response.points:
                logging.info(point)
                ids.append(point.id)

            return rec_pb2.RecommendationResponse(success=True, ids=ids)

        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(
                f"Failed to retrieve project recommendation -> {str(e)}"
            )
            return rec_pb2.RecommendationResponse(success=False, ids=[])

    def UserRecommendation(self, request, context):
        """Recommend users for a project based on their embedding"""
        id = request.id
        try:
            client = db.get_qdrant_client()

            existing = client.retrieve(collection_name="projects", ids=[id])
            if not existing:
                context.set_code(grpc.StatusCode.NOT_FOUND)
                context.set_details(f"Project {id} does not exist")
                return rec_pb2.RecommendationResponse(success=False, ids=[])

            project_vector = existing[0].vector

            if isinstance(project_vector, dict):
                project_vector = list(project_vector.values())[0]

            logging.info(project_vector)

            response = client.query_points(
                collection_name="users", query=project_vector, limit=15
            )

            ids = []

            for point in response.points:
                logging.info(point)
                ids.append(point.id)

            return rec_pb2.RecommendationResponse(success=True, ids=ids)

        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(f"Failed to retrieve user recommendation -> {str(e)}")
            return rec_pb2.RecommendationResponse(success=False, ids=[])
