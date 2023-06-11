import pandas as pd
import numpy as np
import pickle

print('Loading dataset...')
input_path = '202112userlogs.csv'
# input_path = 'eseikatsu-sample.csv' # head 1000 rows of original dataset.
userlogdf = pd.read_csv(input_path)
time = pd.to_datetime(userlogdf['time'])
userlogdf['time'] = time

print('Start unification...')
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
print('Allocating user ID and command ID...')
command_id = []
user_id = []
for row in userlogdf.itertuples():
    command_key = (row.command_type, row.command_name)
    command_id.append(command_id_map[command_key])
    user_key = (row.customer_key, row.user, row.pc_name, row.pc_user)
    user_id.append(user_id_map[user_key])

# allocate session id
print('Allocating session ID...')
preprocess_df = pd.DataFrame(np.array([user_id, command_id]).T, columns=['user_id', 'command_id'])
preprocess_df['timestamp'] = userlogdf.time.map(lambda x: x.strftime('%Y-%m-%dT%H:%M:%S')) # type: str
preprocess_df['time'] = userlogdf.time # type: pd.dataframe
preprocess_df.sort_values('user_id', inplace=True)
session_id = [1]
cur_session_id = 1
pre_row = preprocess_df.iloc[0]
PIVOT_SECOND = 15 * 60
for row in preprocess_df[1:].itertuples():
    if (row.time - pre_row.time).total_seconds() > PIVOT_SECOND or row.user_id != pre_row.user_id:
        cur_session_id += 1
    session_id.append(cur_session_id)
    pre_row = row

preprocess_df.insert(0, 'session_id', session_id)
preprocess_df.drop(columns='time', inplace=True)

output_path = './out-data/eseikatsu.csv'
print('Saving data...')
pickle.dump(user_id_map, open('./out-data/user_id_map.pkl', 'wb'))
pickle.dump(command_id_map, open('./out-data/command_id_map.pkl', 'wb'))
preprocess_df.to_csv(output_path, index=False)
print('Done.')