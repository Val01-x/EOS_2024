# Fonctionnement du code

Le code proposé se veut simple et facile à adapter. 

![interface](https://github.com/HugJax/EOS/blob/main/Images/interface2.png)


## Connexion entre raspberry et code
On peut retrouver les variables à modifier :
* Les informations pour les branchements de l'écran LCD à la ligne 11
* Les branchements des boutons se situent à la ligne 13
  * Bouton 0 = action ligne 1
  * Bouton 1 = action ligne 2
  * Bouton 2 = action valider
  * Bouton 3 = action retour
* Gestion du moteur des lignes 26 à 36

## Axes d'amélioration
Nous avons imaginé plusieurs axes d'amélioration pour l'avenir :
* ajout d'une solution visuelle pour voir les différentes étapes de mise en sachet
* mise en place d'un système de répétition pour l'ensachage de plusieurs sachets à la suite
* mettre en option le choix de vitesse de l'hélice
