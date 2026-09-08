<p align="center">
  <a href="README.ja.md">日本語</a> | <a href="README.zh.md">中文</a> | <a href="README.es.md">Español</a> | <a href="README.md">English</a> | <a href="README.hi.md">हिन्दी</a> | <a href="README.it.md">Italiano</a> | <a href="README.pt-BR.md">Português (BR)</a>
</p>

<p align="center">
  <img src="https://raw.githubusercontent.com/mcp-tool-shop-org/brand/main/logos/schumann-surface/readme.png" alt="Schumann Surface" width="400">
</p>

<p align="center">
  <a href="https://github.com/mcp-tool-shop-org/schumann-surface/actions/workflows/ci.yml"><img src="https://github.com/mcp-tool-shop-org/schumann-surface/actions/workflows/ci.yml/badge.svg" alt="CI"></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-MIT-blue.svg" alt="MIT"></a>
  <a href="https://mcp-tool-shop-org.github.io/schumann-surface/"><img src="https://img.shields.io/badge/landing-page-0ea5e9" alt="Landing page"></a>
  <a href="https://huggingface.co/datasets/mcp-tool-shop/schumann-sierra-nevada"><img src="https://img.shields.io/badge/dataset-Hugging%20Face-ffcc4d" alt="Dataset"></a>
</p>

<p align="center"><a href="README.md">English</a> · <a href="README.ja.md">日本語</a> · <a href="README.zh.md">中文</a> · <a href="README.es.md">Español</a> · <a href="README.fr.md">Français</a> · <a href="README.hi.md">हिन्दी</a> · <a href="README.it.md">Italiano</a> · <a href="README.pt-BR.md">Português (BR)</a></p>

# schumann-surface

Résonance de Schumann présentée sous forme de surface 3D temps-fréquence avec des lignes d’événements et une analyse de corrélation croisée honnête et décalée. Un mois de données réelles d’une station ELF, permettant de visualiser le rythme quotidien des éclairs, les bandes de modes et l’impact d’une tempête géomagnétique (et ce qu’elle n’impacte pas).

État : v1.0.0. Octobre et juin 2013, données de la station ELF de Sierra Nevada (Université de Grenade), reproduites en comparant les données aux spectres et aux ajustements de modes publiés par la station, segment par segment ; les dix mois restants des données brutes sont traités par le même processus. Le visualiseur est un seul fichier HTML autonome avec quatre modes ; disponible en direct sur la [page d’accueil](https://mcp-tool-shop-org.github.io/schumann-surface/viewer/).

## Ce que cela montre

- **Surface** : temps (un mois, colonnes de 30 minutes) × fréquence (6–25 Hz, lignes de 0,125 Hz) × amplitude magnétique en dB par rapport à 1 pT/√Hz. Les capteurs NS et EW sont présentés sous forme de deux plans superposables.
- **Bandes de modes** : fréquence centrale ajustée des modes 1 à 3, affichée sur la surface.
- **Lignes d’événements** devant la surface : indice géomagnétique Kp (toutes les 3 heures, GFZ), heure locale à la station (calculée à partir de l’horodatage), tremblements de terre de magnitude 6 ou plus (USGS).
- **Panneau de corrélation** : corrélation de Pearson r par rapport au décalage (±24 h) entre toute série de surface (amplitude du mode, fréquence du mode, puissance de la bande) et toute série d’événements, avec une bande de référence de 95 %, dont la taille d’échantillon effective est corrigée pour l’autocorrélation dans les deux séries (Bartlett). Une courbe à l’intérieur de la bande indique un résultat nul et est affichée en conséquence.

## Pourquoi la bande est de 6–25 Hz

La bobine de la station est un capteur RLC dont la résonance se situe près de 33 Hz et qui a été calibrée par ses auteurs pour une plage de 6–25 Hz uniquement. Au-dessus de 25 Hz, le spectre brut est dominé par la résonance du capteur, et non par la cavité, de sorte que les modes 4 et suivants ne peuvent pas être résolus avec cet instrument. Une station à plus large bande est nécessaire pour cela.

## Vérification (octobre 2013, 4 464 segments par capteur)

| Vérification par rapport aux données npz publiées par la station | NS | EW |
|---|---|---|
| Rapport du spectre d’amplitude (nos données/données de la station), 6–25 Hz (médiane, 5e percentile, 95e percentile) | 1.0000 / 1.0000 / 1.0000 | 1.0000 / 1.0000 / 1.0000 |
| Fraction de saturation par segment, corrélation | 1.000 | 1.000 |
| Fréquence centrale du mode 1, différence de la médiane | +0,004 Hz | +0,008 Hz |
| Fréquence centrale du mode 2, différence de la médiane | +0,000 Hz | +0,002 Hz |
| Fréquence centrale du mode 3, différence de la médiane | −0,000 Hz | +0,001 Hz |
| Rapport de l’amplitude maximale du mode, médiane | 1.001 / 1.000 / 1.000 | 1.001 / 1.000 / 1.000 |

La dispersion résiduelle de la fréquence est due au fait que les deux implémentations de Levenberg-Marquardt (lmfit à la station, SciPy ici) convergent vers des minimums locaux différents pour quelques pour cent des segments ; le visualiseur masque les ajustements qui sortent des fenêtres par mode documentées.

Le vérificateur est une porte : il s’arrête et renvoie une valeur non nulle, sauf si au moins 95 % des segments correspondent dans un délai de 30 secondes, si les 5e et 95e percentiles du rapport du spectre se situent dans la plage de 1 ± 0,005, si la différence de fréquence médiane de chaque mode est inférieure à 0,02 Hz et si la corrélation des séries de saturation est supérieure à 0,99.

## Ligne des éclairs : modèle, et non mesure

Il n’existe pas de série mondiale de données d’éclairs mesurées et téléchargeables publiquement pour 2013 (WWLLN est un service par abonnement, l’archive Blitzortung nécessite une connexion d’utilisateur, la climatologie LIS/OTD de la NASA est accessible via Earthdata). Le visualiseur contient donc un **calendrier de pics** en tant que ligne de modèle : trois gaussiennes par heure UTC pour l’Asie du Sud-Est, l’Afrique et les Amériques, selon Whipple 1929, la courbe de Carnegie (Harrison 2013) et la climatologie diurne LIS/OTD (Blakeslee et al. 2014). Il est étiqueté comme un modèle partout où il est affiché. Les données mesurées correspondantes sont également intégrées : la moyenne par heure UTC de l’amplitude de chaque mode sur le mois. Voir `docs/data-contract.md`.

## Données et licences

| Source | Quoi | Licence | Utilisation ici |
|---|---|---|---|
| Salinas et al., Zenodo [10.5281/zenodo.6348930](https://zenodo.org/records/6348930) | série temporelle brute de 256 Hz, mars-décembre 2013 et janvier-février 2017 | CC BY 4.0 | entrée ; les produits dérivés sont les nôtres et nous pouvons les publier avec attribution |
| Salinas et al., Digibug [10481/71563](https://digibug.ugr.es/handle/10481/71563) | spectres de 10 minutes traités par la station + ajustements de Lorentz | CC BY-NC-ND 3.0 | uniquement pour le vérificateur, jamais redistribué |
| Salinas et al. 2022, *Computers & Geosciences* 165 : 105148 ; code [asalinas62/Sierra_Nevada_SR](https://github.com/asalinas62/Sierra_Nevada_SR) | formule de calibration et chaîne de traitement | article CC BY-NC-ND ; code selon son dépôt | méthode reproduite dans `scripts/process_month.py` |
| Indice Kp de GFZ Potsdam, Matzka et al. 2021 | Kp toutes les 3 heures | CC BY 4.0 | ligne d’événements |
| Service d’événements FDSN de l’USGS | tremblements de terre | domaine public | ligne d’événements |

Rien dans `data/` n’est enregistré. L’archive Zenodo est une archive zip de 26,5 Go ; le script de récupération lit son répertoire central via des requêtes de plage HTTP et ne diffuse que le mois demandé.

## Processus

```bash
python scripts/fetch_zenodo_month.py 1310          # ~2.4 GB, one month, both sensors
python scripts/process_month.py 1310 0             # NS  -> data/derived/SN_1310_0.npz
python scripts/process_month.py 1310 1             # EW  -> data/derived/SN_1310_1.npz
python scripts/verify_against_granada.py 1310 0    # optional, needs the Digibug npz in data/granada/
python scripts/build_viewer.py 1310                # -> viewer/index.html (+ viewer/artifact.html)
python -m pytest -q tests                          # synthetic checks on the chain
```

Méthode définie (reproduit la chaîne de la station afin qu’elle puisse être vérifiée) : fenêtres Hann de 10 s, chevauchement de 50 %, FFT avec remplissage à zéro jusqu’à 8 192 (31,25 mHz), fenêtres saturées supprimées, calibration RLC `Scal(f) = 1e12/(2500·1.9e6) · sqrt((1-(f/f0)²)² + (2δf/f0)²) / f` avec L = 298 kH, C = 77,75 pF, R = 320 kΩ, filtre à ligne droite de la bande anthropique, trois fonctions de Lorentz plus un terme linéaire ajusté dans le domaine d’amplitude sur 6,35–23,75 Hz.

## Conformité aux normes

Score de 0 à 3 par rapport aux six normes de flux de travail du studio.

| Norme | Score | Preuve |
|---|---|---|
| PIN_PER_STEP | 2 | Chaque choix numérique (fenêtre, chevauchement, taille de la FFT, constantes d’étalonnage, bande d’ajustement, valeurs initiales) est une constante nommée située en haut de `process_month.py` et enregistrée dans le champ npz `method`. Pour l’instant, il n’est pas possible de garantir la compatibilité entre les différentes versions de NumPy ; aucune information sur les versions des bibliothèques n’est disponible. |
| AUTORITÉ_ANDON | 2 | `verify_against_granada.py` est le point d’arrêt en cas de désaccord avec les ajustements publiés par la station ; le script de récupération vérifie la taille décompressée de chaque entrée du fichier zip avant de l’enregistrer. |
| COMPENSATEURS_NOMMÉS | 2 | Aucun appel externe irréversible dans le processus. La seule méthode de publication consiste à effectuer une opération « git push » du code source ; `data/` est ignoré. Compensateur pour un mauvais `viewer/index.html` : reconstruire à partir du fichier npz. |
| DÉCOMPOSITION_PAR_CLÉS | 2 | Récupération, traitement, vérification et construction : il s’agit de quatre scripts, chacun ayant une tâche spécifique ; le modèle de visualisation ne connaît rien de la station et utilise un bloc JSON indépendant de la station. |
| HUMAINS_AVEC_SEUIL_D’INCERTITUDE | 1 | Le panneau de corrélation affiche la bande nulle, qui représente le seuil d’incertitude pour le visualiseur. Il n’y a pas de point de contrôle humain dans le processus lui-même. Correction : faire en sorte que le vérificateur indique si le résultat est acceptable ou non, en fonction d’une tolérance spécifiée (responsable : prochaine session). |
| VÉRIFICATEUR_EXTERNE | 3 | Le vérificateur est la sortie indépendante produite par la station (code différent, auteurs différents, lmfit par rapport à SciPy). Les chiffres se trouvent dans le tableau ci-dessus. |

## Confiance et données

Le processus s’exécute localement à partir d’une copie du code. Il ne lit et n’écrit que dans `data/` et `viewer/`. L’accès au réseau n’a lieu que lorsque vous demandez à un script d’effectuer une récupération : Zenodo (archive brute), Digibug (fichiers de vérification de la station), GFZ (Kp), USGS (tremblements de terre). Le téléchargement de l’ensemble de données utilise votre propre compte Hugging Face, en dehors de ces scripts. Aucun identifiant n’est lu ou stocké, aucune télémétrie n’est envoyée, et le visualiseur est une page statique qui charge Three.js et deux polices à partir de CDN publics, et rien d’autre. Exigences : Python 3.11 ou version ultérieure avec NumPy, SciPy et PyArrow, sur n’importe quel système d’exploitation ; Node n’est nécessaire que pour la page d’accueil facultative.

## Licence

Licence MIT pour le code. Les produits de données dérivés comportent l’attribution requise par leurs sources.

---

<p align="center">Built by <a href="https://mcp-tool-shop.github.io/">MCP Tool Shop</a></p>
