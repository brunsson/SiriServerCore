#!/usr/bin/python
# -*- coding: utf-8 -*-


from plugin import *
import feedparser
import htmlentitydefs
import re
import random

from siriObjects.uiObjects import AddViews, AssistantUtteranceView, Button
from siriObjects import systemObjects
from siriObjects.websearchObjects import WebSearch

class jokes(Plugin):
    @register("fr-FR", "(Blague)|(Humour.*)")
    def joke_du_Matin(self, speech, language):
        if  language == 'fr-FR':
            rss = "http://blague.dumatin.fr/blagues.xml"
        IndiceBlague = random.randint(1,6)
        print IndiceBlague
        feeds = feedparser.parse(rss)
        NomBlague = feeds.entries[IndiceBlague]['title']
        Blague = feeds.entries[IndiceBlague].description        
        TxtBlagueSansCaractere = Blague.replace("<br />","")
        TxtBlague = TxtBlagueSansCaractere[0:TxtBlagueSansCaractere.index("<a href=")]
        LienSite = TxtBlagueSansCaractere[TxtBlagueSansCaractere.index("<a href=") + 16:TxtBlagueSansCaractere.index(">[ blague.dumatin.fr") - 2]
        LienSite = LienSite.replace("."," ")
        print LienSite
        if language == 'fr-FR':
            view = AddViews(self.refId, dialogPhase="Summary")
            
            viewBlague = AssistantUtteranceView(text=TxtBlague, speakableText="Voici une blague du matin", dialogIdentifier="Blague#created")
            button = Button(text=LienSite)
            cmd = systemObjects.SendCommands()
            cmd.commands = [systemObjects.StartRequest(utterance=u"^webSearchQuery^=^{0}^^webSearchConfirmation^=^Yes^".format(LienSite))]
            button.commands = [cmd]
            view.views = [viewBlague,button]
            self.send_object(view)
        self.complete_request()

    @register("de-DE", "(.*Hallo.*)|(.*Hi.*Siri.*)")
    @register("en-US", "(.*Hello.*)|(.*Hi.*Siri.*)")
    @register("fr-FR", "(Bonjour)|(Salut)")
    def rep_bonjour(self, speech, language):
        print language
        if language == 'de-DE':
            self.say("Hallo.")
        elif language == 'en-US':
            self.say("Hello")
        elif language == 'fr-FR':
            self.say("Bonjour, comment ca va aujourd'hui ?")
        self.complete_request()
