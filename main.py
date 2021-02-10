from tkinter import *
import pyautogui
import pyperclip
import json
import time

def main(characters):
    print(f"There are {len(characters[1:])} characters")
    root = Tk()
    labelfont = ('times', 16, 'bold')  # family, size, style
    exit_button = Button(root, text='Exit', command=off)
    exit_button.pack(expand=YES, fill=BOTH)
    # ici on va créer une instance de character() pour chacun des caractères passés
    [character(char, root, labelfont) for char in characters[1:]]
    root.mainloop()


def off():
    '''
    On quitte et on imprime le dictionnaire contenant les statistiques
    :return:
    '''
    print(stats_dict)
    with open('stats.json', 'w') as json_file:
        json.dump(stats_dict, json_file)
    exit(0)




class character:
    '''
    Crée un objet "caractère" qui est un bouton clickable qui enregistre la valeur
    dans le presse-papier quand on clique dessus.
    '''
    def __init__(self, char, root, labelfont):
        self.char = char
        self.button = Button(root, text=self.char, command=self.click)
        self.button.config(font=labelfont)  # use a larger font
        self.button.config(height=1, width=3)  # initial size: lines,chars
        self.button.pack(expand=YES, fill=BOTH)

    def __repr__(self):
        print(self.char)

    def click(self):
        print(f"You just clicked on {self.char}")
        self.add_to_table(self.char)
        pyperclip.copy(self.char)
        time.sleep(.5)
        pyautogui.hotkey("CTRL", "v")

    def add_to_table(self, character):
        '''
        Ici on va avoir des statistiques sur les boutons les plus utilisés.
        De la sorte on pourra adapter la position de chaque bouton pour être
        le plus ergonomique possible.
        :param character:
        :return:
        '''
        try:
            stats_dict[character] += 1
        except KeyError as error:
            stats_dict[character] = 1



if __name__ == '__main__':
    stats_dict = {}
    if len(sys.argv) == 1:
        main([None, 'n̈', '⁊', 'oᷤ', 't', 'ſ', 'ſt', 'ṗ', 'ꝛ', 'q̄', 'q̇', '̇̇̇̇̇', 'ṁ', 'ꝛ', 'u̇', 'ũ', 'ṅ', 'ꝫ', 'ō', 'ṅ', 'u̇', 'p̄', 'ꝑ', 'ḋ'])
    else:
        main(sys.argv)
