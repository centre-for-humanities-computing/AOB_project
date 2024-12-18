# %%
import pandas as pd
import os
import json

import matplotlib.pyplot as plt
import seaborn as sns

# %%
# test open
with open('output_features/ABO_metrics/english_ABO_metrics.json', 'r') as f:
    data = json.load(f)
df = pd.DataFrame(data['data'], columns=data['columns'], index=data['index'])
df.head()

# %%
# Load the all data & concat
path = 'output_features/ABO_metrics'

big_df = pd.DataFrame()

for file in os.listdir(path):
    if file.endswith(".json"):
        # get the first word of the filename
        language = file.split('_')[0]
        print('\n')

        with open(f"{path}/{file}", "r") as f:
            data = json.load(f)
        data = pd.DataFrame(data['data'], columns=data['columns'], index=data['index'])
        # add lang column
        data['language'] = language
        big_df = pd.concat([big_df, data], axis=0)
        print('len', len(big_df))
        print(big_df.columns)

# %%
# drop duplicates
big_df = big_df.drop_duplicates(subset='story_id')
print(len(big_df))
print(big_df.columns)
big_df.tail()

# %%
# # we want to do a shenanigan here where we get the features of the very short english texts (<300 sentences)
# with open('output_features/ABO_metrics/english_ABO_metrics.json', 'r') as f:
#     data = json.load(f)

# df = pd.DataFrame(data['data'], columns=data['columns'], index=data['index'])
# df = df.drop_duplicates(subset='story_id')
# len(df)


# %%
# now we want to get the story_ids from the original data and add metadata
path_meta = 'data/raw_data/'

dfs = []

for file in os.listdir(f"{path_meta}"):
    if file.endswith(".json") or file.endswith(".jsonl"):
        with open(f"{path_meta}{file}", "r") as f:
            content = f.read()

        json_objects = content.split('\n')

        # Parse each JSON object and collect them into a list
        data = []
        for obj in json_objects:
            if obj.strip():  # Ignore empty lines
                data.append(json.loads(obj))

        df = pd.DataFrame(data)
        dfs.append(df)

print('number of files:', len(dfs))
meta_df = pd.concat(dfs, axis=0)
print(len(meta_df))
print(meta_df.columns)
meta_df.head()


# %%
# merge the dataframes
# make sure storyid column is the same
big_df['story_id'] = big_df['story_id'].astype(int)
meta_df['story_id'] = meta_df['story_id'].astype(int)

# rename the language column in meta_df
meta_df['org_language'] = meta_df['language']
# now drop the language column
meta_df = meta_df.drop(columns='language')

# drop duplicates
meta_df = meta_df.drop_duplicates(subset='story_id')

merged_df = pd.merge(big_df, meta_df, on='story_id', how='inner')
print(len(merged_df))

# %%
merged_df.columns

# %%
# drop it to a json
merged_df.to_json('data/merged_data.json', orient='records', lines=True)

# %%
# try opening it
with open('data/merged_data.json', 'r') as f:
    data = f.read()

df = pd.read_json(data, orient='records', lines=True)
print(len(df))
df.head()


# %%
