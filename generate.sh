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
