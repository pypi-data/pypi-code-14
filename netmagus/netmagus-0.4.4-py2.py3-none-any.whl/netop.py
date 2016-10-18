# coding=utf-8
"""
NetMagus Python Library
Copyright (C) 2016 Intelligent Visbility, Inc. - Richard Collins <richardc@intelligentvisibility.com>

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Lesser General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Lesser General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""
from __future__ import absolute_import, division, print_function, unicode_literals

import copy
import json


#  Sample NetOp:
#  {
#     'id':        0, 'name': 'Ask Question 2', 'commandPath': PYTHON_BIN + ' ' + '/'.join([BASEDIR, 'new_leaf_1.py']),
#     'jsonPath':  '/'.join([TMPDIR, 'New_Leaf_Pair2.json']), 'description': 'Step 2 of 2', 'form': form,
#     # 'extraInfo': extraInfo
# }

class NetOpStep(object):
    def __init__(self, name='', commandPath='', description='', form=None, extraInfo=None, currentStep=1,
                 dataValid=True, buttonName='', saveRecord=True, dynamic=False, autoProceed=False,
                 disableBackButton=False, finalStep=False):
        """
        A NetMagus recipe typically behaves as a "wizard" style user interaction.  Each "step" or "screen" in in the
        wizard is created using a JSON representation of the screen atributes and controls.  This class allows a user
        to wrap numerous netmagus.form controls and control the user interaction, shell command exeuctions, and more.

        A JSON serialized repr of this object will control the individual screens and interactions of the NetMagus
        HTML UI.

        :param name: The name field is displayed at the top of the NetMagus UI screen as a typical HTML header
        :param commandPath: this is the full path of the shell command to be executed when a user presses NEXT or SUBMIT
        :param description: This may be text or html and will be rendered appropriately in the UI.  It is displayed
        below the name field.
        :param form: a list containing one or more netmagus.form objects to be drawn below the description in the UI
        :param extraInfo: optional dictionary to be rendered as additional JSON data to be used by UI to display
        extra HTML messages to the user.  It may also be used to pass data to UI to be received in future commandPath
        executuions.
        :param currentStep: integer representing the # of this operation in the overall wizard (i.e. 1 for first
        screen, 2 for 2nd, etc.)
        :param dataValid: boolean to indicate if the data received from NetMagus from the user's input was valid or not
        :param buttonName: string to control the name of the button displayed to users when using RPC based messages
        :param saveRecord: boolean to indicate if this screen/step should be saved in the UI history
        :param dynamic: boolean to specify if this screen contains controls with dynamic data that must be refreshed
        when a user presses the BACK button.  If True, commandPath is executed again when a user revisits the screen
        :param autoProceed: boolean to indicate if the UI should autoproceed from its current screen to this new one
        sent to the UI.  if False, user must manually press the PROCEED button to advance to the next screen/step
        :param finalStep: boolean to indicate when a screen is the last/final screen in an operation.  This is used
        by NetMagus UI to understand when a task is finished and that it no longer needs to have its execution
        tracked by the execution engine
        """
        self.id = 0
        self.name = name
        self.description = description
        self.currentStep = currentStep
        self.commandPath = commandPath
        self.form = form or []
        self.extraInfo = extraInfo or {}
        self.dataValid = dataValid
        self.buttonName = buttonName
        self.saveRecord = saveRecord
        self.dynamic = dynamic
        self.autoProceed = autoProceed
        self.disableBackButton = disableBackButton
        self.finalStep = finalStep

    def __repr__(self):
        return json.dumps(self, sort_keys=True, default=lambda o: o.__dict__)

    @property
    def as_dict(self):
        return_dictionary = copy.copy(self.__dict__)
        return_dictionary['form'] = [component.as_dict for component in self.form]
        return return_dictionary
