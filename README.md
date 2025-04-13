# Assistant Planner
> Une tentative naïve à la résolution d'un problème d'optimisation en utilisant Pymoo.

## Description du problème
Une compagnie d'ascenseurs voudrait un assistant digital pour la planification hebdomadaire du travail.

### Contraintes
- No parallel jobs.
- Technician __Eligibility__.
- Technician __Availability__.
- Respect d'une __Due Date__ pour certains jobs.

## Définition du problème

Après un peu de lecture dans ce vaste domaine appelé *SCHEDULING*, on s'aperçoit qu'il s'agit d'un cas classique appelé: *Parallel Machines*.

### Modélisation

> Au final, comme beaucoup de choses dans cet univers, ce sont des mathématiques. Nous devons alors modéliser notre problème pour pouvoir le résoudre.

### Définition des contraintes
- __Non-preemptive__: les jobs ne peuvent pas être interrompus et repris.
- __Identical Machines__: Le Processing Time d'un job est indépendant de la machine.
- __Sequential Setup Times__: Il y a un temps de préparation entre chaque job, ce temps dépend de la séquence de jobs.
- __Machine eligibility constraints__: Les techniciens ne possèdent pas les mêmes skills.
- __Machine availability constraints__: Les techniciens ne travaillent pas 24h/24h.

### Définition des Variables
Soit pour $j$ un job, on définit son/sa:
- $p_j$: processing time.
- $s_j$: starting time.
- $C_j$: completion time.
- $d_j$: due date.
- $w_j$: weight.
- $t_j = C_j - d_j$: tardiness.

Note: One of the tardiness definitions was redundant and incorrect, so I removed it.

### La Fonction Objectif
> La fonction objectif est la fonction qu'on souhaite optimiser (minimiser dans ce cas-ci).

Nous avons choisi la fonction __Total Weighted Completion Time__, $j \in \{1,2,...,n\}$ avec $n$ jobs.

$f = \sum_{j=1}^{n} w_j C_j$

> La définition des poids $w_j$ se fait en fonction de la priorité des jobs. Un job très urgent aura un poids élevé.

### Contraintes sur Pymoo
Les contraintes sur Pymoo doivent être sous forme d'inégalité.

Nous avons défini une et une seule contrainte:

$|t_j| \leq 0$

On voudrait que les jobs soient complétés à temps, en d'autres termes on voudrait que leur __tardiness__ et leur __earliness__ soient très petites. Cela revient à ce que $|C_j - d_j|$ soit très petit.

> Un problème est qu'en forçant Pymoo à respecter la contrainte on pourrait ne jamais trouver de solution. C'est pour cela qu'on utilise une feature de Pymoo appelée __Constraint Violation as Penalty__, ce qui nous permet plus de flexibilité.