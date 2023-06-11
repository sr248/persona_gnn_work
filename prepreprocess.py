import pandas as pd
import numpy as np

path = 'downloads/202112userlogs.csv'
userlogdf = pd.read_csv(path)
time = pd.to_datetime(userlogdf['time'])
userlogdf['time'] = time

# create map for unique user id
user_df = userlogdf[['customer_key', 'user', 'pc_name', 'pc_user']]
user_df = user_df[~user_df.duplicated()]
user_id_map = dict()
for i, v in enumerate(user_df[['customer_key', 'user', 'pc_name', 'pc_user']].values):
    user_id_map[tuple(v)] = i + 1

# create map for unique command id
command_df = userlogdf[['command_type', 'command_name']]
command_df = command_df[~command_df.duplicated()]
command_id_map = dict()
for i, v in enumerate(command_df[['command_type', 'command_name']].values):
    command_id_map[tuple(v)] = i + 1

# allocate user id and command id
command_id = []
user_id = []
# TODO: Merge following 2 for statements into 1
for row in userlogdf[['command_type', 'command_name']].itertuples():
    map_key = tuple(row)[1:] # remove [0]index
    command_id.append(command_id_map[map_key])
for row in userlogdf[['customer_key', 'user', 'pc_name', 'pc_user']].itertuples():
    map_key = tuple(row)[1:] # remove [0]index
    user_id.append(user_id_map[map_key])

# allocate session id
prepreprocess_df = pd.DataFrame(np.array([user_id, command_id]).T, columns=['user_id', 'command_id'])
prepreprocess_df['timestamp'] = userlogdf.time
prepreprocess_df.sort_values('user_id', inplace=True)
session_id = [1]
cur_session_id = 1
pre_row = prepreprocess_df.iloc[0]
PIVOT_SECOND = 15 * 60
for row in prepreprocess_df[1:].itertuples():
    if (row.timestamp - pre_row.timestamp).total_seconds() > PIVOT_SECOND or row.user_id != pre_row.user_id:
        cur_session_id += 1
    session_id.append(cur_session_id)
    pre_row = row

prepreprocess_df.insert(0, 'session_id', session_id)

# TODO: save user_id_map; command_id_map; prepreprocess_df of eseikatsu for preprocessing
