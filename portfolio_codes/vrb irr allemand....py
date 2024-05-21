
import random,sys

infir="fallen fangen halten hängen lassen laufen raten schlafen fahren graben laden ein/laden schaffen schlagen tragen wachsen waschen essen fressen geben geschehen lesen sehen treten vergessen stehlen befehlen empfehlen brechen gelten helfen nehmen sprechen sterben treffen werfen heben bieten fliegen fliehen flieBSen genieBSen schieBSen ziehen gleichen reiten (sich)streiten bleiben leihen scheinen schreiben schreien schweigen steigen vermeiden binden finden gelingen singen springen trinken verschwinden zwingen beginnen gewinnen schwimmen bitten gehen heiBSen kommen liegen lügen rufen schwören sitzen stehen tun bringen denken kennen nennen wissen haben sein werden"
iinfir=infir.split()
ppresent="fällt fängt hält hängt lässt läuft rät schläft fährt gräbt lädt lädt-ein schafft schlägt trägt wächst wäscht isst frisst gibt geschieht liest sieht tritt vergisst stiehlt befiehlt empfiehlt bricht gilt hilft nimmt spricht stirbt trifft wirft hebt bietet fliegt flieht flieBSt genieBSt schieBSt zieht gleicht reitet streitet bleibt leiht scheint schreibt schreit schweigt steigt vermeidet bindet findet gelingt singt springt trinkt verschwindet zwingt beginnt gewinnt schwimmt bittet geht heiBSt kommt liegt lügt ruft schwört sitzt steht tut bringt denkt kennt nennt weiBS hat ist wird"
pppresent=ppresent.split()
ppreterit="fiel fing hielt hing lieBS lief riet schlief fuhr grub lud lud-ein  schuf schlug trug wuchs wusch aBS fraBS gab geschah las sah trat vergass stahl befahl empfahl brach galt half nahm sprach starb traf warf hob bot flog floh floss genoss schoss zog glich ritt stritt blieb lieh schien schrieb schrie schwieg stieg vermied band fand gelang sang sprang trank verschwand zwang begann gewann schwamm bat ging hieBS kam lag log rief schwor saBS stand tat brachte dachte kannte nannte wusste hatte war wurde"
pppreterit=ppreterit.split()
pparfait="ist gefallen  hat gefangen  hat gehalten  hat gehangen  hat gelassen  ist gelaufen  hat geraten  hat geschlafen  ist gefahren  hat gegraben  hat geladen  hat eingeladen  hat geschaffen  hat geschlagen  hat getragen  ist gewaschen  hat gewaschen  hat gegessen  hat gefressen  hat gegeben  ist geschehen  hat gelesen  hat gesehen  ist getreten  hat vergessen  hat gestohlen  hat befohlen  hat empfohlen  hat gebrochen  hat gegolten  hat geholfen  hat genommen  hat gesprochen  ist gestorben  hat getroffen  hat geworfen  hat gehoben  hat geboten  ist geflogen  ist geflohen  ist geflossen  hat genossen  hat geschossen  hat gezogen  hat geglichen  ist geritten  hat gestritten  ist geblieben  hat gelieben  hat geschienen  hat geschrieben  hat geschrien  hat geschwiegen  ist gestiegen  hat vermeiden  hat gebunden  hat gefunden  ist gelungen  hat gesungen  ist gesprungen  hat getrunken  ist verschwunden  hat gezwungen  hat begonnen  hat gewonnen  ist geschwommen  hat gebeten  ist gegangen  hat geheiBSen  ist gekommen  hat gelegen  hat gelogen  hat gerufen  hat geschworen  hat gesessen  hat gestanden  hat getan  hat gebracht  hat gedacht  hat gekannt  hat gennant  hat gewusst  hat gehabt  ist gewesen  ist geworden"
ppparfait=pparfait.split("  ")
ttrad="tomber attraper tenir,s'arreter etre_suspendu laisser courir conseiller,deviner dormir aller(vehicule) creuser charger inviter creer frapper porter grandir laver manger manger(animaux) donner se_produire lire voir marcher oublier voler,derober ordonner recommander briser valoir aider prendre parler mourir rencontrer jeter/lancer soulever offrir voler fuir couler(eau) profiter_de tirer(arme) tirer(une_porte) ressembler faire_de_l'équitation (se)disputer rester prêter briller,paraître écrire crier se_taire monter éviter lier,attacher trouver réussir chanter sauter boire disparaître obliger commencer gagner nager prier,demander aller s'appeler venir être_allongé mentir appeler promettre être_assis être_debout faire apporter penser connaître nommer savoir avoir être devenir"
tttrad=ttrad.split()

infinitif,present,preterit,parfait,trad=[],[],[],[],[]
globalite=[infinitif,present,preterit,parfait,trad]
glob=["infinitif","present","preterit","parfait","trad"]

tab=[0,8,17,25,28,36,37,44,47,55,63,66,77,82]
tabl=list(tab)
#On rempli les listes

a=0
for Items in iinfir:
  infinitif.append(iinfir[a])
  a+=1


a=0
for Items in pppresent:
  present.append(pppresent[a])
  a+=1

a=0
for Items in pppreterit:
  preterit.append(pppreterit[a])
  a+=1

a=0
for Items in ppparfait:
  parfait.append(ppparfait[a])
  a+=1

a=0
for Items in tttrad:
  trad.append(tttrad[a])
#  print(Items)
  a+=1


##for x in trad:
##  
##  print(x)

def entrain():

  """Choix tableau, forme hasard, verification fautes"""

  try:
    choix=int(input("Quel tableau voulez-vous réviser?\n(tableau 1-14  / tout : 0)\n"))
  except:
    print("Il semblerait que vous avez saisi autre chose qu'un entier...\n")
    entrain()
    
  if (0<choix<15):

    b1=tabl[choix-1]
    b2=tabl[choix]
    
  elif choix==0:
    b1=0
    b2=85
  elif choix==100:
    b1=0
    b2=28
    
  else:
    print("Vous avez bien saisi un entier, mais il ne se situe pas dans l'intervalle [0;15]...\n")
    entrain()
             
    
  while input("\nQuitter=\"q\", sinon frappez ce que vous voulez.\n")!="q":

    num=random.randint(b1,b2)
    tmps=random.choice(globalite)
    time=glob[globalite.index(tmps)]
    print(time,":",tmps[num])
    for temps in globalite:
      if temps!=tmps:
        entree=input("%s : "%glob[globalite.index(temps)])
        if entree==temps[num]:
          print("\nCorrect!\n")
        else:
          print("\nFaux!\n","C'était ",temps[num],".\n")
      else:
        print("forme donnee: %s : %s.\n"%(glob[globalite.index(temps)],temps[num]))
  menu()
def tab():
  for a in range(0,1):
    print()
    
    
def lecon():
  """Sort les formes verbales de maniere organisee"""
  max_i=0
  for mot in infinitif:
    if len(mot)>max_i:
      max_i=len(mot)
    
  max_pres=0
  for mot in present:
    if len(mot)>max_pres:
      max_pres=len(mot)
    
  max_pret=0
  for mot in preterit:
    if len(mot)>max_pret:
      max_pret=len(mot)
    
  max_par=0
  for mot in parfait:
    if len(mot)>max_par:
      max_par=len(mot)
    
  max_t=0
  for mot in trad:
    if len(mot)>max_t:
      max_t=len(mot)
  for x in range(75):
    print("%s%s | %s%s | %s%s | %s%s | %s\n"%(infinitif[x]," "*(max_i-len(infinitif[x])), present[x]," "*(max_pres-len(present[x])), preterit[x]," "*(max_pret-len(preterit[x])), parfait[x]," "*(max_par-len(parfait[x])), trad[x]) )
  menu()
def menu():

  choix=input("\nChoisissez votre type d'entraînement:\n1) Tableau des verbes.\n2) Random verbe.\n[q=quitter]\n")
  if choix=="1":
    lecon()

  elif choix=="2":
    entrain()
  
  elif choix=="q":
    sys.exit()

  else:
    print("\nChoix non valide!\n")
    menu()
  

if __name__== "__main__":
  print("Entraînement des verbes forts\nRomain David\nAnnee 2017_2018\n")
  menu()

