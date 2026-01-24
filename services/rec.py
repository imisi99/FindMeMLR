import logging
import grpc
from qdrant_client.models import FieldCondition, Filter, HasIdCondition, MatchValue
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
                logging.info(f"Failed to retrieve user with id -> {id}, not found")
                context.set_code(grpc.StatusCode.NOT_FOUND)
                context.set_details(f"User {id} does not exist")
                return rec_pb2.RecommendationResponse(success=False, res={})

            user_vector = existing[0].vector

            if user_vector is None:
                logging.info(f"User with id -> {id} exists but the vector doesn't")
                context.set_code(grpc.StatusCode.NOT_FOUND)
                context.set_details(f"User {id} exists but the vector doesn't")
                return rec_pb2.RecommendationResponse(success=False, res={})

            if isinstance(user_vector, dict):
                user_vector = user_vector.get("profile")
                if user_vector is None:
                    logging.info(f"User with id -> {id} has no named vector 'user'")
                    context.set_code(grpc.StatusCode.NOT_FOUND)
                    context.set_details(f"User {id} has no named vector 'user'")
                    return rec_pb2.RecommendationResponse(success=False, res={})

            response = client.query_points(
                collection_name="projects",
                query=user_vector,
                using="description",
                limit=15,
                query_filter=Filter(
                    must_not=[
                        FieldCondition(key="user_id", match=MatchValue(value=id))
                    ],
                    must=[FieldCondition(key="status", match=MatchValue(value=True))],
                ),
            )

            avg_score = 0
            res = {}

            for point in response.points:
                res[point.id] = point.score
                avg_score += point.score

            if len(res) != 0:
                avg_score /= len(res)

            logging.info(
                f"Recommended {len(res)} projects for user with an average score of {avg_score}"
            )
            return rec_pb2.RecommendationResponse(success=True, res=res)

        except Exception as e:
            logging.error(
                f"An error occured while trying to recommend projects for user with id -> {id}, err -> {str(e)}"
            )
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(
                f"Failed to retrieve project recommendation -> {str(e)}"
            )
            return rec_pb2.RecommendationResponse(success=False, res={})

    def UserRecommendation(self, request, context):
        """Recommend users for a project based on their embedding"""
        id = request.id
        try:
            client = db.get_qdrant_client()

            existing = client.retrieve(
                collection_name="projects",
                ids=[id],
                with_vectors=True,
                with_payload=True,
            )
            if not existing:
                logging.info(f"Failed to retrieve project with id -> {id}, not found")
                context.set_code(grpc.StatusCode.NOT_FOUND)
                context.set_details(f"Project {id} does not exist")
                return rec_pb2.RecommendationResponse(success=False, res={})

            project = existing[0]
            project_vector = project.vector

            user_id = project.payload.get("user_id") if project.payload else None

            if user_id is None:
                user_id = ""

            if project_vector is None:
                logging.info(f"User with id -> {id} exists but the vector doesn't")
                context.set_code(grpc.StatusCode.NOT_FOUND)
                context.set_details(f"User {id} exists but the vector doesn't")
                return rec_pb2.RecommendationResponse(success=False, res={})

            if isinstance(project_vector, dict):
                project_vector = project_vector.get("description")
                if project_vector is None:
                    logging.info(
                        f"Project with id -> {id} has no named vector 'description'"
                    )
                    context.set_code(grpc.StatusCode.NOT_FOUND)
                    context.set_details(f"User {id} has no named vector 'user'")
                    return rec_pb2.RecommendationResponse(success=False, res={})

            response = client.query_points(
                collection_name="users",
                query=project_vector,
                using="profile",
                limit=15,
                query_filter=Filter(
                    must_not=[HasIdCondition(has_id=[user_id])],
                    must=[FieldCondition(key="status", match=MatchValue(value=True))],
                ),
            )

            avg_score = 0
            res = {}

            for point in response.points:
                res[point.id] = point.score
                avg_score += point.score

            if len(res) != 0:
                avg_score /= len(res)

            logging.info(
                f"Recommended {len(res)} users for project with an average score of {avg_score}"
            )

            return rec_pb2.RecommendationResponse(success=True, res=res)

        except Exception as e:
            logging.error(
                f"An error occured while trying to recommend users for project with id -> {id}, err -> {str(e)}"
            )
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(f"Failed to retrieve user recommendation -> {str(e)}")
            return rec_pb2.RecommendationResponse(success=False, res={})
