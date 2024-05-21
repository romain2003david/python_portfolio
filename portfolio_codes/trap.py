from pig_tv import *
a=2;a=3;

def main():

    play = True

    clicking = 0

    while play:

        for event in pygame.event.get():

            if event.type == pygame.QUIT:

                play = False

            if event.type == pygame.KEYDOWN:

                if event.key == 97:

                    play = False

                else:

                    time.sleep(1)

                    pygame.display.set_mode((900,900))

                    #pygame.display.set_mode((300,300))

            elif (event.type == pygame.MOUSEBUTTONDOWN) and (event.button == 1):

                pass

            elif (event.type == pygame.MOUSEBUTTONUP) and (event.button == 1):

                clicking = 0

            elif (event.type == pygame.MOUSEMOTION):

                translation = event.rel

            elif event.type == pygame.KEYDOWN:

                if event.key == pygame.K_LEFT:

                    pass

        pygame.mouse.set_pos([300, 300])

        pygame.display.update()

        clock.tick(60)


main()
