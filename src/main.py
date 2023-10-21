from database.data_load import read_from_csv
from database.create_collection import create_milvus_collection, connect_milvusdb
from src.data_processing.data_preprocess import apply_basic_preprocess
from src.data_processing.data_postprocess import apply_basic_postprocess
from towhee import ops, pipe, DataCollection
from src.utils.params import PARAMS


def load_data_to_milvus(path=None):

    # Read data from csv file
    df_orj = read_from_csv(path)
    print("Done: Data read from CSV file.")

    # Data preprocessing
    df = apply_basic_preprocess(df_input=df_orj)
    print("Done: Data preprocessin.g")

    # Create MilvusDB Collection
    connect_milvusdb()
    collection = create_milvus_collection(PARAMS.DATABASE.COLLECTION_NAME,
                                          PARAMS.MODEL.DIMENTION)
    print("Done: Collection created.")

    # Create Towhee pipelines to embed and insert data to DB
    emb_pipe = (
        pipe.input('df')
            .flat_map('df', 'index', lambda df: df['index'])
            .flat_map('df', 'data', lambda df: df['JobDescription'].values.tolist())
        .map('data', 'embeddings', ops.sentence_embedding.transformers(model_name=PARAMS.MODEL.NAME))
    )

    insert_pipe = (
        emb_pipe.map(('index', 'data', 'embeddings'), 'res',
                     ops.ann_insert.milvus_client(
            host=PARAMS.NETWORK.HOST,
            port=PARAMS.NETWORK.PORT,
            collection_name=PARAMS.DATABASE.COLLECTION_NAME
        ))
        .output('res')
    )
    print("Done: Pipelines created.")

    # Insert data
    insert_pipe(df)
    print("Done: Data moved to MilvusDB.")


def search(user_input):
    # Search pipeline created
    search_pipe = (pipe.input('query')
                   .map('query', 'vec',
                        ops.sentence_embedding.transformers(model_name=PARAMS.MODEL.NAME))
                   .flat_map('vec', 'rows',
                             ops.ann_search.milvus_client(
                                 host=PARAMS.NETWORK.HOST,
                                 port=PARAMS.NETWORK.PORT,
                                 collection_name=PARAMS.DATABASE.COLLECTION_NAME,
                                 output_fields=['search_job_in_milvus', 'job_detail']))
                   .map('rows', ('id', 'score', 'search_job_in_milvus', 'job_detail'), lambda x: (x[0], x[1], x[2], x[3]))
                   .output('id', 'job_detail', 'score', 'search_job_in_milvus')
                   )

    # Prediction made
    res = search_pipe(user_input)
    res_dict = DataCollection(res).to_dict()
    res_df = apply_basic_postprocess(res_dict)
    return res_df


# search('Are you eager to roll up your sleeves and harn')
# load_data_to_milvus()
