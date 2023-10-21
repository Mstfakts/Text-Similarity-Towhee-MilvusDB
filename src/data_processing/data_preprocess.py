def apply_basic_preprocess(df_input):
    df_input['index'] = [x for x in range(0, len(df_input.values))]
    df = df_input.dropna()
    df = df.iloc[0:50]

    for c in df.columns:
        df = df.rename(columns={c: c.replace(" ", "")})

    df['JobDescription'] = df['JobDescription'].str[0:50]
    return df