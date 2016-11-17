# coding:utf-8
from expy import *

# initiate the environment
start(port=0xC100, sample_rate=16000)

def trial(data):
    # calculate the trigger number
    if data.type=='SVO':
        mark = 1
    elif data.type=='SV':
        mark = 2
    elif 'RND' in data.type:
        mark = 3
    if data.pure == True:
        mark += 3

    sendTrigger(0,mode='P')  # clear port
    sound = loadManySound('stimuli/',data.content.split(' '))  # load 10 sentences' wav

    # display the fixation in 800-1400ms (set in "setting.txt")
    drawText('+')
    show(timing('fix'),cleanScreen=False)

    # send trigger
    sendTrigger(mark,mode='P')  

    # play the loaded sound, then clear the screen 
    playSound(sound)
    clear()

    # wait for a response
    drawText('J：没有 -- K：有')
    key,rt = waitForResponse({K_j:'T',K_k:'F'})
    clear()

    return key,rt

def block(blockID,block_data): 
    # tip
    alertAndGo('实验会在3秒内开始，请注意看屏幕。',3000)
    # execute trial function repeatly and get the response data
    result = [trial(data) for data in block_data]
    # save data
    saveResult(blockID, result, stim=block_data)
    # tip of rest
    restTime()


'''session'''
shared.subj = getInput('请输入被试编号：')
blockCount = 6
firstBlock = 1
if firstBlock ==1:
    resp = instruction(shared.setting['instruction'])

# run on blocks between firstBlock and blockCount
for blockID in range(firstBlock, blockCount+1):
    # load the stimuli in this block
    block_data = readStimuli('trial_list.csv', query='block==%d' %blockID)
    # execute block function
    block(blockID,block_data)

alertAndQuit('实验结束, 谢谢参与我们的实验!')