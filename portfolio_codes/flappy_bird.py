import pygame,time,random
from pygame.locals import *
""" 8 en Insane """

base= open ("base.txt","a")

pygame.init()


listfps=[100,150,250,400]
listcolumnwait=[150,100,80,50]
largeur_fen, hauteur_fen = 800, 600

SON_explosion=pygame.mixer.Sound("C:\\Users\\romai\\Desktop\\python\\sons\\explosion.wav")
SON_cash=pygame.mixer.Sound("C:\\Users\\romai\\Desktop\\python\\sons\\cash_register.wav")

screen = pygame.display.set_mode((largeur_fen, hauteur_fen))#,FULLSCREEN)
pygame.display.set_caption("Salvation bird")


def inter(list1,list2):
    def dicho_index(l1,l2,element):  
        m=(l1+(l2 or (len(list2)-1)))//2
        if list2[m]==element:
            return True
        elif len(list2[l1:l2])==1 or (list2[l1:l2]==[]):
            return False
        elif list2[m]>element:
            return dicho_index(l1,m,element)
        else:
            return dicho_index(m+1,l2,element)
        
    return [k for k in list1 if dicho_index(0,None,k)]

def colision(minAbs1,maxAbs1,minOrd1,maxOrd1,minAbs2,maxAbs2,minOrd2,maxOrd2):
    #print(minAbs1,maxAbs1,int(minOrd1),int(maxOrd1),minAbs2,maxAbs2,minOrd2,maxOrd2)
    return (1*(inter(list([k for k in range(minAbs1,maxAbs1)]),list([k for k in range(minAbs2,maxAbs2)])))) and (inter(list([k for k in range(int(minOrd1),int(maxOrd1))]),list([k for k in range(minOrd2,maxOrd2)])))

def borne(y):
    if y<0:
        return False
    elif y>560:
        return False
    else:
        return True

def pborne(x):
    if x<-25:
        return True
    else:
        return False
def creer_pilier(clrListe)  :
    
    ny=random.randint(100,350)
    clrListe.append((random.randint(0,255),random.randint(0,255),random.randint(0,255)))
    pilier1,pilier2=pygame.Rect(770,0,30,ny),pygame.Rect(770,ny+200,30,600-ny-200)
    return pilier1,pilier2

def move_pilier(nbr, clrListe, piliers):

    pygame.draw.rect(screen, clrListe[nbr], piliers[nbr][0])
    pygame.draw.rect(screen, clrListe[nbr], piliers[nbr][1])

def aff_tree(x):
    y,m=586,30
    pygame.draw.polygon(screen, (139,69,19), ((x, y), (x+2*m,y),(x+m*(3/2),y-m/2),(x+m*(3/2),y-m/2-2*m),(x+m/2,y-m/2-2*m),(x+m/2,y-m/2)  ))
    pygame.draw.polygon(screen, (0,255,0), ( (x+m*(3/2),y-m/2-2*m),(x+m/2,y-m/2-2*m),(x-m/2,y-3*m),(x+m/2,int(y-2.8*m)),(x+m/4,y-3.5*m),(x+m,y-3*m),(x+2*m,y-3.5*m),(x+1.5*m,int(y-2.8*m)),(x+2*m+m/2,y-3*m) ))
                                                   
def saut():
    return -5

def aff_bird(y,clr):  
    oiseau=pygame.Rect(200,y,60,40)
    pygame.draw.rect(screen,clr,oiseau)
    return y

def swipe():
    swiper=pygame.Rect(170,350,20,20)
    def go_to(coor,loop,add):
        for x in range(loop):
            pygame.draw.rect(screen,(255,0,0),swiper)
            pygame.display.update()
            if coor==0:
                swiper[0]+=add
            else:
                swiper[1]+=add
                
    go_to(0,640-170-20,1)
    go_to(1,460-320-20,1)
    go_to(0,640-170-20,-1)
    go_to(1,460-320-20,-1)

def breakeur(y):
    screen.fill((255,255,255))
    aff_bird(y,((255,0,0)))
    pygame.display.update()
    time.sleep(0.2)
    
    screen.fill((255,205,0))
    aff_bird(y,((255,0,255)))
    pygame.display.update()
    return 50,2000


def option():
    screen.fill((0,0,0))
    myfont = pygame.font.SysFont("monospace", 60,True)
    label = myfont.render("Options", 1, (255,255,255))
    screen.blit(label, (250, 50))
    
    clair=(150,150,150)
    fonce=(50,50,50)
    speed_choice=1
    column_choice=1
    clr=[(0,255,0),(0,0,255),(255,0,0),(255,0,255)]
    
    myfont2 = pygame.font.SysFont("monospace", 30,True)
    bouton1=pygame.Rect(40,150,200,50)
    bouton2=pygame.Rect(450,150,240,50)
    pygame.draw.rect(screen,clair,bouton1)
    label2 = myfont2.render("Speed", 1, (255,255,255))
    screen.blit(label2, (50, 155))
    sortie=pygame.Rect(230,500,285,60)
    pygame.draw.rect(screen,(100,100,100),sortie)
    myfont3=pygame.font.SysFont("monospace",40,True)
    label=myfont3.render("S T A R T !",1,(255,0,0),True)
    screen.blit(label, (250,510))
    
    pygame.draw.rect(screen,fonce,bouton2)
    label = myfont2.render("Column Spawn", 1, (255,255,255))
    screen.blit(label, (460, 155))
    inactif=1
    boutons=[bouton1,bouton2]
    pygame.display.update()
    
    def aff_option(inactif,pos):
        myfont2 = pygame.font.SysFont("monospace", 25,True)
        
        for x in range(4):
            option=myfont2.render(pos[inactif][x],1,clr[x])
            screen.blit(option, (250,220+x*75))
            pygame.display.update()

    def aff_titre(inactif):
        liste=[bouton1,bouton2,bouton1]
        pygame.draw.rect(screen,(0,0,0),pygame.Rect(200,200,400,400))
        pygame.draw.rect(screen,clair,liste[inactif])                        
        pygame.draw.rect(screen,fonce,liste[inactif+1])
        myfont2 = pygame.font.SysFont("monospace", 30,True)
        label2 = myfont2.render("Speed", 1, (255,255,255))
        label = myfont2.render("Column Spawn", 1, (255,255,255))
        screen.blit(label, (460, 155))
        screen.blit(label2, (50, 155))
        pygame.display.update()
        inactif=(1 * (inactif==0)) or 0
        return inactif
    continu=True
    while continu:

        for event in pygame.event.get():
            
            if (event.type == pygame.MOUSEBUTTONUP) and (event.button == 1):
                pos = pygame.mouse.get_pos()

                if boutons[inactif].collidepoint(pos):
                    inactif=aff_titre(inactif)

                elif sortie.collidepoint(pos):
                    continu=False
            if event.type == pygame.KEYDOWN:
                if event.key==pygame.K_RETURN:
                    inactif=aff_titre(inactif)
                    
                elif inactif==1:
                
                    if (event.key == pygame.K_UP) and ( speed_choice >0):
                        
                        pygame.draw.rect(screen,(0,0,0),pygame.Rect(220,speed_choice*75+230-5,20,20))
                        speed_choice-=1
                    elif (event.key == pygame.K_DOWN) and (speed_choice<3):
                        pygame.draw.rect(screen,(0,0,0),pygame.Rect(220,speed_choice*75+230-5,20,20))
                        speed_choice+=1
                else:
                    if (event.key == pygame.K_UP) and ( column_choice >0):
                        pygame.draw.rect(screen,(0,0,0),pygame.Rect(220,column_choice*75+230-5,20,20))
                        column_choice-=1
                    elif (event.key == pygame.K_DOWN) and (column_choice<3):
                        pygame.draw.rect(screen,(0,0,0),pygame.Rect(220,column_choice*75+230-5,20,20))
                        column_choice+=1
                    
        aff_option(inactif,[["Easy   : 150 tours","Medium : 100 tours","Hard   : 80 tours","Insane : 50  tours"],["Easy   : 100  fps","Medium : 150  fps","Hard   : 250 fps","Insane : 400 fps"]])
        #Exit
        sortie=pygame.Rect(230,500,285,60)
        pygame.draw.rect(screen,(20,20,20),sortie)
        myfont3=pygame.font.SysFont("monospace",40,True)
        if inactif==1:
            label=myfont3.render("S T A R T !",1,(clr[speed_choice]),True)
        else:
            label=myfont3.render("S T A R T !",1,(clr[column_choice]),True)
        screen.blit(label, (250,510))
        ##
        #Fleche
        if inactif==1:
            y=speed_choice*75+230
        else:
            y=column_choice*75+230
        taille=5
        debut=220
        pygame.draw.polygon(screen, (255, 255, 255), ((debut, y), (debut, y+taille), (debut+2*taille, y+taille), (debut+2*taille, y+2*taille), (debut+3*taille, y+taille/2), (debut+2*taille, y-taille), (debut+2*taille, y)))

    return speed_choice,column_choice

def chargement(a):
    if a == 1:
        myfont = pygame.font.SysFont("monospace", 60,True)
        label = myfont.render("Salvation Bird", 1, (255,255,0))
        screen.blit(label, (150, 100))
    pygame.draw.rect(screen,(100,100,100),pygame.Rect(200,380,410,80))
    for loop in range(8):
        load_bar=pygame.Rect(210+50*loop,390,40,60)
        pygame.draw.rect(screen,(255,255,255),load_bar)
        pygame.draw.rect(screen,(0,0,0),pygame.Rect(620,400,50,50))
        myfont3 = pygame.font.SysFont("monospace", 40)
        label3 = myfont3.render("{}%".format(random.randint(loop*10,loop*10+20)), 1, (255,255,255))
        screen.blit(label3, (620, 400))    
        time.sleep(0.2)
        pygame.display.update()
    pygame.draw.rect(screen,(0,0,0),pygame.Rect(620,400,100,100))    
    label3 = myfont3.render("100%", 1, (255,255,255))
    screen.blit(label3, (620, 400))        
    pygame.display.update()
    time.sleep(0.2)

    
def aff_accueil():
    screen.fill((0,0,0))

    myfont = pygame.font.SysFont("monospace", 60,True)
    label = myfont.render("Fire & Fury Corp.", 1, (255,255,0))
    screen.blit(label, (100, 100))
    myfont2 = pygame.font.SysFont("monospace", 20)
    label2 = myfont2.render("introducing:", 1, (255,255,0))
    screen.blit(label2, (325, 200))
    myfont3 = pygame.font.SysFont("monospace", 45)
    label3 = myfont3.render("Salvation Bird", 1, (255,255,0))
    screen.blit(label3, (200, 250))
    
    pygame.display.update()
    
    chargement(0)

    #swipe()
    notyet=True
    a=0
    while notyet:
        for ev in pygame.event.get():
            if (ev.type == pygame.KEYDOWN) or (ev.type == pygame.MOUSEBUTTONUP):
                notyet = False
        
        if a==0:
            myfont3 = pygame.font.SysFont("monospace", 40)
            label3 = myfont3.render("Press to start !", 1, (255,255,255))
            screen.blit(label3, (200, 500))
            b=1.5
        elif a==9:
            pygame.draw.rect(screen,(0,0,0),pygame.Rect(200,500,400,100))
            b=-1
        a+=b
        pygame.display.update()
        pygame.time.Clock().tick(10)
    speed_choice,column_choice=option()
    screen.fill((0,0,0))
    myfont = pygame.font.SysFont("monospace", 60,True)
    label = myfont.render("Loading...", 1, (255,255,255))
    screen.blit(label, (240, 260))
    chargement(1)
    return speed_choice,column_choice
#aff_tree(100)
#time.sleep(5)

def menu():
    screen.fill((0,0,0))
    start_bouton = pygame.Rect(250,240,260,130)
    option_bouton = pygame.Rect(270,390,220,60)
    exit_bouton = pygame.Rect(300, 520, 150, 70)
    pygame.draw.rect(screen,(60, 60, 60), exit_bouton)
    pygame.draw.rect(screen,(60, 60, 60), start_bouton)
    pygame.draw.rect(screen,(60, 60, 60), option_bouton)


    myfont = pygame.font.SysFont("monospace", 60,True)
    label = myfont.render("Salvation Bird", 1, (255,255,0))
    screen.blit(label, (150, 100))
    myfont2 = pygame.font.SysFont("monospace", 40)
    label2 = myfont2.render("Options", 1, (255, 255, 255))
    screen.blit(label2, (300, 400))
    myfont3 = pygame.font.SysFont("monospace", 50, True)
    label3 = myfont3.render("Play !", 1, (255, 255, 255))
    screen.blit(label3, (300, 250))
    myfont3 = pygame.font.SysFont("monospace", 20)
    label3 = myfont3.render("[difficulte insane]", 1, (255, 255, 255))
    screen.blit(label3, (260, 330))
    myfont3 = pygame.font.SysFont("monospace", 50, True)
    label3 = myfont3.render("EXIT", 1, (255, 0, 0))
    screen.blit(label3, (315, 530))

    pygame.display.update()
    
    while True:
        for event in pygame.event.get():
            if (event.type == pygame.MOUSEBUTTONUP) and (event.button == 1):
                pos = pygame.mouse.get_pos()

                if start_bouton.collidepoint(pos):
                    return 2

                elif option_bouton.collidepoint(pos):
                    return 1
                elif exit_bouton.collidepoint(pos):
                    return 0
def aff_titre():
    myfont = pygame.font.SysFont("monospace", 60,True)
    label = myfont.render("Salvation Bird", 1, (255,255,0))
    screen.blit(label, (150, 100))
def partie(fps,columnwait):
    #variables
    jeu=True
    a=0
    x,y=200,400
    pwait=100
    br=-90
    brwait=0
    cy,cx=0,0
    piliers=[]
    clrListe=[]
    point=0
    trees=[]
    twait=150
    ##
    while jeu:
        screen.fill((0,50,255))
        terre,herbe=pygame.Rect(0,590,800,10),pygame.Rect(0,586,800,4)
        pygame.draw.rect(screen,(150,45,10),terre)
        pygame.draw.rect(screen,(0,240,0),herbe)

        if twait+ 50 > random.randint(90,300):
            trees.append([800])
            twait = 0
        #print(trees,pwait+50>150,pwait,treelimite)
        for rang in range(len(trees)):
            if x > -20:
                aff_tree(trees[rang][0])
                trees[rang][0]-=1
            
        
        del_liste=[]
        for event in pygame.event.get():
            if event.type == QUIT:
                jeu=False
            if event.type == pygame.KEYDOWN:
                if (event.key == pygame.K_RETURN) and (brwait < 0):
                    br,brwait=breakeur(y)
                else:
                    cy=saut()
        jeu=borne(y)
        
        cy+=0.1
        pwait+=0.2
        twait+=0.3
        if pwait>columnwait:
            pilier1,pilier2=creer_pilier(clrListe)
            piliers.append([pilier1,pilier2])
            pwait=0
            
        y=aff_bird(y+cy,(0,255,0))
        br-=1
        brwait-=1
        if br>0:        
            screen.fill((255,205,0))
            aff_bird(x,((255,0,255)))
            
        for rang in range(len(piliers)):
            if not piliers[rang]==0:
                move_pilier(rang,clrListe,piliers)
                piliers[rang][0][0],piliers[rang][1][0]=piliers[rang][0][0]-1,piliers[rang][1][0]-1
                if (colision(200,200+60,y,y+40,piliers[rang][0][0],piliers[rang][0][0]+piliers[rang][0][2],piliers[rang][0][1],piliers[rang][0][1]+piliers[rang][0][3]) or colision(200,200+60,y,y+40,piliers[rang][1][0],piliers[rang][1][0]+piliers[rang][1][2],piliers[rang][1][1],piliers[rang][1][1]+piliers[rang][1][3])) and (br<-90):
                    jeu=False
                if piliers[rang][0][0]==200:
                    SON_cash.play()
                    point+=1
                if pborne(piliers[rang][0][0]):
                    piliers[rang]=0
                #print(piliers[rang][0][0],piliers,rang)
                

        if brwait<0:
            pygame.draw.rect(screen,(255,0,0),pygame.Rect(50,50,30,30))
        
        myfont3 = pygame.font.SysFont("monospace", 20)
        label3 = myfont3.render("Points: {}".format(point), 1, (0,0,0))
        screen.blit(label3, (50, 20))
        
        pygame.display.update()
        if a == 0:
            while a == 0:
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_SPACE:
                            a=1
                            cy=saut()
        pygame.time.Clock().tick(fps)
    return point

def loose(point,difficulte):
    screen.fill((0,0,0))
    font=pygame.font.SysFont("monospace",100,True)
    label=font.render("YOU LOOSE !",1,(255,0,0))
    screen.blit(label, (110,280))
    pygame.display.update()
    SON_explosion.play()
    time.sleep(2)
    print("Vous avez passé {} piliers avant de mourrir !".format(point))   
    print("death right now !".upper())
    base.write("Difficulte : {} ; Score : {}\n".format(difficulte,point))

    
def end():
    base.close()
    pygame.quit()


def main():
    base.write("#"+time.asctime( time.localtime(time.time()) )+"#\n")
    partie_cours = menu()
    while partie_cours:
        if partie_cours == 1:
            fps,columnwait = aff_accueil()
        else:
            fps,columnwait = 3, 3
            screen.fill((0, 0, 0))
            chargement(1)
        difficulte = fps+columnwait
        print("Difficulte de niveau {} activee !".format(difficulte))
        fps,columnwait=listfps[fps],listcolumnwait[columnwait]
        point = partie(fps,columnwait)
        loose(point,difficulte)
        partie_cours = menu()
    end()

main()
