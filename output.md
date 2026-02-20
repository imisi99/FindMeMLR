This file is a merged representation of the entire codebase, combined into a single document by Repomix.

# File Summary

## Purpose
This file contains a packed representation of the entire repository's contents.
It is designed to be easily consumable by AI systems for analysis, code review,
or other automated processes.

## File Format
The content is organized as follows:
1. This summary section
2. Repository information
3. Directory structure
4. Repository files (if enabled)
5. Multiple file entries, each consisting of:
  a. A header with the file path (## File: path/to/file)
  b. The full contents of the file in a code block

## Usage Guidelines
- This file should be treated as read-only. Any changes should be made to the
  original repository files, not this packed version.
- When processing this file, use the file path to distinguish
  between different files in the repository.
- Be aware that this file may contain sensitive information. Handle it with
  the same level of security as you would the original repository.

## Notes
- Some files may have been excluded based on .gitignore rules and Repomix's configuration
- Binary files are not included in this packed representation. Please refer to the Repository Structure section for a complete list of file paths, including binary files
- Files matching patterns in .gitignore are excluded
- Files matching default ignore patterns are excluded
- Files are sorted by Git change count (files with more changes are at the bottom)

# Directory Structure
```
db/
  db.py
generated/
  rec_pb2_grpc.py
  rec_pb2.py
  rec_pb2.pyi
proto/
  rec.proto
services/
  rec.py
.gitignore
docker-compose.yml
Dockerfile
generate.sh
LICENSE
main.py
README.md
requirements.txt
```

# Files

## File: README.md
```markdown
****FINDMEMLR****
```

## File: .gitignore
```
# Byte-compiled / optimized / DLL files
__pycache__/
*.py[codz]
*$py.class

# C extensions
*.so

# Distribution / packaging
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
share/python-wheels/
*.egg-info/
.installed.cfg
*.egg
MANIFEST

# PyInstaller
#  Usually these files are written by a python script from a template
#  before PyInstaller builds the exe, so as to inject date/other infos into it.
*.manifest
*.spec

# Installer logs
pip-log.txt
pip-delete-this-directory.txt

# Unit test / coverage reports
htmlcov/
.tox/
.nox/
.coverage
.coverage.*
.cache
nosetests.xml
coverage.xml
*.cover
*.py.cover
.hypothesis/
.pytest_cache/
cover/

# Translations
*.mo
*.pot

# Django stuff:
*.log
local_settings.py
db.sqlite3
db.sqlite3-journal

# Flask stuff:
instance/
.webassets-cache

# Scrapy stuff:
.scrapy

# Sphinx documentation
docs/_build/

# PyBuilder
.pybuilder/
target/

# Jupyter Notebook
.ipynb_checkpoints

# IPython
profile_default/
ipython_config.py

# pyenv
#   For a library or package, you might want to ignore these files since the code is
#   intended to run in multiple environments; otherwise, check them in:
# .python-version

# pipenv
#   According to pypa/pipenv#598, it is recommended to include Pipfile.lock in version control.
#   However, in case of collaboration, if having platform-specific dependencies or dependencies
#   having no cross-platform support, pipenv may install dependencies that don't work, or not
#   install all needed dependencies.
#Pipfile.lock

# UV
#   Similar to Pipfile.lock, it is generally recommended to include uv.lock in version control.
#   This is especially recommended for binary packages to ensure reproducibility, and is more
#   commonly ignored for libraries.
#uv.lock

# poetry
#   Similar to Pipfile.lock, it is generally recommended to include poetry.lock in version control.
#   This is especially recommended for binary packages to ensure reproducibility, and is more
#   commonly ignored for libraries.
#   https://python-poetry.org/docs/basic-usage/#commit-your-poetrylock-file-to-version-control
#poetry.lock
#poetry.toml

# pdm
#   Similar to Pipfile.lock, it is generally recommended to include pdm.lock in version control.
#   pdm recommends including project-wide configuration in pdm.toml, but excluding .pdm-python.
#   https://pdm-project.org/en/latest/usage/project/#working-with-version-control
#pdm.lock
#pdm.toml
.pdm-python
.pdm-build/

# pixi
#   Similar to Pipfile.lock, it is generally recommended to include pixi.lock in version control.
#pixi.lock
#   Pixi creates a virtual environment in the .pixi directory, just like venv module creates one
#   in the .venv directory. It is recommended not to include this directory in version control.
.pixi

# PEP 582; used by e.g. github.com/David-OConnor/pyflow and github.com/pdm-project/pdm
__pypackages__/

# Celery stuff
celerybeat-schedule
celerybeat.pid

# SageMath parsed files
*.sage.py

# Environments
.env
.envrc
.venv
env/
venv/
ENV/
env.bak/
venv.bak/

# Spyder project settings
.spyderproject
.spyproject

# Rope project settings
.ropeproject

# mkdocs documentation
/site

# mypy
.mypy_cache/
.dmypy.json
dmypy.json

# Pyre type checker
.pyre/

# pytype static type analyzer
.pytype/

# Cython debug symbols
cython_debug/

# PyCharm
#  JetBrains specific template is maintained in a separate JetBrains.gitignore that can
#  be found at https://github.com/github/gitignore/blob/main/Global/JetBrains.gitignore
#  and can be added to the global gitignore or merged into this file.  For a more nuclear
#  option (not recommended) you can uncomment the following to ignore the entire idea folder.
#.idea/

# Abstra
# Abstra is an AI-powered process automation framework.
# Ignore directories containing user credentials, local state, and settings.
# Learn more at https://abstra.io/docs
.abstra/

# Visual Studio Code
#  Visual Studio Code specific template is maintained in a separate VisualStudioCode.gitignore 
#  that can be found at https://github.com/github/gitignore/blob/main/Global/VisualStudioCode.gitignore
#  and can be added to the global gitignore or merged into this file. However, if you prefer, 
#  you could uncomment the following to ignore the entire vscode folder
# .vscode/

# Ruff stuff:
.ruff_cache/

# PyPI configuration file
.pypirc

# Cursor
#  Cursor is an AI-powered code editor. `.cursorignore` specifies files/directories to
#  exclude from AI features like autocomplete and code analysis. Recommended for sensitive data
#  refer to https://docs.cursor.com/context/ignore-files
.cursorignore
.cursorindexingignore

# Marimo
marimo/_static/
marimo/_lsp/
__marimo__/
```

## File: Dockerfile
```dockerfile
FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

RUN chmod +x generate.sh && ./generate.sh

EXPOSE 8050

CMD [ "python", "main.py" ]
```

## File: generate.sh
```bash
#!/bin/bash

set -e

python -m grpc_tools.protoc \
  -I proto \
  --python_out=generated \
  --pyi_out=generated \
  --grpc_python_out=generated \
  proto/rec.proto

# Fixing the import path to be relative
sed -i 's/^import rec_pb2 as/from . import rec_pb2 as/' generated/rec_pb2_grpc.py

echo "Proto files generated successfully"
```

## File: LICENSE
```
MIT License

Copyright (c) 2025 Imisioluwa Isong

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

## File: requirements.txt
```
qdrant_client==1.16.2
requests==2.32.5
grpcio==1.76.0
grpcio-tools==1.76.0
grpcio-reflection==1.76.0
```

## File: db/db.py
```python
import os
import logging
from typing import Optional
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams

VECTOR_SIZE = 768
QDRANT_HOST = os.getenv("QDRANT_HOST")
QDRANT_PORT = int(os.getenv("QDRANT_PORT", 6333))
QDRANT_CLIENT: Optional[QdrantClient] = None


def qdrant_client_connect() -> QdrantClient:
    client = QdrantClient(host=QDRANT_HOST, port=QDRANT_PORT)
    return client


def ensure_collections(client: QdrantClient):
    collections = client.get_collections().collections
    existing = {c.name for c in collections}

    if "users" not in existing:
        logging.info("[QDRANT] Creating users collections as it did not exist.")

        try:
            client.create_collection(
                collection_name="users",
                vectors_config={
                    "profile": VectorParams(size=VECTOR_SIZE, distance=Distance.COSINE),
                },
            )
            logging.info("[QDRANT] Users collection created.")
        except Exception as e:
            logging.error("[QDRANT] Failed to create the users collection -> %s", e)

    if "projects" not in existing:
        logging.info("[QDRANT] Creating projects collections as it did not exist.")

        try:
            client.create_collection(
                collection_name="projects",
                vectors_config={
                    "description": VectorParams(
                        size=VECTOR_SIZE, distance=Distance.COSINE
                    )
                },
            )
            logging.info("[QDRANT] Projects collection created.")
        except Exception as e:
            logging.error("[QDRANT] Failed to create the project collection. -> %s", e)
            raise


def get_qdrant_client() -> QdrantClient:
    """Returns a pre-initialized qdrant client"""
    if QDRANT_CLIENT is None:
        raise RuntimeError("[QDRANT] Qdrant Client not initialized.")
    return QDRANT_CLIENT
```

## File: generated/rec_pb2.pyi
```
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class RecommendationRequest(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class RecommendationResponse(_message.Message):
    __slots__ = ("success", "res")
    class ResEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: float
        def __init__(self, key: _Optional[str] = ..., value: _Optional[float] = ...) -> None: ...
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    RES_FIELD_NUMBER: _ClassVar[int]
    success: bool
    res: _containers.ScalarMap[str, float]
    def __init__(self, success: bool = ..., res: _Optional[_Mapping[str, float]] = ...) -> None: ...
```

## File: docker-compose.yml
```yaml
services:
  rec:
    build:
      context: .
      dockerfile: Dockerfile
    container_name: findme_rec
    restart: always
    environment:
      - QDRANT_HOST=${QDRANT_HOST}
      - QDRANT_PORT=${QDRANT_PORT}
    networks:
      - findme-shared-network

networks:
  findme-shared-network:
    external: true
```

## File: main.py
```python
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

# TODO:
# The project should have a user id to prevent it from recommending the curr user projects
# (This would be implemented in the emb service first) then filter on search here.


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
```

## File: generated/rec_pb2_grpc.py
```python
# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc
import warnings

from . import rec_pb2 as rec__pb2

GRPC_GENERATED_VERSION = '1.76.0'
GRPC_VERSION = grpc.__version__
_version_not_supported = False

try:
    from grpc._utilities import first_version_is_lower
    _version_not_supported = first_version_is_lower(GRPC_VERSION, GRPC_GENERATED_VERSION)
except ImportError:
    _version_not_supported = True

if _version_not_supported:
    raise RuntimeError(
        f'The grpc package installed is at version {GRPC_VERSION},'
        + ' but the generated code in rec_pb2_grpc.py depends on'
        + f' grpcio>={GRPC_GENERATED_VERSION}.'
        + f' Please upgrade your grpc module to grpcio>={GRPC_GENERATED_VERSION}'
        + f' or downgrade your generated code using grpcio-tools<={GRPC_VERSION}.'
    )


class RecommendationServiceStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.ProjectRecommendation = channel.unary_unary(
                '/rec.RecommendationService/ProjectRecommendation',
                request_serializer=rec__pb2.RecommendationRequest.SerializeToString,
                response_deserializer=rec__pb2.RecommendationResponse.FromString,
                _registered_method=True)
        self.UserRecommendation = channel.unary_unary(
                '/rec.RecommendationService/UserRecommendation',
                request_serializer=rec__pb2.RecommendationRequest.SerializeToString,
                response_deserializer=rec__pb2.RecommendationResponse.FromString,
                _registered_method=True)


class RecommendationServiceServicer(object):
    """Missing associated documentation comment in .proto file."""

    def ProjectRecommendation(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def UserRecommendation(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_RecommendationServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'ProjectRecommendation': grpc.unary_unary_rpc_method_handler(
                    servicer.ProjectRecommendation,
                    request_deserializer=rec__pb2.RecommendationRequest.FromString,
                    response_serializer=rec__pb2.RecommendationResponse.SerializeToString,
            ),
            'UserRecommendation': grpc.unary_unary_rpc_method_handler(
                    servicer.UserRecommendation,
                    request_deserializer=rec__pb2.RecommendationRequest.FromString,
                    response_serializer=rec__pb2.RecommendationResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'rec.RecommendationService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))
    server.add_registered_method_handlers('rec.RecommendationService', rpc_method_handlers)


 # This class is part of an EXPERIMENTAL API.
class RecommendationService(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def ProjectRecommendation(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/rec.RecommendationService/ProjectRecommendation',
            rec__pb2.RecommendationRequest.SerializeToString,
            rec__pb2.RecommendationResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def UserRecommendation(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/rec.RecommendationService/UserRecommendation',
            rec__pb2.RecommendationRequest.SerializeToString,
            rec__pb2.RecommendationResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)
```

## File: generated/rec_pb2.py
```python
# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# NO CHECKED-IN PROTOBUF GENCODE
# source: rec.proto
# Protobuf Python Version: 6.31.1
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import runtime_version as _runtime_version
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
_runtime_version.ValidateProtobufRuntimeVersion(
    _runtime_version.Domain.PUBLIC,
    6,
    31,
    1,
    '',
    'rec.proto'
)
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\trec.proto\x12\x03rec\"#\n\x15RecommendationRequest\x12\n\n\x02id\x18\x01 \x01(\t\"\x88\x01\n\x16RecommendationResponse\x12\x0f\n\x07success\x18\x01 \x01(\x08\x12\x31\n\x03res\x18\x02 \x03(\x0b\x32$.rec.RecommendationResponse.ResEntry\x1a*\n\x08ResEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\x02:\x02\x38\x01\x32\xb8\x01\n\x15RecommendationService\x12P\n\x15ProjectRecommendation\x12\x1a.rec.RecommendationRequest\x1a\x1b.rec.RecommendationResponse\x12M\n\x12UserRecommendation\x12\x1a.rec.RecommendationRequest\x1a\x1b.rec.RecommendationResponseB\x07Z\x05./recb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'rec_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  _globals['DESCRIPTOR']._loaded_options = None
  _globals['DESCRIPTOR']._serialized_options = b'Z\005./rec'
  _globals['_RECOMMENDATIONRESPONSE_RESENTRY']._loaded_options = None
  _globals['_RECOMMENDATIONRESPONSE_RESENTRY']._serialized_options = b'8\001'
  _globals['_RECOMMENDATIONREQUEST']._serialized_start=18
  _globals['_RECOMMENDATIONREQUEST']._serialized_end=53
  _globals['_RECOMMENDATIONRESPONSE']._serialized_start=56
  _globals['_RECOMMENDATIONRESPONSE']._serialized_end=192
  _globals['_RECOMMENDATIONRESPONSE_RESENTRY']._serialized_start=150
  _globals['_RECOMMENDATIONRESPONSE_RESENTRY']._serialized_end=192
  _globals['_RECOMMENDATIONSERVICE']._serialized_start=195
  _globals['_RECOMMENDATIONSERVICE']._serialized_end=379
# @@protoc_insertion_point(module_scope)
```

## File: proto/rec.proto
```protobuf
syntax="proto3";

package rec;

option go_package = "./rec";

service RecommendationService {
  rpc ProjectRecommendation(RecommendationRequest) returns (RecommendationResponse);
  rpc UserRecommendation(RecommendationRequest) returns (RecommendationResponse);
}

message RecommendationRequest {
  string id = 1;
}

message RecommendationResponse {
  bool success = 1;
  map<string, float> res = 2;
}
```

## File: services/rec.py
```python
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
```
