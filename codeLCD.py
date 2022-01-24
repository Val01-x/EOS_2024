# coding:utf-8
# Utilisation d'un afficheur LCD 1602 sur Raspberry 3 B+


from RPLCD.gpio import CharLCD
import time
import unittest
from lcd import LcdApi


class LcdSim(LcdApi):
    def __init__(self, num_lines=2, num_columns=16):
        LcdApi.__init__(self, num_lines, num_columns)
        self.reset()
        self.num_lines = num_lines
        self.num_columns = num_columns
        # chargement des données
        with open('data.json') as json_data:
            self.data_options = json.load(json_data)

    def start(self):    
        # affichage de bienvenue
        lcd.cursor_pos = (0, 3)  # 0 = 1ère ligne / 3 = 4ème colonne
        lcd.write_string(u'Bienvenue')
        lcd.cursor_pos = (1, 7)  # 1 = 2ème ligne / 7 = 8ème colonne
        lcd.write_string(u'EOS')
        time.sleep(3)
        self.menu()

    def menu(self):    
        # affichage du menu
        lcd.clear()
        lcd.cursor_pos = (0, 1)  # 0 = 1ère ligne / 1 = 2ème colonne
        lcd.write_string(u'Mise en sachet')
        lcd.cursor_pos = (1, 1)  # 1 = 2ème ligne / 1 = 2ème colonne
        lcd.write_string(u'Options')
        if lcd.buttonPressed(lcd.bouton1):
            self.mise_en_sachet_en_attente()
        if lcd.buttonPressed(lcd.bouton2):
            self.options()

    def mise_en_sachet_en_attente(self):    
        # affichage de la mise en sachet en attente
        lcd.clear()
        lcd.cursor_pos = (0, 1)  # 0 = 1ère ligne / 1 = 2ème colonne
        lcd.write_string(u'Poids : ')
        lcd.cursor_pos = (0, 9)  # 1 = 2ème ligne / 9 = 10ème colonne
        lcd.write_string(self.data_options['data']['poids'])
        lcd.cursor_pos = (0, 13)  # 1 = 2ème ligne / 13 = 14ème colonne
        lcd.write_string(self.data_options['data']['ordre'])
        if lcd.buttonPressed(lcd.valider):
            self.mise_en_sachet_en_cours()
        if lcd.buttonPressed(lcd.retour):
            self.menu()

    def mise_en_sachet_en_cours(self):    
        # affichage de la mise en sachet en cours
        lcd.clear()
        while true:
            lcd.cursor_pos = (0, 1)  # 0 = 1ère ligne / 1 = 2ème colonne
            lcd.write_string(u'Poids : ')
            lcd.cursor_pos = (0, 9)  # 0 = 1ème ligne / 9 = 10ème colonne
            lcd.write_string(self.data_options['data']['poids'])
            lcd.cursor_pos = (0, 13)  # 0 = 1ème ligne / 13 = 14ème colonne
            lcd.write_string(self.data_options['data']['ordre'])
            lcd.cursor_pos = (1, 5)  # 1 = 2ème ligne / 5 = 6ème colonne
            lcd.write_string(u'En cours')
            time.sleep(2)
            lcd.clear()
            time.sleep(1)
            # tester la fin de la mise sachet
            # si fini self.mise_en_sachet_en_attente()

    def options(self):    
        # affichage des options
        lcd.clear()
        lcd.cursor_pos = (0, 1)  # 0 = 1ère ligne / 1 = 2ème colonne
        lcd.write_string(u'Poids : ')
        lcd.cursor_pos = (0, 9)  # 0 = 1ère ligne / 9 = 10ème colonne
        lcd.write_string(self.data_options['data']['poids'])
        lcd.cursor_pos = (1, 1)  # 1 = 2ème ligne / 1 = 2ème colonne
        lcd.write_string(u'Ordre')
        lcd.cursor_pos = (1, 9)  # 1 = 2ème ligne / 9 = 10ème colonne
        lcd.write_string(self.data_options['data']['ordre'])
        if lcd.buttonPressed(lcd.bouton1):
            self.option_poids()
        if lcd.buttonPressed(lcd.bouton2):
            self.option_ordre()
        if lcd.buttonPressed(lcd.retour):
            self.menu()

    def option_poids(self):    
        # affichage option poids
        poids = self.data_options['data']['poids']
        lcd.clear()
        lcd.cursor_pos = (0, 1)  # 0 = 1ère ligne / 1 = 2ème colonne
        lcd.write_string(u'Nouveau poids')
        lcd.cursor_pos = (0, 15)  # 0 = 1ère ligne / 15 = 16ème colonne
        lcd.write_string(u'+')
        lcd.cursor_pos = (1, 6)  # 1 = 2ème ligne / 6 = 7ème colonne
        lcd.write_string(poids)
        lcd.cursor_pos = (1, 15)  # 1 = 2ème ligne / 15 = 16ème colonne
        lcd.write_string(u'-')
        if lcd.buttonPressed(lcd.bouton1):
            poids = poids + 1
        if lcd.buttonPressed(lcd.bouton2):
            poids = poids - 1
        if lcd.buttonPressed(lcd.retour):
            self.options()
        if lcd.buttonPressed(lcd.valider):
            self.data_options['data']['poids'] = poids
            self.enregistrer()
            self.options()

    def option_ordre(self):    
        # affichage option ordre
        lcd.clear()
        lcd.cursor_pos = (0, 1)  # 0 = 1ère ligne / 1 = 2ème colonne
        lcd.write_string(u'Nouvel ordre')
        lcd.cursor_pos = (0, 13)  # 0 = 1ère ligne / 13 = 14ème colonne
        lcd.write_string(u'KG')
        lcd.cursor_pos = (1, 14)  # 1 = 2ème ligne / 14 = 15ème colonne
        lcd.write_string(u'G')
        if lcd.buttonPressed(lcd.bouton1):
            self.data_options['data']['ordre'] = 'kg'
            self.enregistrer()
            self.options()
        if lcd.buttonPressed(lcd.bouton2):
            self.data_options['data']['ordre'] = 'g'
            self.enregistrer()
            self.options()

    def enregistrer(self):
        with open('data.json') as json:
                json.dump(data_options, json)


if __name__ == '__main__':
    lcd = CharLCD(cols=16, rows=2, pin_rs=37, pin_e=35, pins_data=[33, 31, 29, 23])
    unittest.main()