import requests
import psycopg2, psycopg2.extras
import json
'''
To do
1. Create a function to check to parent emailid and only collect the emails from that id only
2. insert if not exists
3. More try and catch 
'''
def entery(messages):
    message = json.loads(json.dumps(messages))
    #message =json.loads(messages)
    #if(check(message['@odata.context'])):
    #    return
    #else:
    con = None
    try:
        con = psycopg2.connect(dbase='d8625tt3dr4d5r', user='xpvirwrpybbjph', password='5b52a9a74f873d954a0084eb33896ad7700168705aee2f36eb1730741eac004a', host='ec2-54-243-43-72.compute-1.amazonaws.com', port="5432")
        #con = psycopg2.connect(dbname = 'testdb', user = 'aki', password = 'abcd@123')
        cur = con.cursor(cursor_factory=psycopg2.extras.DictCursor)
        data = ()
        query = "INSERT INTO reader_emaildata (eid, emailid, rdatetime, subject, content) VALUES (%s,%s,%s,%s,%s) ON CONFLICT (eid) DO NOTHING"
        cnt = 0     #to count no of records
        for i in message['value']:
            cnt = cnt+1
            #if(cnt>1): break
            content = i['body']['content']
            rdatetime = i['receivedDateTime']
            subject = i['subject']
            emailid = i['from']['emailAddress']['address']
            eid = i['id']
            data = data+((eid,emailid,rdatetime,subject,content),)
        try:
            cur.executemany(query,data)
            con.commit()
        except psycopg2.Error as e:
            print('Error %s' % e)
            print('for record',data[:4])
    except psycopg2.Error as e:
        if con:
            con.rollback()
        print('Error %s' % e)
    finally:
        if con:
            con.close()
    return

def check(string):
    if(string.find('trial_wali_id%40outlook.com'))==-1:
        return True
    else:
        return False
