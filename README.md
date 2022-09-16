README

Logiciel de gestion de tâches

##Informations générales
Ce logiciel a pour but d'aider un utilisateur à gérer une liste de tâches à réaliser. Il se 
base sur l'utilisation de lignes de commande simples à entrer dans le terminal d'un 
interpréteur python.

##Description des commandes utilisateur
(remplacer toutes les instructions entre crochets par les informations réelles)
```python
python [nom du fichier python, main par défaut].py default.txt --show
```
exemple: 
```python
python main.py default.txt --show
 ```
fonction: affiche la liste des tâches sous forme de tableau
note: default.txt est le nom par défaut du fichier texte créé en local contenant les tâches.
Il peut être remplacé par un autre nom de fichier dans toutes les commandes. Si le nom de fichier
n'est pas précisé dans la commande, le fichier default.txt est utilisé.
```python
python [nom du fichier python, main par défaut].py --add [description de la tache]
python [nom du fichier python, main par défaut].py --add [description de la tache] --prio [priorité de la tache entre 1 et 5, 5 par defaut]
python [nom du fichier python, main par défaut].py --add [description de la tache] --dureeEst [temps estimé pour la tache au format 0a/00m/00j/00h/00min/00s par defaut]
```
fonction: ajoute une tâche à la liste des tâches actuelles, renvoie l'id de la nouvelle tache. 
```python
python [nom du fichier python, main par défaut].py --modify [id] [nouvelle description]
python [nom du fichier python, main par défaut].py --modify [id] [nouvelle description] --prio [nouvelle priorité]
```
fonction: modifie un élément d'une tâche actuelle de la liste, identifiée par son numéro de ligne (ou identifiant dans le tableau)
```python
python [nom du fichier python, main par défaut].py --changePriority [id] [nouvelle priorité]
python [nom du fichier python, main par défaut].py -c [id] [nouvelle priorité]
```
fonction: change la priorité d'une tâche donnée, identifiée par son numéro de ligne (ou identifiant dans le tableau)
```python
python [nom du fichier python, main par défaut].py --modifyDureeEst [id] [nouvelle duree]
python [nom du fichier python, main par défaut].py --mde [id] [nouvelle duree]
```
fonction: change la durée estimée d'une tâche donnée, identifiée par son numéro de ligne (ou identifiant dans le tableau)
```python
python [nom du fichier python, main par défaut].py --rm [id]
```
fonction: supprime une tâche donnée, identifiée par son numéro de ligne (ou identifiant dans le tableau)
```python
python [nom du fichier python, main par défaut].py --tacheFini [id] [durée réelle pour finir la tache]
```
fonction: ajoute la durée réelle qui s'est révélée nécessaire pour finir la tâche dans le tableau.
```python
python [nom du fichier python, main par défaut].py -sm
```
exemple:
```python
python main.py -sm
```
foncion: affiche la liste des méta-tâches existantes. Les méta-tâches sont des modèles de tâches 
classiques ou récurrentes qui peuvent être réutilisés pour ajouter des tâches à la liste plus 
rapidement. Chaque méta-tâche s'affichera sur 4 lignes (nom, description, priorité, durée estimée).

```python
python [nom du fichier python, main par défaut].py -cm [Nom de la metatache] [description ou None] [priorité ou None] [durée ou None]
```
fonction: créer une méta-tâche. L'ordre des arguments est à respecter, si le modèle ne prévoit pas de remplir une donnée,
remplir None
```python
python [nom du fichier python, main par défaut].py [fichier ou sauvegarder la tache] -am [Nom de la metatache a utiliser] [description ou None] [priorité ou None] [durée ou None]
```
fonction: ajoute une tâche créée à partir d'un modèle méta-tâche à la liste. Remplir None pour conserver les données
préremplies lors de la création de la méta-tâche.
