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

            existing = client.retrieve(collection_name="users", ids=[id])
            if not existing:
                context.set_code(grpc.StatusCode.NOT_FOUND)
                context.set_details(f"User {id} does not exist")
                return rec_pb2.RecommendationResponse(success=False, ids=[])

            user_vector = existing[0].vector

        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(
                f"Failed to retrieve project recommendation -> {str(e)}"
            )
            return rec_pb2.RecommendationResponse(success=False, ids=[])
