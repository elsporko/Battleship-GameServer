import json
import sys
from Battleship_AWS.AWS.aws import AWS

class Game(object):
    def __init__(self):
        self.order = 0
        self.playerRoster = {} # Placeholder for all players in the game self.playerOrder = [0 for x in range(100)] # Order of player turn
        self.playerOrder = [None for x in range(100)]


def process_message(message):
    payload = json.loads(message)

    actions = {
        'register': register(payload),
    }

def register(payload):
    receipthandle=payload['ReceiptHandle']
    msg=json.loads(payload['Body'])
    payload=json.loads(msg['Message']) 
    message = {"registration": "FAIL", 'arn': payload['arn']}
    if 'handle' in payload and payload['handle'] not in game.playerRoster:
        game.playerRoster[payload['handle']]={'handle': payload['handle'], 'arn': payload['arn'], 'order': game.order}

    # message returned to caller
    message = {"registration": "SUCCESS",
           "arn": payload["arn"],
           "order" : game.order,
           "handle" : payload['handle'],
           "registered_players" : game.playerRoster
          }
    game.order += 1

    try:
        resp = sns_client.publish(TopicArn=payload['arn'], Message=json.dumps(message))
        print ("Roster: {}\n\n".format(game.playerRoster))
    except KeyError:
        print("payload: ", payload)
        print("register KeyError")
        return
    except TypeError:
        print("register TypeError")
        return
    except NotFound:
        print("register NotFound - Need to do something more than print")
        return

    # next, we delete the message from the queue so no one else will process it again
    ret = sqs_client.delete_message(QueueUrl=queue.url, ReceiptHandle=receipthandle)

    return

count=1
game = Game()
aws = AWS()

# Set up the queue and topic for registration
aws.create_queue('Battleship')
aws.create_topic('Registration')
aws.add_policy()
aws.subscribe_to_topic()

while True:
    messages = aws.receive_message()
    print ("received message({}): {}".format(count, messages))
    count = count + 1
    if 'Messages' in messages: # when the queue is exhausted, the response dict contains no 'Messages' key
        for message in messages['Messages']: # 'Messages' is a list
            # process the messages
            process_message(json.dumps(message))

