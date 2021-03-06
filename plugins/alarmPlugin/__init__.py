#!/usr/bin/python
# -*- coding: utf-8 -*-

import re

from fractions import Fraction

from plugin import *

from siriObjects.baseObjects import AceObject, ClientBoundCommand
from siriObjects.uiObjects import AddViews, AssistantUtteranceView
from siriObjects.systemObjects import DomainObject
from siriObjects.alarmObjects import *

class alarmPlugin(Plugin):

    localizations = {
        'Alarm': {
            "settingAlarm": {
                "en-US": u"Setting the Alarm\u2026","fr-FR": u"Ajouter alarme\u2026"
            }, "alarmWasSet": {
                "en-US": "Your alarm is set for {0}:{1} {2}.","fr-FR": "Votre alarme est configuré pour {0}:{1} {2}."
            }, "alarmSetWithLabel": {
                "en-US": "Your alarm {0} {1} is set for {2}:{3} {4}.","fr-FR": "Votre alarme {0} {1} est configuré pour {2}:{3} {4}."
            }
        }
    }

    res = {
        'setAlarm': {
            'en-US': '.*set.* alarm for.* (0?[1-9]|1[012])([0-5]\d)?\s?([APap][mM])\s?(\bnommé|appele|titre\b)?\s?(([a-z0-9]{1,7}\s)?([a-z0-9]{1,7})\s?([a-z0-9]{1,7}))?',
            'fr-FR': '(Alarme)|(Ajouter .*alarme)|(Reveil)|(Ajouter.* reveil)'
        }
    }

    @register("en-US", res['setAlarm']['en-US'])
    @register("fr-FR", "(Alarme)|(Ajouter .*alarme)|(Reveil)|(Ajouter.* réveil)")
    def setAlarm(self, speech, language):
        if language == "fr-FR":
            Heure_alarm = self.ask("A quel heure ?")
            if Heure_alarm.count('heures') > 0:
                Heure_alarm = Heure_alarm.replace('heure','')
            alarmString = Heure_alarm.split(' ')
            alarmHour = int(alarmString[0])
            alarm24Hour = alarmHour
            alarmMinutes = int(alarmString[1])
            alarmAMPM = ""              
            alarmLabelExists = None
            alarmLabel = None

            alarmString = re.match(alarmPlugin.res['setAlarm'][language], speech, re.IGNORECASE)
        if language == "en-US":
            alarmString = re.match(alarmPlugin.res['setAlarm'][language], speech, re.IGNORECASE)
            
            alarmHour = int(alarmString.group(1))
            alarm24Hour = alarmHour
            alarmMinutes = alarmString.group(2)
            alarmAMPM = alarmString.group(3)
            alarmLabelExists = alarmString.group(4)
        
            #check if we are naming the alarm
            if alarmLabelExists == None:
                alarmLabel = None
            else:
                alarmLabel = alarmString.group(5)
            
            #the siri alarm object requires 24 hour clock
            if (alarmAMPM == "pm" and alarmHour != 12):
                alarm24Hour += 12

            if alarmMinutes == None:
                alarmMinutes = "00"
            else:
                alarmMinutes = int(alarmMinutes.strip())

        view = AddViews(self.refId, dialogPhase="Reflection")
        view.views = [
            AssistantUtteranceView(
                speakableText=alarmPlugin.localizations['Alarm']['settingAlarm'][language],
                dialogIdentifier="Alarm#settingAlarm")]
        self.sendRequestWithoutAnswer(view)

        #create the alarm
        print alarm24Hour
        alarm = AlarmObject(alarmLabel, int(alarmMinutes), alarm24Hour, None, 1)
        response = self.getResponseForRequest(AlarmCreate(self.refId, alarm))
        
        print(alarmPlugin.localizations['Alarm']['alarmWasSet'][language].format(alarmHour, alarmMinutes, alarmAMPM))
        view = AddViews(self.refId, dialogPhase="Completion")
        
        if alarmLabel == None:
            view1 = AssistantUtteranceView(speakableText=alarmPlugin.localizations['Alarm']['alarmWasSet'][language].format(alarmHour, alarmMinutes, alarmAMPM), dialogIdentifier="Alarm#alarmWasSet")
        else:
            view1 = AssistantUtteranceView(speakableText=alarmPlugin.localizations['Alarm']['alarmSetWithLabel'][language].format(alarmLabelExists, alarmLabel, alarmHour, alarmMinutes, alarmAMPM), dialogIdentifier="Alarm#alarmSetWithLabel")
        
        view2 = AlarmSnippet(alarms=[alarm])
        view.views = [view1, view2]
        self.sendRequestWithoutAnswer(view)
        self.complete_request()
