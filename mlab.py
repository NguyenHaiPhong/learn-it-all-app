import mongoengine

# mongodb://<dbuser>:<dbpassword>@ds227322.mlab.com:27322/learn-it-all-final-project-c4e19
host = "ds227322.mlab.com"
port = 27322
    
db_name = "learn-it-all-final-project-c4e19"
user_name = "admin"
password = "admin1"

def connect():
    mongoengine.connect(db_name, host=host, port=port, username=user_name, password=password)

def list2json(l):
    import json
    return [json.loads(item.to_json()) for item in l]


def item2json(item):
    import json
    return json.loads(item.to_json())