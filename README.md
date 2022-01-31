<img src="https://github.com/HugJax/EOS/blob/main/Images/logo%20eos.png" width="350">   

Notre projet a pour vocation de promouvoir le développement des PME en leur proposant un outil adapté à leur besoin et à leurs moyens, leur permettant ainsi de mieux lutter contre la concurrence des grands groupes nationaux et internationaux. Pour ainsi dire, offrir aux petites entreprises une solution qui favorise leur développement et leur expansion sur le marché.
Une solution personnalisée et adaptée aux besoins de l’utilisateur permet ainsi d’accompagner l’entreprise dans une production plus automatisée et donc le développement de ces dernières.


## Accès
* [Codes](https://github.com/HugJax/EOS/tree/main/Codes)
* [Schéma électronique](https://github.com/HugJax/EOS/tree/main/Electronique)
* [Modèles 3D](https://github.com/HugJax/EOS/tree/main/Mod%C3%A8les%203D) ou sur [Thingiverse](https://www.thingiverse.com/thing:5220804)


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
* Quatre résistances de 10kΩ et un de 5kΩ  

Un [tutoriel](https://raspberrypi-tutorials.fr/construire-une-balance-numerique-raspberry-pi-avec-capteur-de-poids-hx711/) vous permet de construire la balance que nous avons utilisé.  


## Contribution
Si vous voulez contribuer au développement de ce projet, toute contribution d'une personne enthousiaste est la bienvenue. Pour cela, le projet EOS a maintenant un miroir sur GitHub, pour simplifier la vie de tout le monde ! Toutes les corrections de bogues, les nouvelles fonctionnalités, les nouveaux tutoriels, etc. doivent être soumis via le mécanisme de pull requests de GitHub.

Si vous n'êtes pas familier avec ce mécanisme, ne vous inquiétez pas, c'est très simple. Continuez à lire.

### Une introduction en bref
* Installer Git
* Enregistrez-vous sur GitHub. Créez votre fork du dépôt EOS https://github.com/HugJax/EOS (voir https://help.github.com/articles/fork-a-repo pour les détails)
* Choisissez une tâche pour vous-même. Il peut s'agir d'une correction de bogue ou d'un nouveau code
* Créez une branche de base pour votre travail
* Clonez votre fork sur votre ordinateur. Vous pouvez installer le hook pre-commit par défaut en renommant EOS/.git/hooks/pre-commit.sample en EOS/.git/hooks/pre-commit - cela vous évitera de commettre des erreurs d'espacement
* Créez une nouvelle branche (avec un nom significatif) à partir de la branche de base que vous avez choisie
* Modifiez ou ajoutez les codes/fichiers
* Lorsque vous avez terminé, push votre branche vers votre fork GitHub, puis créez une demande de transfert de votre branche vers la branche de base (voir https://help.github.com/articles/using-pull-requests pour plus de détails)

### Faire un bon pull request
En suivant ces directives, vous augmenterez les chances que votre demande soit acceptée :
* Avant de pousser votre PR vers le dépôt, assurez-vous qu'il se construit correctement sur votre système local
* Ajoutez suffisamment d'informations, comme un titre significatif, la raison pour laquelle vous avez fait la livraison et un lien vers la page du problème si vous en avez ouvert une pour ce PR
* Limitez votre PR à un seul problème. Avant de soumettre, assurez-vous que le diff ne contient pas de changements sans rapport. Si vous souhaitez couvrir plus d'un problème, soumettez vos modifications pour chacun d'entre eux dans des demandes de retrait distinctes
* Si vous avez ajouté une nouvelle fonctionnalité, vous devez mettre à jour/créer la documentation correspondante, ainsi qu'ajouter des tests pour cette fonctionnalité à la suite de tests
* Essayez de ne pas inclure de commits "oups" - ceux qui corrigent simplement une erreur dans le commit précédent. Si c'est le cas, avant de soumettre, intégrez ces corrections directement dans les commits auxquels elles appartiennent
* Veillez à ajouter un test pour la nouvelle fonctionnalité ou un test qui reproduit le bogue corrigé avec les données de test correspondantes. N'ajoutez pas d'images ou de vidéos supplémentaires, si certains des fichiers multimédias existants conviennent
* Veillez à ajouter un test de performance, si vous proposez une optimisation ou si le correctif peut affecter les performances d'une fonctionnalité majeure

Un grand merci à vous si cous nous aidez à développer ce projet en y contribuant.
