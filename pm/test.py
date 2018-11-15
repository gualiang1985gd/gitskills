from werkzeug.security import generate_password_hash,check_password_hash
from readJson import read_db_json_indices

db_info = read_db_json_indices()
db_data = db_info
i = 0
for i in range(len(db_info)):
    if db_info[i]["number"] == '2':
        db_data[i]["username"] = 'hjl'
        print db_data





