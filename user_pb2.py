# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: user.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\nuser.proto\x12\x04\x62\x65\x61m\"\x89\x01\n\x04User\x12\x14\n\x07user_id\x18\x01 \x01(\tH\x00\x88\x01\x01\x12\x18\n\x07\x66\x65\x61ture\x18\x02 \x01(\tB\x02\x18\x01H\x01\x88\x01\x01\x12(\n\x0c\x66\x65\x61ture_enum\x18\x03 \x01(\x0e\x32\r.beam.FeatureH\x02\x88\x01\x01\x42\n\n\x08_user_idB\n\n\x08_featureB\x0f\n\r_feature_enum*<\n\x07\x46\x65\x61ture\x12\x13\n\x0f\x46\x45\x41TURE_UNKNOWN\x10\x00\x12\r\n\tFEATURE_A\x10\x01\x12\r\n\tFEATURE_B\x10\x02\x62\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'user_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _USER.fields_by_name['feature']._options = None
  _USER.fields_by_name['feature']._serialized_options = b'\030\001'
  _FEATURE._serialized_start=160
  _FEATURE._serialized_end=220
  _USER._serialized_start=21
  _USER._serialized_end=158
# @@protoc_insertion_point(module_scope)
