# Mini statistiques — point de départ du TP

Un dépôt par trinôme. `main` contient seulement ce point de départ ; chaque fonction est réalisée sur sa propre branche, via une issue et une pull request.

Fonctions à compléter dans `median.py`, `variance.py` et `pearson.py`. La fonction `mean` est fournie dans `mean.py`. Les fichiers séparés permettent aux trois branches d'avancer en parallèle. Les testeurs créent `tests/test_median.py`, `tests/test_variance.py` et `tests/test_pearson.py` avec `unittest`.

Contrat commun : les entrées sont des listes de nombres réels finis. Chaque fonction refuse les entrées invalides ci-dessous avec `ValueError`.

- `median(values)` : ne modifie pas la liste ; prend l'élément central si sa longueur est impaire, la moyenne des deux éléments centraux si elle est paire ; refuse la liste vide.
- `variance(values)` : variance de population, `sum((x - mean(values)) ** 2 for x in values) / len(values)` ; renvoie `0.0` pour un singleton ; refuse la liste vide.
- `pearson(xs, ys)` : covariance de population divisée par la racine carrée du produit des deux variances ; refuse les longueurs différentes, moins de deux valeurs et une série constante. Deux séries proportionnelles croissantes donnent `1.0`, décroissantes `-1.0`.

Chaque fonction a une issue, une branche et une PR vers `main`. Le développeur code et ouvre la PR, le testeur ajoute un commit de tests à cette PR, le troisième membre fait la review. Chaque personne change de rôle pour les deux autres fonctions. La description de la PR contient `Closes #N` et le résultat de la commande de test.

Lancer les tests une fois les fichiers écrits :

```sh
python3 -m unittest discover -s tests -v
```

Attention : `unittest` affiche `OK` même si aucun test n'a été découvert. Vérifier le nombre de tests exécutés.
