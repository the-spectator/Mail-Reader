import requests
import uuid
import json
from reader.housekeeping import clean
graph_endpoint = 'https://graph.microsoft.com/v1.0{0}'

# Generic API Sending
def make_api_call(method, url, token, user_email, payload = None, parameters = None):
  # Send these headers with all API calls
  headers = { 'User-Agent' : 'mailreader/1.0',
              'Authorization' : 'Bearer {0}'.format(token),
              'Accept' : 'application/json',
              'X-AnchorMailbox' : user_email }

  # Use these headers to instrument calls. Makes it easier
  # to correlate requests and responses in case of problems
  # and is a recommended best practice.
  request_id = str(uuid.uuid4())
  instrumentation = { 'client-request-id' : request_id,
                      'return-client-request-id' : 'true' }

  headers.update(instrumentation)

  response = None

  if (method.upper() == 'GET'):
      response = requests.get(url, headers = headers, params = parameters)
  elif (method.upper() == 'DELETE'):
      response = requests.delete(url, headers = headers, params = parameters)
  elif (method.upper() == 'PATCH'):
      headers.update({ 'Content-Type' : 'application/json' })
      response = requests.patch(url, headers = headers, data = json.dumps(payload), params = parameters)
  elif (method.upper() == 'POST'):
      headers.update({ 'Content-Type' : 'application/json' })
      response = requests.post(url, headers = headers, data = json.dumps(payload), params = parameters)

  return response
  
def get_me(access_token):
  get_me_url = graph_endpoint.format('/me')

  # Use OData query parameters to control the results
  #  - Only return the displayName and mail fields
  query_parameters = {'$select': 'displayName,mail'}

  r = make_api_call('GET', get_me_url, access_token, "", parameters = query_parameters)

  if (r.status_code == requests.codes.ok):
    return r.json()
  else:
    return "{0}: {1}".format(r.status_code, r.text)

def get_my_messages(access_token, user_email):
  get_messages_url = graph_endpoint.format('/me/mailfolders/sentitems/messages')

  # Use OData query parameters to control the results
  #  - Only first 10 results returned
  #  - Only return the ReceivedDateTime, Subject, and From fields
  #  - Sort the results by the ReceivedDateTime field in descending order
  query_parameters = {'$top':'1000000000',
  					  '$select': 'receivedDateTime,subject,from,body',
                      '$orderby': 'receivedDateTime DESC'}

  r = make_api_call('GET', get_messages_url, access_token, user_email, parameters = query_parameters)

  if (r.status_code == requests.codes.ok):
  	nwjson = clean(r.json()) #cleaned json: content
  	return nwjson
  	#return r.json()
  	
  else:
    return "{0}: {1}".format(r.status_code, r.text)

def send_my_messages(access_token, user_email,message):
  get_messages_url = graph_endpoint.format('/me/microsoft.graph.sendMail')
  r = make_api_call('POST', 'https://graph.microsoft.com/v1.0/me/microsoft.graph.sendMail', access_token, user_email,payload = message,parameters = None)

  if (r.status_code == requests.codes.ok):
  	nwjson = clean(r.json()) #cleaned json: content
  	return nwjson
  	
  else:
    return "{0}: {1}".format(r.status_code, r.text)
    
    
    
    
