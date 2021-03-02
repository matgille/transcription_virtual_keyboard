#!/usr/bin/env python3.7
from tkinter import *
import pyautogui
import pyperclip
import json
import time

# TODO: régler le problème de position et de taille du formulaire de recherche.

class VirtualKeyboard:
    def __init__(self, characters, height, labelfont):
        new_order = order_characters(characters)
        print(f"Target characters:\n{characters}")
        print(f"New order:\n{new_order}")
        root = Tk()
        root.title("cvirtuel")
        default_bg_color = root.cget('bg')

        exit_button = Button(root, text='Save/Exit', command=save_and_exit)
        exit_button.grid(column=0, columnspan=2, row=1)
        update_grid_button = Button(root, text='Reorder',
                                    command=lambda: update_grid(root, new_order,
                                                                default_bg_color, height))  # https://stackoverflow.com/a/6921225
        update_grid_button.grid(column=2, columnspan=2, row=1)
        search_form = Entry(root, textvariable='Search')
        search_form.grid(row=1, column=6, columnspan=1)
        search_form.config(fg='grey')
        search_form.insert(END, "Search for combining chars")

        # On crée une variable globale pour pouvoir la modifier à l'intérieur de la classe. Je ne sais pas si c'est
        # très pythonique !
        global liste_object_character
        liste_object_character = set_grid(labelfont, root, new_order, default_bg_color, height)

        root.bind('<Return>', lambda _: get_character(search_form, liste_object_character, default_bg_color))
        search_form.bind("<Enter>", lambda _: handle_focus_in(search_form))
        search_form.bind("<Leave>", lambda _: handle_focus_out(search_form, root))
        root.mainloop()


def get_character(form, liste, default_bg_color):
    """
    Cette fonction récupère le caractère cherché dans le formulaire et active la fonction de surbrillance.
    :param form: le formulaire qui est un objet Entry
    :param liste: la liste d'objets des objets de classe character.
    :return: None
    """
    print(f"Searched character: {form.get()}")
    clean_color(default_bg_color)
    searched_character = form.get()
    find_char_and_colour_it(searched_character, liste)


def find_char_and_colour_it(character, liste):
    '''
    Cette fonction permet de changer le fond des boutons ayant un caractère précis.
    :param character: le caractère à trouver
    :param liste: la liste d'objets character() instanciée.
    :return:
    '''
    # Ça ne marche aps quand on update car les objets sont détruits et remplacés par de nouveaux objets. Il
    # faut mettre à jour la liste à chaque update.
    matching_button_objects_index = [liste.index(button) for button in liste if character in button.char]
    print(matching_button_objects_index)
    for button in matching_button_objects_index:
        print(liste[button].char)
        liste[button].button.config(bg='red')


def set_grid(police, tkinter_racine, liste_caracteres, default_bg_color, hauteur):
    """
    Cette fonction permet d'organiser la grille par création d'instances de la classe `character`
    qui sont des boutons dont la position est déterminée par cette fonction.
    :param default_bg_color:
    :param hauteur:
    :param police:
    :param tkinter_racine:
    :param liste_caracteres:
    :return:
    """
    # Organisation de la grille
    n = 0
    nombre_lignes = hauteur  # nombre de lignes de chaque colonne: hauteur de l'interface graphique.
    list_char_objects = []
    for char in liste_caracteres:
        ligne = (n % nombre_lignes) + 2
        colonne = (n // nombre_lignes)
        list_char_objects.append(
            Character(char, tkinter_racine, police, colonne, ligne, liste_caracteres, default_bg_color)
        )
        n += 1
    return list_char_objects


# https://stackoverflow.com/a/51781808
def handle_focus_in(search_form):  # https://stackoverflow.com/a/51781808
    search_form.delete(0, END)
    search_form.config(fg='black')
    search_form.focus_set()


def handle_focus_out(search_form, root):  # https://stackoverflow.com/a/51781808

    search_form.delete(0, END)
    search_form.config(fg='grey')
    search_form.insert(0, "Search combined chars")
    root.focus()


def clean_color(default_bg_color):
    global liste_object_character
    for character_object in liste_object_character:
        character_object.button.config(bg=default_bg_color)


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


def update_grid(root, liste_caracteres, default_bg_color, hauteur):
    """
    Cette fonction met à jour la grille en fonction de la fréquence ainsi que la liste d'objets de classe character.
    :param hauteur: hauteur de la grille
    :param default_bg_color: La couleur du fond produite par défaut
    :param root: l'instance tkinter produite
    :param liste_caracteres: la liste de caractères originelle.
    :return:None
    """
    global liste_object_character
    liste_object_character = set_grid(('times', 16, 'bold'), root, order_characters(liste_caracteres), default_bg_color, hauteur)


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
    # on transforme le dictionnaire en liste ordonnée par fréquence
    sorted_list = [pair[0] for pair in sorted(frequency_dict.items(), key=lambda item: item[1], reverse=True)]

    # ici on nettoie la liste triée et on ne garde que les éléments indiqués dans la liste définie par l'utilisateur/ice
    output_sorted_list = []
    for i in sorted_list:
        if i in target_characters:
            output_sorted_list.append(i)
        else:
            pass

    # ici au contraire on supprime dans la liste définie les éléments qui sont présents dans la liste triée, car ce
    # serait redondant.
    nouveaux_caracteres = []
    for i in target_characters:
        if i in output_sorted_list:
            pass
        else:
            nouveaux_caracteres.append(i)

    # et on les ajoute à la fin de la liste ordonnée. 
    liste_finale_ordonnee = output_sorted_list + nouveaux_caracteres
    print(len(liste_finale_ordonnee))
    return liste_finale_ordonnee


class Character:
    '''
    Crée un objet "caractère" qui est un bouton clickable qui enregistre la valeur
    dans le presse-papier quand on clique dessus.
    '''

    def __init__(self, char, root, labelfont, column, row, liste_caracteres, default_bg_color):
        self.position = [column, row]
        self.char = char
        self.root = root
        self.character_list = liste_caracteres
        self.labelfont = labelfont
        self.button = Button(root, text=self.char, command=lambda: self.click(default_bg_color))
        self.button.grid(column=column, row=row)
        self.button.config(font=labelfont, height=1, width=3)

    # def __repr__(self):
    # print(self.char)

    def click(self, default_bg_color):
        """
        On clique, on copie, on colle.
        :return: None
        """
        save_frequency()
        clean_color(default_bg_color)  # on réinitialise la couleur de tous les boutons.
        print(f"You just clicked on {self.char}")
        self.add_to_frequency_table(self.char)
        pyperclip.copy(self.char)
        time.sleep(.5)
        pyautogui.hotkey("CTRL", "v")

    def add_to_frequency_table(self, character):
        '''
        Ici on va avoir des statistiques sur les boutons les plus utilisés.
        De la sorte on pourra adapter la position de chaque bouton pour être
        le plus ergonomique possible.
        :param character: Le caractère à ajouter à la table de fréquences
        :return: None
        '''
        try:
            stats_dict[character] += 1
        except KeyError as _:
            stats_dict[character] = 1


if __name__ == '__main__':

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

    VirtualKeyboard(characters, height=15, labelfont=('times', 16, 'bold'))
