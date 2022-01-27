# EOS
Notre projet a pour vocation de promouvoir le développement des PME en leur proposant un outil adapté à leur besoin et à leurs moyens, leur permettant ainsi de mieux lutter contre la concurrence des grands groupes nationaux et internationaux. Pour ainsi dire, offrir aux petites entreprises une solution qui favorise leur développement et leur expansion sur le marché.
Une solution personnalisée et adaptée aux besoins de l’utilisateur permet ainsi d’accompagner l’entreprise dans une production plus automatisée et donc le développement de ces dernières.


## Accès
* [Codes](https://github.com/HugJax/EOS/tree/main/Codes)
* [Schéma électronique](https://github.com/HugJax/EOS/tree/main/Electronique)
* [Modèles 3D](https://github.com/HugJax/EOS/tree/main/Mod%C3%A8les%203D)


## Open Source
Ce projet est open source, vous pouvez donc télécharger tous les fichiers pour pouvoir adapter la solution à vos besoins.


## Matériel nécessaire
Vous pouvez trouver les codes et modèles 3D (nous vous suggérons du Z-ABS) sur ce repository. Pour modifier les modèles 3D, ces derniers ont été réalisés grâce au logiciel fusion 360.  
Pour la partie électronique, nous avons eu besoin de :
* [Cellule de charge](https://www.amazon.fr/s?k=Cellule+de+charge&__mk_fr_FR=%C3%85M%C3%85%C5%BD%C3%95%C3%91&ref=nb_sb_noss_2&tag=754fr-21)
* [HX711](https://www.amazon.fr/s?k=HX711&__mk_fr_FR=%C3%85M%C3%85%C5%BD%C3%95%C3%91&ref=nb_sb_noss_2)
* Breadboard
* Cables jumper
* Deux planches (les planches ne doivent pas se plier facilement, donc le mieux est de ne pas avoir un contreplaqué trop fin)
* Boulons plus longs + écrous correspondants
* [Raspbery Pi 3](https://www.raspberrypi.com/products/raspberry-pi-3-model-b/)
* [Driver de moteur pas à pas](https://www.amazon.fr/azdelivery-A4988-dmos-baguettes-dissipateur-thermique/dp/B01N9QOJ99/ref=sr_1_5?__mk_fr_FR=ÅMÅŽÕÑ&crid=1ULCTZJZIXN6R&keywords=a4988&qid=1643294036&s=computers&sprefix=a4988%2Ccomputers%2C87&sr=1-5)
* [Moteur pas à pas](https://www.amazon.fr/dp/B00PNEQUZ2/)
* [Ecran LCD](https://www.amazon.fr/AZDelivery-HD44780-1602-Module-16-caractères-Arduino-Display/dp/B079T264ZZ/ref=sr_1_7?__mk_fr_FR=ÅMÅŽÕÑ&crid=2UM9VVTDYC33R&keywords=écran+lcd+1602&qid=1643294070&s=computers&sprefix=écran+lcd+1602%2Ccomputers%2C92&sr=1-7)
* [Alimentation](https://www.amazon.fr/dp/B083LWHWKC)
* [Convertisseur 12V vers 5V](www.amazon.fr/Greluma-convertisseur-abaisseur-régulateur-dalimentation/dp/B08K37TS6F)
* Quatre boutons poussoirs
* Quatre résistances de 10kΩ  

Un [tutoriel](https://raspberrypi-tutorials.fr/construire-une-balance-numerique-raspberry-pi-avec-capteur-de-poids-hx711/) vous permet de construire la balance que nous avons utilisé.  
Pour l'ensemble des branchements, nous vous proposons le schéma électronique suivant :
![circuit-électronique](https://github.com/HugJax/EOS/blob/main/Electronique/circuit%20%C3%A9lectronique.png)  
Le fichier [Fritzing](https://github.com/HugJax/EOS/blob/main/Electronique/branchements%20fritzing.fzz) est également disponible pour retravailler les branchements.
