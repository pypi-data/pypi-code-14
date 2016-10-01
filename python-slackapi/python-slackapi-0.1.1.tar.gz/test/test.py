from slackapi import SlackApi



##################################
# SlackApi Wrapper TEST CODE     #
##################################
"""
Usage

slackApi = SlackApi('API-KEY')

# call without wrapper
slackApi.api_call('chat.postMessage', args)

# call with wrapper 
slackApi.chat.postMessage(args)


"""

def testSendMessageUsingWrapper():
    result = slackApi.chat.postMessage(
        {
            'channel'   : 'CHANNEL-ID',
            'text'      : 'api test from python wrapper',
            'as_user'   : 'false'
        }
    )

    print(result)

def testSendMessageUsingApiCall():
    result = slackApi.api_call(
        "chat.postMessage",
        {
            "channel":"CHANNEL-ID","text":"api call test from PYTHON", 
            "as_user":"false"
        }
    ) 
    print(result)

def testApiTestUsingWrapper():
    result = slackApi.api.test()
    print(result)

def test():

    testApiTestUsingWrapper()
    testSendMessageUsingApiCall()
    testSendMessageUsingWrapper()

slackApi = SlackApi('xoxp-71556812259-71605382544-86284462273-507fab82dfa7e533ccd0f393f5e52be1')
print(slackApi.channels.list() )