from pig_tv import *


class Agent:

    dico_color = {"altruiste":GREEN, "profiteur":RED, "basique":BLUE}

    dico_type_agent = {"altruiste":1, "profiteur":2, "basique":0}

    def __init__(self, pos=None, type_agent=None, radius=None, energy=None):

        if pos != None:

            self.pos = pos

        else:

            self.pos = Arr(get_random_point_in_screen())

        self.x = self.pos[0]

        self.y = self.pos[1]

        self.vector = Arr([10, 0])  # Arr.get_nul([2])

        # type_agent
        if type_agent != None:

            self.type_agent = type_agent

        else:

            self.type_agent = "basique"

        self.type_agent_int = Agent.dico_type_agent[self.type_agent]
        ##

        # radius
        if radius != None:

            self.radius = radius

        else:

            self.radius = 10
        ##

        self.color = Agent.dico_color[self.type_agent]

        #energy
        if energy != None:

            self.energy = energy

        else:

            self.energy = 1
        ##

        self.age = 0

        self.is_eating = False

        self.on_spot = False

    def get_energy(self):

        return self.energy

    def get_vector(self):

        return self.vector

    def get_y(self):

        return self.y

    def get_x(self):

        return self.x

    def update(self, draw=True):

        self.age += 1

        if self.energy > 0:

            Agent.update_vect(self)

            Agent.move(self)

            if draw:

                Agent.draw(self)

        else:

            return -1  # dead
        

    def draw(self):

        pygame.draw.circle(screen, self.color, self.pos, self.radius)

    def move(self):

        self.pos += self.vector

    def update_vect(self) :

      vect = self.get_vector()
      module = sqrt((vect[0]**2 + vect[1])**2)
      if (self.get_y() == 0) :
        b = randint(0,4)
        for i in range(5):
          j=i+1
          if (b == i) :
            vect2 =Arr(cos(pi*j*0.2),sin(pi*j*0.2))
            vect2 = vect2 * module
      elif(self.get_y() == screen_height) :
        for i in range(5):
          if (b == i) :
            vect2 =Arr(cos(pi*j*1/6),-sin(pi*j*1/6))
            vect2 = vect2 * module
      elif(self.get_x() == 0) :
        for i in range(5):
          if (b == i) :
            vect2 =Arr(sin(pi*j*1/6),-cos(pi*j*1/6))
            vect2 = vect2 * module
      elif(self.get_x() == screen_width):
         for i in range(5):
          if (b == i) :
            vect2 =Arr(-sin(pi*j*1/6),-cos(pi*j*1/6))
            vect2 = vect2 * module
      else:
        vect2 = vect

      self.vector = vect2


class Button:

    back_color = WHITE

    deco_color = BLACK

    selected_color = RED

    def __init__(self, x, y, string, default_val=None):

        self.x = x

        self.y = y

        self.width = 200

        self.height = 75

        self.string = string

        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

        self.deco_decal = 5

        self.txt_decal_x = 2*self.deco_decal

        self.txt_decal_y = 5

        self.rect_deco = pygame.Rect(self.x+self.deco_decal, self.y+self.deco_decal, self.width-2*self.deco_decal, self.height-2*self.deco_decal)

        self.state_clicked = False

        self.val = default_val

    def draw(self):

        pygame.draw.rect(screen, Button.back_color, self.rect)

        if not self.state_clicked:

            pygame.draw.rect(screen, Button.deco_color, self.rect_deco, 3)

        else:

            pygame.draw.rect(screen, Button.selected_color, self.rect_deco, 3)

        aff_txt(self.string, self.x+self.txt_decal_x, self.y+self.txt_decal_y, taille=20)

        aff_txt(self.val, self.x+self.txt_decal_x, self.y+30+self.txt_decal_y)

    def clicked(self, mouse_pos):

        clicked = collide_point_to_rect(mouse_pos, self.rect)

        return collide_point_to_rect(mouse_pos, self.rect)

    def set_clicked(self, val):

        self.state_clicked = val

    def update_val(self, user_input):

        n_val = self.val

        if user_input != None:

            n_val += user_input

        Button.modify_val(self, n_val)

    def modify_val(self, n_val):

        self.val = n_val



class Univers:

    button_height = 100

    def __init__(self):

        self.agents = []

        # graphic interface

        # buttons

        self.buttons = []

        self.clicked_button = None

    def add_agent(self, agent):

        self.agents.append(agent)

    def add_button(self, string):

        button = Button(0, Univers.button_height*len(self.buttons), string, "0")

        self.buttons.append(button)

    def update_buttons(self, draw, mouse_clicked):

        user_input = None

        mouse_pos = pygame.mouse.get_pos()

        button_got_clicked = False

        for button in self.buttons:

            # drawing if necessary

            if draw:

                button.draw()

            # updating clicked button

            if mouse_clicked:

                if button.clicked(mouse_pos):

                    button_got_clicked = True

                    if not self.clicked_button == button:

                        self.clicked_button = button

                        button.set_clicked(True)

                # updating value of clicked button

                if button.state_clicked:

                    button.update_val(user_input)

        if mouse_clicked and (self.clicked_button != None) and (not button_got_clicked):

            self.clicked_button.set_clicked(False)

            self.clicked_button = None


    def update(self, draw, mouse_clicked):

        Univers.update_buttons(self, draw, mouse_clicked)

        # agent update

        for agent in self.agents:

            agent.update(draw)




def main():

    univers = Univers()

    univers.add_agent(Agent())

    univers.add_button("proba mutation")

    temps = 0

    draw = True

    run = True

    while run:

        temps += 1

        clicked = False

        # user events

        for event in pygame.event.get():

            if event.type == pygame.QUIT:

                play = False

            elif (event.type == pygame.MOUSEBUTTONDOWN) and (event.button == 1):

                clicked = True

        # drawing and updating universe
        if draw:

            screen.fill(GREY)

        univers.update(draw, clicked)

        if draw:

            pygame.display.update()

            clock.tick(60)

    return


if __name__ == "__main__":

    main()
















