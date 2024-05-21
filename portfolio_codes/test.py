def arretes_to_liste_adjacence(arretes):
    liste_adj = {}
    for paire in arretes:
        upadte_dico(s1, defs2)
        if sommet1 in liste_adj:
            liste_adj[sommet1].append(sommet2)
        else:
            liste_adj[sommet1] = [sommet2]

    return liste_adj

def parcours(sommet, liste_adj):
    visites = set()
    pile = set([sommet])
    while pile:
        n_visite = pile.pop()
        visites.add(n_visite)
        for nei in liste_adj[n_visite]:
            if not((nei in visites) or (nei in pile)):
                pile.add(nei)
    return visites

def comp_connexes(liste_paire_sommets):
    liste_adj = arretes_to_liste_adjacence(liste_paire_sommets)
    tout_sommets = list(liste_adj.keys())
    composantes = []
    while tout_sommets:
        premier_sommet = list(tout_sommets)[0]
        comp = parcours(premier_sommet, liste_adj)
        composantes.append(comp)
        for sommet in comp:
            tout_sommets.remove(sommet)
    return composantes


liste_paire_sommets = [["A", "B"], ["B", "C"], ["R", "F"]]
print(comp_connexes(liste_paire_sommets))
    
    
class Graphe:
    
    