# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %% [markdown]
# Go find all the 'wide' rows and collapse into denser cells of 'values'.

# %%

import numpy as np
import pandas as pd
df = pd.read_csv('input/test-lime-data.csv')
df.index.name = 'id'

ndf = pd.DataFrame(columns=['from_org', 'to_org', 'rel_type', 'rel_freq'])
ndf

# %%
rel_type_column_names = ['agriculture', 'climate_change', 'community_development', 'conservation', 'economic_development', 'education', 'energy',
                         'food_security', 'gender', 'grant_making', 'health', 'human_rights', 'peace_building', 'policy_making_governance', 'water', 'wildlife_biodiversity']
freq_column_names = ['not_in_6_months', 'once_6_monthly',
                     'multiple_6_monthly', 'multiple_monthly', 'weekly', 'multiple_weekly']
# Column indices
max_partner_length = 1  # 10
name_start_idx = [43, 44, 45, 46, 47, 48, 49, 50, 51, 52]
name_len = 1
type_start_idx = [53, 75, 97, 119, 141, 163, 185, 207, 229, 251]
type_len = 16  # 22
freq_start_idx = [273, 279, 285, 291, 297, 303, 309, 315, 321, 327]
freq_len = 6


# %%
def flatten_type(row: pd.Series, start_col):
    types = row[start_col:start_col+type_len]
    types.index = rel_type_column_names
    types_keep = types[types == 'Yes']
    res = '|'.join(types_keep.index)
    return res

# %%


def flatten_freq(row, start_col):
    freqs = row[start_col:start_col+freq_len]
    freqs.index = freq_column_names
    freq = freqs[freqs == 'Yes']
    return freq.index[0]

# %%


# For every row...
for index, row in df.iterrows():
    # Go through every potential partner...
    for partner_index in range(0, max_partner_length):
        partner_number = partner_index + 1
        # print(f'Doing partner {partner_number}')
        from_org = row.iloc[0]

        to_org_idx = name_start_idx[partner_index]
        to_org = row.iloc[to_org_idx]

        if to_org == 'No' or pd.isnull(to_org):
            print(f'drop!: {to_org}')
            continue

        type_start = type_start_idx[partner_index]
        rel_type = flatten_type(row, type_start)

        freq_start = freq_start_idx[partner_index]
        rel_freq = flatten_freq(row, freq_start)

        row_data = {'from_org': from_org, 'to_org': to_org,
                    'rel_type': rel_type, 'rel_freq': rel_freq}
        ndf = ndf.append(row_data, ignore_index=True)
ndf

# %%
