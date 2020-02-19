import pygame
"""
Класс кнопки
"""


class Button:
    def __init__(self, scr, xy, wh, text="", font=(None, 100), fc=(255, 255, 255),
                 border=(255, 255, 255), color=(0, 0, 0), alt=(255, 255, 255), bw=5):
        self.coords = xy
        self.width = wh[0]
        self.height = wh[1]
        self.color = color
        self.border = border
        self.border_weight = bw
        self.alt = alt
        self.screen = scr
        self.func = (lambda: None, '')
        self.text = pygame.font.Font(font[0], font[1]).render(text, 80, fc)
        self.border_color = border
        self.calm = True

    def render(self):
        if self.calm:
            pygame.draw.rect(self.screen, self.color,
                             (self.coords[0], self.coords[1], self.width, self.height))
        else:
            pygame.draw.rect(self.screen, self.alt,
                             (self.coords[0], self.coords[1], self.width, self.height))
        self.screen.blit(self.text, (self.coords[0] +
                                     (self.width / 2 - self.text.get_width()/2),
                                     self.coords[1] +
                                     (self.height/2 - self.text.get_height() / 2)))
        pygame.draw.rect(self.screen, self.border,
                         (self.coords[0], self.coords[1], self.width, self.height),
                         self.border_weight)

    def mouse_down_track(self, mouse):
        if self.is_overlapping(mouse.pos):
            self.calm = False

    def set_act(self, func, value=None):
        self.func = (func, value)

    def init_click(self):
        if not self.calm:
            self.func[0](self.func[1])

    def is_overlapping(self, coords):
        if self.coords[0] <= coords[0] <= self.coords[0] + self.width and \
           self.coords[1] <= coords[1] <= self.coords[1] + self.height:
            return True
        return False


class Game:
    def __init__(self, display):
        self.on = True
        self.display = display
        self.mouse_down = False
        self.screen = self.Menu(self)
    """
    Класс самой игры
    """
    class Game:
        def __init__(self, parent):
            self.parent = parent

        def render(self):
            pass

        def mouse_pressed(self, mouse):
            pass

        def key_pressed(self, key):
            pass

        def mouse_moved(self, movement):
            pass
    """
    Класс меню игры
    """
    class Menu:
        def __init__(self, parent):
            self.parent = parent
            self.objects = {'buttons': [Button(self.parent.display, (50, 200), (400, 100),
                                               text="Start", alt=(50, 50, 50))]}
            self.objects['buttons'][0].set_act(self.parent.change_screen, value=1)

        def render(self):
            self.parent.display.blit(pygame.font.Font(None, 150).render("Project Name", 80,
                                                                        (100, 0, 0)), (50, 50))
            for i in self.objects:
                for k in self.objects[i]:
                    k.render()

        def mouse_pressed(self, mouse):
            pass

        def key_pressed(self, key):
            if key.key == pygame.K_KP_ENTER:
                self.parent.change_screen(self.parent.Game(self.parent))

        def mouse_moved(self, movement):
            pass

    def kill_the_game(self):
        self.on = False

    def render(self):
        self.screen.render()

    def change_screen(self, scr):
        self.screen = scr

    def key_pressed(self, key):
        self.screen.key_pressed(key)

    def mouse_pressed(self, mouse, up=False):
        if not up:
            self.mouse_down = True
        self.screen.mouse_pressed(mouse)

    def get_screen_obj_info(self):
        pass

    def mouse_moved(self, movement):
        self.screen.mouse_moved(movement)


if __name__ == '__main__':
    SIZE = (1000, 800)
    pygame.init()
    pygame.font.init()
    screen = pygame.display.set_mode(SIZE)
    game = Game(screen)
    while game.on:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F4 and event.mod == pygame.KMOD_LALT:
                    game.kill_the_game()
                else:
                    game.key_pressed(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                game.mouse_pressed(event)
            elif event.type == pygame.MOUSEBUTTONUP:
                game.mouse_pressed(event, up=True)
            elif event.type == pygame.MOUSEMOTION:
                game.mouse_moved(event)
            elif event.type == pygame.QUIT:
                game.kill_the_game()
        screen.fill((0, 0, 0))
        game.render()
        pygame.time.Clock().tick(60)
        pygame.display.flip()
