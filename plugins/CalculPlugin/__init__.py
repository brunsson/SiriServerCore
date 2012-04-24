#!/usr/bin/python
# -*- coding: utf-8 -*-


from plugin import *

class Calcul_Siri(Plugin):
    def Calcul_Addition(self,Premier_Nbr,Deuxieme_Nbr):
        result_cacl = int(Premier_Nbr) + int(Deuxieme_Nbr)
        return result_cacl

    def Calcul_Soustraction(self,Premier_Nbr,Deuxieme_Nbr):
        result_cacl = int(Premier_Nbr) - int(Deuxieme_Nbr)
        return result_cacl

    def Calcul_Multiplication(self,Premier_Nbr,Deuxieme_Nbr):
        result_cacl = int(Premier_Nbr) * int(Deuxieme_Nbr)
        return result_cacl

    def Calcul_Division(self,Premier_Nbr,Deuxieme_Nbr):
        result_cacl = int(Premier_Nbr) / int(Deuxieme_Nbr)
        return result_cacl

    @register("fr-FR", u"((Calcul)|(Calculer))? (?P<Premier>[0-9]+) (?P<Signe>(\+|\-|multiplié par|fois|divisé par)) (?P<Deuxieme>([0-9]+))$")
    def Calcul_brunsson(self, speech, language, regex):
        Premier_Nombre = regex.group('Premier')
        Deuxieme_Nombre = regex.group('Deuxieme')
        Signe = regex.group('Signe')
        Calcul_Swicth = {
            '+': self.Calcul_Addition(Premier_Nombre,Deuxieme_Nombre),
            '-': self.Calcul_Soustraction(Premier_Nombre,Deuxieme_Nombre),
            u'multiplié par': self.Calcul_Multiplication(Premier_Nombre,Deuxieme_Nombre),
            'fois': self.Calcul_Multiplication(Premier_Nombre,Deuxieme_Nombre),
            u'divisé par': self.Calcul_Division(Premier_Nombre,Deuxieme_Nombre),
        }
        Result_calcul = Calcul_Swicth[Signe]
        self.say("Le resultat de votre calcul est " + str(Result_calcul))
        Reponse_Supplementaire = "Debut"
        self.complete_request()
