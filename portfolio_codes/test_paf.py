from pig_tv import *

def p_loop():

    play = True

    clicking = 0

    while play:

        for event in pygame.event.get():

            if event.type == pygame.KEYDOWN:

                string = event.unicode

                if string != "":

                    user_input = string
                    

        pygame.display.update()

        clock.tick(60)


p_loop()
