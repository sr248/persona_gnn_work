### preprocess.py:

原本のデータセットを前処理し、user, commandのID付けとセッション番号の振り分けを行います。以下入出力ファイルの様子。

Input:
```
time,customer_key,branch,user,pc_name,pc_user,command_type,command_name
2021-12-01T00:00:05.774,2108386,branch1663,user19493,pcName26646,pcUser29,プロセス,login
2021-12-01T00:00:05.775,2108386,branch1663,user19493,pcName26646,pcUser29,プロセス,start
2021-12-01T00:00:09.653,2101030,branch2156,user21542,pcName21710,pcUser21544,帳票出力,物件チラシ_賃貸借
...
```

Output:
```
session_id,user_id,command_id,timestamp
1,1,1,2021-12-01T00:00:05
1,1,2,2021-12-01T00:00:05
1,1,6,2021-12-01T00:01:55
2,2,3,2021-12-01T00:18:38
...
```

ファイル内の`path = 'downloads/eseikatsu-sample.csv'`や以下の部分でのpathは適宜変更し、`python cprepreprocess.py`を実行してください。少し時間がかかります(3分ほど)。
```python
output_path = './out-data/eseikatsu.csv'
pickle.dump(user_id_map, open('./out-data/user_id_map.pkl', 'wb'))
pickle.dump(command_id_map, open('./out-data/command_id_map.pkl', 'wb'))
prepreprocess_df.to_csv(output_path, index=False)
```
また出力ファイルである`user_id_map.pkl`と`command_id_map.pkl`には`user_id`と`command_id`にそれぞれ対応する実際の内容 (ex. `customer_key`; `pc_name`; `command_name`など) が入っています。実際のコマンド内容を参照したいときは例えば以下を実行してファイルをロードしてください。
```python
with open('chome/user_id_map.pkl', 'rb') as f:
    user_id_map = pickle.load(f)
```
