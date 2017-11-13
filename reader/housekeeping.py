import lxml.html,json
from pprint import pprint

def clean(data):
	#employing the lxml parser to clean the content of mail
	#every other thing is pretty self explanatory
	newdata = data
	htmldata = []
	replaced = []
	for i in data["value"]: 
		htmldata.append(i['body']['content'])
	for x in htmldata:
		doc  = lxml.html.document_fromstring(x)
		replaced.append(doc.text_content().strip())
	for i,obj in enumerate(newdata['value']):
		obj['body']['content'] = replaced[i]
	writer(newdata,data)
	return newdata
	
def writer(nwjson,oljson):
	#function to write both old json and new json prettily
	with open('oldata.json','w') as olwriter:
		json.dump(oljson,olwriter,sort_keys=True,indent=4, separators=(',', ': '))
	with open('nwdata.json','w') as nwwriter:
		json.dump(nwjson,nwwriter,sort_keys=True,indent=4, separators=(',', ': '))
	return	  	 
