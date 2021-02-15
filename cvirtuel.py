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
    updategrid = Button(root, text='Update', command=lambda: update_grid(root, new_order)) #https://stackoverflow.com/a/6921225

    exit_button.grid(column=1, columnspan=2, row=1)
    updategrid.grid(column=3, columnspan=2, row=1)
    set_grid(labelfont, root, new_order)

    root.mainloop()


def set_grid(police, tkinter_racine, liste_caracteres):
    # Organisation de la grille
    n = 0
    nombre_caractères = len(liste_caracteres)
    nombre_lignes = 11  # nombre de lignes de chaque colonne = hauteur de l'interface graphique.
    nombre_colonnes = nombre_caractères // nombre_lignes

    for char in liste_caracteres:
        ligne = (n % nombre_lignes) + 2
        colonne = (n // nombre_lignes)
        character(char, tkinter_racine, police, colonne, ligne, liste_caracteres)
        n += 1


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


def update_grid(root, liste_caracteres):
    """
    Cette fonction met à jour la grille en fonction de la fréquence.
    :param root:
    :param liste_caracteres:
    :return:
    """
    print("Mise à jour de la grille.")
    print(f"Ordre avant mise à jour: \n{liste_caracteres}")
    set_grid(('times', 16, 'bold'), root, order_characters(liste_caracteres))
    print(stats_dict)
    print(f"Ordre après mise à jour: \n{order_characters(liste_caracteres)}")


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

    # on ne garde parmi la liste ordonnée que les caractères qui sont présents dans les caractères
    # demandés par l'utilisateur lors du lancement de la fonction
    # TODO:: vérifier le problème de perte de caractères.
    output_sorted_list = []
    for i in sorted_list:
        if i in target_characters:
            output_sorted_list.append(i)
        else:
            pass
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

    def __init__(self, char, root, labelfont, column, row, liste_caracteres):
        self.position = [column, row]
        self.char = char
        self.root = root
        self.character_list = liste_caracteres
        self.labelfont = labelfont
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
