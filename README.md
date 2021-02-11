# Clavier virtuel


Ce programme permet d'afficher un clavier virtuel, conçu à faciliter la transcription
d'écritures manuscrites médiévales comprenant des abréviations et des caractères aujourd'hui
disparus. Il est assez pratique en combinaison avec des outils comme eScriptorium par exemple 
([dépôt git](https://gitlab.inria.fr/scripta/escriptorium)).

## Installation

```
git clone url.git
cd url
python3 -m venv env_clavier_virtuel
pip3 install -r requirements.txt
```

Les caractères à représenter sont à ajouter au fichier characters.conf; ils doivent être séparés par des virgules.

## Utilisation

```
python3 cvirtuel.py
```

L'interface graphique apparaît, en cliquant sur chaque caractère, un compteur se 
déclenche, le caractère est copié dans le presse-papier et sera collé 0.5s après.

Le programme ajuste la position des caractères en fonction de la fréquence de 
leur utilisation.