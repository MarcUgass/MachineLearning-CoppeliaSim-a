#!/usr/bin/env python3
# -*- coding: utf-8 -*-

class Parametros:
    def __init__(self):
        self.iteraciones = 0
        self.cerca = 0
        self.media = 0
        self.lejos = 0
        self.min_puntos = 0
        self.max_puntos = 0
        self.umbral = 0
        
    def get_valores(self):
        return self.iteraciones,self.cerca,self.media,self.lejos,self.min_puntos,self.max_puntos,self.umbral
    
    def set_valores(self, it,ce,me,le,mi,ma,um):
        self.iteraciones = it
        self.cerca = ce
        self.media = me
        self.lejos = le
        self.min_puntos = mi
        self.max_puntos = ma
        self.umbral = um
    
instancia =Parametros() #instancia que usaremos