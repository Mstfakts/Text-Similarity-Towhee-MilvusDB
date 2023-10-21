import pandas as pd


def apply_basic_postprocess(dict_):
    res_df = pd.DataFrame(data=dict_['iterable'], columns=dict_['schema'])
    res_df = res_df.drop([
                            #'query', 
                            'search_job_in_milvus'
                        ], axis=1)
    res_df = res_df.rename(columns={"id": "Database ID", "score": "Distance", "job_detail": "Job Detail"})
    return res_df
