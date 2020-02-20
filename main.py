import os
import json
import sqlite3
import slack

@slack.RTMClient.run_on(event='message')
def store(**payload):
    data = payload['data']

    # this pretty prints the output
    # j = json.dumps(data, sort_keys=True, indent=4, separators=(',', ':'))

    # assigns values to keys
    dict = {
        'user': data['user'],
        'channel': data['channel'],
        'timestamp': data['ts'],
        'text': data['text']
        }

    insert_data(dict)

def slacktoken():
    return os.environ['SLACKTOKEN']

# creates table it it's not already created
def create_db():
    conn = sqlite3.connect('src/slack')
    c = conn.cursor()

    c.execute('''CREATE TABLE IF NOT EXISTS slack
                            (user text,
                             channel text,
                             timestamp text,
                             msg text)''')

    conn.commit()
    conn.close()

# takes dict and makes insert statement
def insert_data(msg):
    conn = sqlite3.connect('src/slack')
    c = conn.cursor()

    # users sqlite3 concatination insated of python
    c.execute('INSERT INTO slack VALUES (?, ?, ?, ?)', (msg['user'], msg['channel'], msg['timestamp'], msg['text']))
    conn.commit()
    conn.close()


def main():
    # gets slack token
    slack_token = slacktoken()

    # creates tables if they don't EXIST
    create_db()
    print('db_created')

    # initiates rtm loop
    rtm_client = slack.RTMClient(token=slack_token)
    rtm_client.start()

main()
