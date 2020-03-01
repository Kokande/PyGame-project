import pygame
import random
import pprint
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
        self.func = (lambda x: None, 'not None')
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
        else:
            self.calm = True

    def set_act(self, func, value=None):
        self.func = (func, value)

    def mouse_released(self, mouse):
        if self.is_overlapping(mouse.pos):
            if self.func[1] is None:
                self.func[0]()
            else:
                self.func[0](self.func[1])
            self.calm = True
        else:
            self.calm = True

    def is_overlapping(self, coords):
        if self.coords[0] <= coords[0] <= self.coords[0] + self.width and \
           self.coords[1] <= coords[1] <= self.coords[1] + self.height:
            return True
        return False


"""
Сама игра
"""


class Game:
    def __init__(self, display):
        self.on = True
        self.display = display
        self.mouse_down = False
        self.screen = self.Menu(self)
        self.game = None
    """
    Класс самой игры
    """
    class Game:
        def __init__(self, parent):
            self.parent = parent
            self.map_size = 3
            self.current_lvl = 1
            self.map_draft = {0: [['.' for i in range(10)] for i in range(10)]}
            self.map = [[0 for k in range(self.map_size)] for i in range(self.map_size)]
            self.player_pos = (-1, -1)
            self.standing_on = '0'
            self.indoor = True
            self.map_generator()

        def render(self):
            step = 40
            visible = [[self.map[i][k]
                        if 0 <= k < self.map_size * 10
                        else '*'
                        for k in range(self.player_pos[0] - (SIZE[0] // step - 1) // 2,
                                       self.player_pos[0] + (SIZE[0] // step - 1) // 2 + 1)]
                       if 0 <= i < self.map_size * 10
                       else list('*' * (SIZE[0] // step))
                       for i in range(self.player_pos[1] - (SIZE[1] // step) // 2 + 1,
                                      self.player_pos[1] + (SIZE[1] // step) // 2 + 2)]
            for x in range(1, SIZE[0] + 1, step):
                for y in range(1, SIZE[1] + 1, step):
                    tile = visible[y // step][x // step]
                    if tile == '0':
                        pygame.draw.rect(self.parent.display, pygame.Color('brown'),
                                         (x, y, step, step), 2)
                    elif tile == '*':
                        pygame.draw.rect(self.parent.display, pygame.Color('brown'),
                                         (x, y, step, step))
                    elif tile == 'P':
                        pygame.draw.rect(self.parent.display, (200, 0, 100),
                                         (x, y, step, step))
                    elif tile == '1':
                        pygame.draw.rect(self.parent.display, (50, 0, 0),
                                         (x, y, step, step))
                        pygame.draw.rect(self.parent.display, pygame.Color('brown'),
                                         (x + 5,
                                          y + (step - 10) // 2, 10, 10))
                    elif tile == 'b':
                        pygame.draw.circle(self.parent.display, pygame.Color('brown'),
                                           (x + step // 2, y + step // 2), step // 2)
                    elif tile == 'c':
                        pygame.draw.rect(self.parent.display, (100, 50, 0),
                                         (x, y, step, step))
                    elif tile == 'E':
                        pygame.draw.rect(self.parent.display, pygame.Color('green'),
                                         (x, y, step, step))
                    elif tile == 'C':
                        pygame.draw.rect(self.parent.display, pygame.Color('yellow'),
                                         (x, y, step, step))

        def mouse_pressed(self, mouse):
            pass

        def key_pressed(self, key):
            if key.key == pygame.K_ESCAPE:
                self.parent.change_screen(self.parent.Menu(self.parent))
            elif key.key == pygame.K_UP:
                self.move_player('UP')
            elif key.key == pygame.K_DOWN:
                self.move_player('DOWN')
            elif key.key == pygame.K_LEFT:
                self.move_player('LEFT')
            elif key.key == pygame.K_RIGHT:
                self.move_player('RIGHT')

        def mouse_moved(self, movement):
            pass

        def move_player(self, direction):
            self.map[self.player_pos[1]][self.player_pos[0]] = self.standing_on
            if direction == 'UP':
                new_coords = (self.player_pos[0], self.player_pos[1] - 1)
                if self.move_possible(new_coords):
                    self.player_pos = new_coords
            elif direction == 'DOWN':
                new_coords = (self.player_pos[0], self.player_pos[1] + 1)
                if self.move_possible(new_coords):
                    self.player_pos = new_coords
            elif direction == 'LEFT':
                new_coords = (self.player_pos[0] - 1, self.player_pos[1])
                if self.move_possible(new_coords):
                    self.player_pos = new_coords
            elif direction == 'RIGHT':
                new_coords = (self.player_pos[0] + 1, self.player_pos[1])
                if self.move_possible(new_coords):
                    self.player_pos = new_coords
            self.standing_on = self.map[self.player_pos[1]][self.player_pos[0]]
            self.map[self.player_pos[1]][self.player_pos[0]] = 'P'

        def move_possible(self, new_coords):
            if 0 <= new_coords[0] < 10 * self.map_size and \
               0 <= new_coords[1] < 10 * self.map_size and \
               self.map[new_coords[1]][new_coords[0]] in ['0', '1', '.'] and \
               (self.map[new_coords[1]][new_coords[0]] == '1' or
               self.standing_on == self.map[new_coords[1]][new_coords[0]] or
               self.standing_on == '1'):
                return True
            return False

        def map_generator(self):
            with open("draft.dat", 'rt') as draft:
                for i in range(1, BLOCKS + 1):
                    draft.readline()
                    self.map_draft[i] = []
                    for k in range(10):
                        self.map_draft[i].append(list(draft.readline().rstrip()))
            generator = dict()
            coord_seq = random.sample(range(1, self.map_size ** 2 + 1), BLOCKS)
            seq = random.sample(range(1, len(self.map_draft)), BLOCKS)

            for i in range(BLOCKS):
                generator[coord_seq[i]] = seq[i]
            for i in range(self.map_size):
                for k in range(self.map_size):
                    if i * self.map_size + k + 1 in coord_seq:
                        self.map[i][k] = generator[i * self.map_size + k + 1]
            self.map_constructor()

        def map_constructor(self):
            map_rows = [[] for i in range(10 * self.map_size)]
            for i in range(self.map_size):
                for k in range(self.map_size):
                    for j in range(10):
                        map_rows[i * 10 + j].extend(self.map_draft[self.map[i][k]][j])
                        if self.map[i][k] == 1 and j == 4:
                            self.player_pos = (k * 10 + 4, i * 10 + j)
            self.map = map_rows
    """
    Класс меню игры
    """
    class Menu:
        def __init__(self, parent):
            self.parent = parent
            self.objects = {'buttons': [Button(self.parent.display, (50, 200), (400, 100),
                                               text="Start", alt=(100, 0, 0)),
                                        Button(self.parent.display, (50, 350), (325, 100),
                                               text="Load", alt=(100, 0, 0), bw=2),
                                        Button(self.parent.display, (50, 500), (325, 100),
                                               text="Save", alt=(100, 0, 0), bw=2),
                                        Button(self.parent.display, (50, 650), (250, 100),
                                               text="Quit", alt=(100, 0, 0), bw=2)]}
            self.objects['buttons'][0].set_act(self.parent.change_screen,
                                               value=self.parent.Game(self.parent))
            self.objects['buttons'][3].set_act(self.parent.kill_the_game)

        def render(self):
            self.parent.display.blit(pygame.font.Font(None,
                                                      150).render("Project Name", 80,
                                                                  (100, 0, 0)), (50, 50))
            for i in self.objects:
                for k in self.objects[i]:
                    k.render()

        def mouse_pressed(self, mouse):
            for i in self.objects:
                for k in self.objects[i]:
                    k.mouse_released(mouse)

        def key_pressed(self, key):
            if key.key == pygame.K_KP_ENTER:
                self.parent.change_screen(self.parent.Game(self.parent))
            elif key.key == pygame.K_ESCAPE:
                self.parent.kill_the_game()

        def mouse_moved(self, mouse):
            for i in self.objects:
                for k in self.objects[i]:
                    k.mouse_down_track(mouse)

    """
    Методы класса Game
    """

    def kill_the_game(self):
        self.on = False

    def render(self):
        self.screen.render()

    def change_screen(self, scr):
        if type(self.screen) == Game.Game:
            self.save_game_state()
        self.screen = scr

    def key_pressed(self, key):
        self.screen.key_pressed(key)

    def mouse_pressed(self, mouse, up=False):
        if not up:
            self.mouse_down = True
            self.mouse_moved(mouse)
        else:
            self.mouse_down = False
            self.screen.mouse_pressed(mouse)

    def get_screen_obj_info(self):
        pass

    def mouse_moved(self, mouse):
        self.screen.mouse_moved(mouse)

    def save_game_state(self):
        self.game = self.screen


SIZE = (1000, 800)
BLOCKS = 6
if __name__ == '__main__':
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
