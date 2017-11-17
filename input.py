import json

data = json.load(open('nwdata.json'))

def givemap():
	mymap = {}
	for i in data['value']:
		mymap[i['id']] = {i['body']['content'],i['receivedDateTime'],i['subject'],i['from']['emailAddress']['address']}
	'''
	for i,val in mymap.items():
		print(i,val)
	'''
	return mymap
	
givemap()
