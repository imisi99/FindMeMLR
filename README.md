# FindMe — Recommendation Service

> A gRPC micro-service that returns ranked user and project recommendations using vector similarity search against a Qdrant vector database.

---

## Overview

This service is part of the FindMe micro-services architecture. It is a read-only service — it does not write or modify any vectors. It queries the Qdrant collections maintained by the [embedding service](https://github.com/imisi99/FindMeML) to find the most semantically similar users or projects for a given query.

The service exposes a single `RecommendationService` with two RPCs and is called directly by the [back-end service](https://github.com/imisi99/FindMe) when a user requests recommendations.

---

## How It Works

**Project recommendations for a user (`ProjectRecommendation`):**

1. Retrieves the user's `profile` vector from the `users` Qdrant collection.
2. Queries the `projects` collection using that vector against the `description` named vector.
3. Filters out projects owned by the requesting user and projects with `status: false`.
4. Returns the top 15 results as a map of `project_id → similarity_score`.

**User recommendations for a project (`UserRecommendation`):**

1. Retrieves the project's `description` vector from the `projects` Qdrant collection, along with its `user_id` payload.
2. Queries the `users` collection using that vector against the `profile` named vector.
3. Filters out the project owner and users with `status: false` (unavailable).
4. Returns the top 15 results as a map of `user_id → similarity_score`.

```
Backend (Go)
    │ gRPC
    ▼
Recommendation Service (Python)
    │ HTTP
    ▼
Qdrant (reads users + projects collections)
```

---

## gRPC API

### RecommendationService

| Method | Request | Response | Description |
|---|---|---|---|
| `ProjectRecommendation` | `RecommendationRequest` | `RecommendationResponse` | Returns ranked projects for a given user ID |
| `UserRecommendation` | `RecommendationRequest` | `RecommendationResponse` | Returns ranked users for a given project ID |

**RecommendationRequest**

```protobuf
message RecommendationRequest {
  string id = 1; // user_id or project_id
}
```

**RecommendationResponse**

```protobuf
message RecommendationResponse {
  bool success = 1;
  map<string, float> res = 2; // id -> similarity score
}
```

gRPC server reflection is enabled — you can inspect the API with `grpcurl` or Postman.

---

## Query Filters

Both RPCs apply the following filters at query time to ensure quality results:

| Filter | ProjectRecommendation | UserRecommendation |
|---|---|---|
| Exclude owner | Projects where `user_id == requesting_user_id` are excluded | The project owner (`user_id` from payload) is excluded |
| Availability | Only projects with `status: true` are returned | Only users with `status: true` are returned |
| Limit | Top 15 results | Top 15 results |

---

## Tech Stack

| Concern | Technology |
|---|---|
| Language | Python 3.12 |
| gRPC Framework | `grpcio` 1.76.0 |
| Vector Database | Qdrant (shared with embedding service) |
| Containerization | Docker + Docker Compose |

---

## Project Structure

```
.
├── db/
│   └── db.py           # Qdrant client init and collection setup
├── generated/          # Auto-generated gRPC code (do not edit)
│   ├── rec_pb2.py
│   ├── rec_pb2_grpc.py
│   └── rec_pb2.pyi
├── proto/
│   └── rec.proto       # Protobuf service definition
├── services/
│   └── rec.py          # RecommendationService implementation
├── docker-compose.yml
├── Dockerfile
├── generate.sh         # Proto code generation script
├── main.py             # Server entrypoint
└── requirements.txt
```

---

## Getting Started

### Prerequisites

- Docker & Docker Compose
- The `findme-shared-network` Docker network must exist
- The Qdrant instance from the embedding service must be running and reachable — this service shares the same Qdrant, it does not run its own

### Environment Variables

Create a `.env` file in the project root:

```env
QDRANT_HOST=qdrant
QDRANT_PORT=6333
```

> The `QDRANT_HOST` should point to the same Qdrant instance used by the embedding service.

### Running with Docker Compose

```bash
# Create the shared network (only needed once)
docker network create findme-shared-network

# Start the recommendation service
docker compose up -d --build
```

The gRPC server will be available at `[::]:8050` on the shared network.

### Running Locally

```bash
pip install -r requirements.txt

# Generate proto files
chmod +x generate.sh && ./generate.sh

# Set env vars and run
QDRANT_HOST=localhost \
QDRANT_PORT=6333 \
python main.py
```

### Regenerating Proto Files

If you modify `proto/rec.proto`:

```bash
chmod +x generate.sh
./generate.sh
```

This regenerates the files in `generated/` and automatically fixes the relative import path in `rec_pb2_grpc.py`.

---

## Deployment Note

This service is intentionally lightweight — it has no Qdrant or Ollama of its own. It depends on the Qdrant instance managed by the embedding service being on the same Docker network. Make sure the embedding service is deployed and its Qdrant has data before this service starts receiving requests.

---

## License

See [LICENSE](./LICENSE).
