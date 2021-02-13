from tkinter import *
import pyautogui
import pyperclip
import json
import time


def main(characters):
    print(f"There are {len(characters)} characters")
    new_order = order_characters(characters)
    print(f"Target characters:\n{characters}")
    print(f"New order:\n{new_order}")
    root = Tk()
    root.title("cvirtuel")
    labelfont = ('times', 16, 'bold')  # family, size, style
    exit_button = Button(root, text='Save/Exit', command=save_and_exit)
    exit_button.grid(column=1, columnspan=2, row=1)

    # ici on va créer une instance de character() pour chacun des caractères passés, et on organise
    # la grille. Revoir le tout, ce n'est pas très clair.
    nombre_lignes = len(new_order) // 2  # nombre de ligne visé
    modulo = len(new_order) % 2  # on regarde si c'est divisible par deux
    if modulo == 0:
        nombre_lignes -= 1  # si ce n'est pas divisible, il faut ajouter une ligne à la première colonne.

    n = 1
    for char in new_order:
        n += 1
        if n <= nombre_lignes + 2:
            character(char, root, labelfont, 1, n)
        else:
            character(char, root, labelfont, 2, n - nombre_lignes - 1)

    root.mainloop()

def save_and_exit():
    save_frequency()
    exit_app()

def save_frequency():
    '''
    On enregiste et on imprime le dictionnaire contenant les statistiques
    :return: None
    '''
    print("Enregistrement de la fréquence")
    print(stats_dict)
    with open('stats.json', 'w') as json_file:
        json.dump(stats_dict, json_file)

def exit_app():
    exit(0)


def order_characters(target_characters):
    '''
    Cette fonction permet d'ordonner la liste de caractères
    en fonction de leur fréquence d'utilisation.
    :param target_characters: La liste de caractères à afficher
    :return: La liste ordonnée
    '''
    try:
        with open('stats.json', 'r') as json_file:
            try:
                frequency_dict = json.load(json_file)
            except ValueError as e:
                frequency_dict = {}
    except FileNotFoundError as e:
        with open('stats.json', 'w') as json_file:
            frequency_dict = {}
            json.dump(frequency_dict, json_file)
    print(frequency_dict)
    # on transforme le dictionnaire en liste ordonnée par fréquence
    sorted_list = [pair[0] for pair in sorted(frequency_dict.items(), key=lambda item: item[1], reverse=True)]

    # on ne garde parmi la liste ordonnée que les caractères qui sont présents dans les caractères
    # demandés par l'utilisateur lors du lancement de la fonction
    output_sorted_list = []
    for i in sorted_list:
        print(i)
        if i in target_characters:
            print(f"{i} is in target_characters")
            output_sorted_list.append(i)
        else:
            print(f"removing {i}")
    # on veut ici récupérer les nouveaux caractères qui n'ont jamais été vus par le programme
    nouveaux_caracteres = []
    for i in target_characters:
        if i in output_sorted_list:
            pass
        else:
            nouveaux_caracteres.append(i)

    # et on les ajoute à la fin de la liste ordonnée. 
    liste_finale_ordonnee = output_sorted_list + nouveaux_caracteres
    return liste_finale_ordonnee


class character:
    '''
    Crée un objet "caractère" qui est un bouton clickable qui enregistre la valeur
    dans le presse-papier quand on clique dessus.
    '''

    def __init__(self, char, root, labelfont, column, row):
        self.position = [column, row]
        self.char = char
        self.button = Button(root, text=self.char, command=self.click)
        self.button.grid(column=column, row=row)
        self.button.config(font=labelfont, height=1, width=3)

    def __repr__(self):
        print(self.char)

    def click(self):
        """
        On clique, on copie, on colle.
        :return: None
        """
        global click_number
        click_number += 1
        print(click_number)
        if click_number % 20 == 0:
            save_frequency()
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
        :param character: Le caractère à ajouter à la table de fréquences
        :return: None
        '''
        try:
            stats_dict[character] += 1
        except KeyError as error:
            stats_dict[character] = 1


if __name__ == '__main__':

    click_number = 0
    try:
        with open('stats.json', 'r') as json_file:
            try:
                stats_dict = json.load(json_file)
            except ValueError as e:
                stats_dict = {}
    except FileNotFoundError as e:
        stats_dict = {}

    try:
        with open("characters.conf", "r") as chars_file:
            characters = chars_file.read().replace(' ', '').replace('\n', '').split(',')
    except FileNotFoundError as error:
        print("Veuillez créer le fichier characters.conf et y ajouter les caractères à afficher.")
        exit()
    main(characters)
