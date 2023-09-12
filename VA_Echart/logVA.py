import psychopy.visual
import psychopy.event
import math,random,os
import numpy as np
from psychopy import sound, gui, visual, core, data, event, logging, clock, colors, layout
import pyglet
font_file = '/Users/sc/Desktop/Psychopy/VA_Echart/OpticianSans/Optician-Sans.otf'
# Load the custom font
pyglet.font.add_file(font_file)

#Store info about the experiment session
_thisDir = os.path.dirname(os.path.abspath(__file__))
os.chdir(_thisDir)
expName = 'VA'  # from the Builder filename that created this script
expInfo = {'participant': '', 'session': '001'}
dlg = gui.DlgFromDict(dictionary=expInfo, sortKeys=False, title=expName)
if dlg.OK == False:
    core.quit()  # user pressed cancel
expInfo['date'] = data.getDateStr()  # add a simple timestamp
expInfo['expName'] = expName
# Data file name stem = absolute path + name; later add .psyexp, .csv, .log, etc
filename = _thisDir + os.sep + u'data/%s_%s_%s' % (expInfo['participant'], expName, expInfo['date'])
# An ExperimentHandler isn't essential but helps with data saving
thisExp = data.ExperimentHandler(name=expName, version='',
    extraInfo=expInfo, runtimeInfo=None,
    originPath='/Users/sc/Desktop/Psychopy',
    savePickle=True, saveWideText=True,
    dataFileName=filename)

# Setup the Window
win = visual.Window(
    size=[1470, 956], fullscr=True, screen=0,
    winType='pyglet', allowGUI=False, allowStencil=False,
    monitor='testMonitor', color=[1.0000, 1.0000, 1.0000], colorSpace='rgb',
    blendMode='avg', useFBO=True,
    units='height')

viewing_distance_cm = 300
arcminutes = 5
radians = arcminutes * (math.pi / 180 / 60)
tan_5_arcminutes = math.tan(radians)
# tan_5_arcminutes=0.00145444206890373
response_keys = ['left', 'down', 'right', 'up']  # Response keys for 4AFC
# key_sound = sound.Sound('B', secs=0.02, stereo=True, hamming=True)

trial_clock = core.Clock()
# Instructions
instructions_text = visual.TextStim(win, text='Press any key to start the test.',
                             pos=(0, 0), height=0.1, ori=0,
                             color='black', colorSpace='rgb', opacity=None,
                             languageStyle='LTR', depth=-1.0)
instructions_text.draw()
win.flip()
psychopy.event.waitKeys()

# set up handler to look after randomisation of trials etc
conditions = data.importConditions('/Users/sc/Desktop/Psychopy/VA_Echart/QUEST.xlsx')
trials = data.MultiStairHandler(stairType='QUEST', name='trials',
                                nTrials=30.0, conditions=conditions,
                                method='random',
                                originPath=-1)
nTrials=30

# trials = data.QuestPlusHandler(nTrials=30, intensityVals=[0.1,1,2], thresholdVals=[0.5,1], slopeVals=0.1, lowerAsymptoteVals=0.25, lapseRateVals=0.01, responseVals=('Yes', 'No'), prior=None, startIntensity=None, psychometricFunc='weibull', stimScale='linear', stimSelectionMethod='minEntropy', stimSelectionOptions=None)
thisExp.addLoop(trials)  # add the loop to the experiment
# initialise values for first condition
condition = trials.currentStaircase.condition
TrialCount = 0
level = trials._nextIntensity  # initialise some vals
# Loop through the trials
for thisTrial in trials:
    continueRoutine = True

    # current_intensity, condition = thisTrial  # Get the current intensity level
    log_VA, condition = thisTrial  # Get the current intensity level
    print('log_VA',log_VA)
    dir = np.random.choice([0, 90, 180, 270])
    tumbling_e_height = tan_5_arcminutes * viewing_distance_cm / (10 ** (-log_VA))
    tumbling_e = visual.TextStim(win=win,
                                 text='E',
                                 font='Optician Sans',
                                 pos=(0, 0), height=tumbling_e_height, ori=dir,
                                 color='black', colorSpace='rgb', opacity=None,
                                 languageStyle='LTR', depth=-1.0)
    tumbling_e.setOri(dir)
    tumbling_e.setHeight(tumbling_e_height)
    # tumbling_e.setPos((0, 0))
    tumbling_e.draw()
    win.flip()
    core.wait(0.2)
    TrialCount += 1
    #only got to next trial when key is pressed
    response = psychopy.event.waitKeys(keyList=response_keys, timeStamped=trial_clock)

    if response:
        response_key, response_time = response[0]
        # key_sound.play()
    else:
        response_key, response_time = None, float('nan')  # No response
    if event.getKeys(keyList=["escape"]):
        core.quit()

    correctness_dict = {'left': 180, 'down': 90, 'right': 0, 'up': 270}
    correct = 1 if response_key is not None and correctness_dict.get(response_key) == dir else 0
    # Store the results
    trials.addResponse(correct)
    trials.addOtherData('response_time', response_time)
    trials.addOtherData('dir', dir)
    trials.addOtherData('response_key', response_key)
    trials.addOtherData('TrialCount', TrialCount)
    trials.addOtherData('log_VA', log_VA)

    if TrialCount == nTrials:
        break
    #quit if 'escape' is pressed
    if response_keys == 'escape':
        core.quit()
# Save the results
excel_filename = 'data/%s.xlsx' % expInfo['participant']
trials.saveAsExcel(fileName=excel_filename)
# Close the window
win.close()