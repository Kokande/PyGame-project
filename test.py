import pygame


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
        self.func = lambda: None
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

    def set_act(self, func):
        self.func = func

    def init_click(self):
        if not self.calm:
            self.func()

    def is_overlapping(self, coords):
        if self.coords[0] <= coords[0] <= self.coords[0] + self.width and \
           self.coords[1] <= coords[1] <= self.coords[1] + self.height:
            return True
        return False


class Game:
    def __init__(self, display):
        self.on = True
        self.screen = 0
        self.display = display
        self.objects = dict()

    def kill_the_game(self):
        self.on = False

    def render(self):
        if self.screen == 0:
            self.render_menu()
        elif self.screen == 1:
            self.render_game()

    def render_menu(self):
        self.display.blit(pygame.font.Font(None, 150).render("Project Name", 80,
                                                             (100, 0, 0)), (50, 50))
        for i in self.objects:
            for k in self.objects[i]:
                k.render()

    def change_screen(self, scr):
        self.screen = scr
        if self.screen == 0:
            self.set_menu()
        elif self.screen == 1:
            self.set_game()

    def render_game(self):
        pass

    def key_pressed(self, key):
        if self.screen == 0:
            self.key_pressed_menu(key)
        elif self.screen == 1:
            self.key_pressed_ingame(key)

    def mouse_pressed(self, mouse):
        if self.screen == 0:
            self.mouse_pressed_menu(mouse)
        elif self.screen == 1:
            self.mouse_pressed_ingame(mouse)

    def get_screen_obj_info(self):
        pass

    def key_pressed_menu(self, key):
        if key.key == pygame.K_KP_ENTER:
            self.change_screen(1)

    def key_pressed_ingame(self, key):
        pass

    def mouse_pressed_menu(self, mouse):
        pass

    def mouse_pressed_ingame(self, mouse):
        pass

    def mouse_moved(self, movement):
        if self.screen == 0:
            pass

    def set_menu(self):
        self.objects.clear()
        self.objects['buttons'] = [Button(self.display, (50, 200), (400, 100),
                                          text="Start", alt=(50, 50, 50))]
        self.objects['buttons'][0].set_act(self.change_screen(1))

    def set_game(self):
        pass


if __name__ == '__main__':
    SIZE = (1000, 800)
    pygame.init()
    pygame.font.init()
    screen = pygame.display.set_mode(SIZE)
    game = Game(screen)
    game.set_menu()
    while game.on:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F4 and event.mod == pygame.KMOD_LALT:
                    game.kill_the_game()
                else:
                    game.key_pressed(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                game.mouse_pressed(event)
            elif event.type == pygame.MOUSEMOTION:
                game.mouse_moved(event)
            elif event.type == pygame.QUIT:
                game.kill_the_game()
        screen.fill((0, 0, 0))
        game.render()
        pygame.time.Clock().tick(60)
        pygame.display.flip()
