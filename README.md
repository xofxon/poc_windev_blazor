Le 25 novembre 2025

Dans le cadre de ma recherche de récupération d'éléments écrits en Windev pour les utiliser dans un autre language, j'ai commencé à écrire, avec Gemini, deux scripts python.

Le premier "clarification_windev.py" va faire un peu de ménage pour, à partir d'une fenêtre windev enregistrée en texte et pas en binaire, éliminer ce qui ne peut, a priori, pas être exploité en dehors de l'éditeur Windev et l'enregistrer dans un nouveau fichier texte. Il s'appuie sur les deux fichier "correspondance_controls.txt" et "correspondance_evenements.txt" pour identifier champs et évènements. 
Ces deux fichiers sont très incomplets et ne demandent qu'à être enrichis.
Le second "creation_de_squelette_balzor_a_partir_de_fenêtre windev.py" va créer, en lisant les fichiers créés par le premier script, et en créant des squelettes de fichiers blazor. La traduction du code windev en c# n'est pas opérationnelle et je ne sais pas encore si je l'intégrerai dans ce script ou si j'essaierai d'utiliser une IA qui saurait le faire, via un troisième script.

Les cartouches des deux scripts sont réputés expliquer sommairement l'attendu et les arguments de la ligne de commande.

Les quatre fichiers sont dans le répertoire exploitable par python, dans cet exemple.

Exemple :
python .\\clarification_windev.py --dir "C:\Mes Projets\Mon_Projet_texte"

lira tous les fichiers *.wdw du répertoire sus-nommé et déposera les fichiers retravaillés dans un sous-répertoire "clarifications" en changeant l'extension de "wdw" en "wdw.clair".

python .\\creation_de_squelette_balzor_a_partir_de_fenetre_windev.py --dir "C:\Mes Projets\Mon_Projet_texte" --lang fr

lira tous les fichiers du sous répertoire "clarifications" du répertoire sus-nommé et déposera les fichiers créés dans un sous-répertoire "sqelettes". Deux fichiers seront créé par fichier lu. Un avec l'extension ".razor" et l'autre avec l'extension ".razor.cs".

Les deux scripts produisent également des .log réputés donner quelques éclairages sur le déroulé de chacun des scripts.

En exemple, 4 fichiers, "pentnom.wdw" (windev 2025), qui sera exploité par le premier script et qui produira "pentnom_wdw.clair" qui sera exploité par le second script qui produira "pentnom.razor" et "pentnom.razor.cs".


