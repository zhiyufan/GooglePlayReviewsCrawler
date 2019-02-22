import json

app_ip = ['com.owncloud.android']
app_num = 0

fp = open(app_ip[app_num]+".json", "r")
content = json.loads(fp.read())

print(content[0])