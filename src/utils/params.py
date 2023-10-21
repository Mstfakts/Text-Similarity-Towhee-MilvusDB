class PARAMS:

    class NETWORK:
        # Network parameters
        HOST = 'standalone'
        PORT = '19530'

    class MODEL:
        # Embedding model parameters
        DIMENTION = 768
        NAME = 'sentence-transformers/paraphrase-albert-small-v2'

    class DATABASE:
        # Database parameters
        COLLECTION_NAME = 'search_job_in_milvus'

    class DATA:
        CSV_PATH = '/app/data/DataAnalyst.csv'
