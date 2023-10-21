from pymilvus import connections, FieldSchema, CollectionSchema, DataType, Collection, utility
from src.utils.params import PARAMS


def connect_milvusdb():
    connections.connect(host=PARAMS.NETWORK.HOST,
                        port=PARAMS.NETWORK.PORT)


def create_milvus_collection(collection_name, dim):

    if utility.has_collection(collection_name):
        utility.drop_collection(collection_name)

    fields = [
        FieldSchema(name="index", dtype=DataType.INT64, is_primary=True, auto_id=False),
        FieldSchema(name="job_detail", dtype=DataType.VARCHAR, max_length=500),
        FieldSchema(name="search_job_in_milvus", dtype=DataType.FLOAT_VECTOR, dim=dim)
    ]

    schema = CollectionSchema(fields=fields, description='search_job_in_milvus')
    collection = Collection(name=collection_name, schema=schema)

    index_params = {
        'metric_type': "L2",
        'index_type': "IVF_FLAT",
        'params': {"nlist": 2253}
    }
    collection.create_index(field_name='search_job_in_milvus', index_params=index_params)
    print("Collection yaratıldı")
    return collection
