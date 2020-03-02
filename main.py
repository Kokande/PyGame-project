import pygame
import random
"""
Класс Сущности
"""


class Entity:
    def __init__(self, pos, parent, standing_on='0', type_name=None):
        self.pos = pos
        self.parent = parent
        self.type_name = type_name
        self.pause = 0
        self.standing_on = standing_on
        self.visibles = dict()

    def move_logic(self):
        if self.type_name == 'Enemy':
            visible = self.get_vision()
            self.get_visible_objects(visible)
            if self.visibles['player'] is None or\
                    ((self.standing_on == '.' or self.standing_on == '0') and
                     self.standing_on != self.parent.standing_on):
                return random.sample(['UP', 'DOWN', 'LEFT', 'RIGHT'], 4)
            else:
                """
                Простой алгоритм преследования игрока:)
                """
                if self.visibles['player'][0] < 0 and self.visibles['player'][1] > 0:
                    return ['DOWN', 'LEFT', 'RIGHT', 'UP']
                elif self.visibles['player'][0] > 0 and self.visibles['player'][1] < 0:
                    return ['UP', 'RIGHT', 'LEFT', 'DOWN']
                elif self.visibles['player'][0] > 0 and self.visibles['player'][1] > 0:
                    return ['DOWN', 'RIGHT', 'LEFT', 'UP']
                elif self.visibles['player'][0] < 0 and self.visibles['player'][1] < 0:
                    return ['UP', 'LEFT', 'RIGHT', 'DOWN']
                elif self.visibles['player'][0] == 0 and self.visibles['player'][1] > 0:
                    return ['DOWN', 'LEFT', 'RIGHT', 'UP']
                elif self.visibles['player'][0] == 0 and self.visibles['player'][1] < 0:
                    return ['UP', 'LEFT', 'RIGHT', 'DOWN']
                elif self.visibles['player'][0] < 0 and self.visibles['player'][1] == 0:
                    return ['LEFT', 'UP', 'DOWN', 'RIGHT']
                elif self.visibles['player'][0] > 0 and self.visibles['player'][1] == 0:
                    return ['RIGHT', 'UP', 'DOWN', 'LEFT']

    def move(self):
        change = self.parent.game_map
        decision = self.move_logic()
        moved = False
        new_coords = self.pos
        directions = {'UP': (self.pos[0], self.pos[1] - 1),
                      'DOWN': (self.pos[0], self.pos[1] + 1),
                      'LEFT': (self.pos[0] - 1, self.pos[1]),
                      'RIGHT': (self.pos[0] + 1, self.pos[1])}
        if decision is not None:
            for i in decision:
                new_coords = directions[i]
                if self.move_possible(new_coords):
                    change[self.pos[1]][self.pos[0]] = self.standing_on
                    self.pos = new_coords
                    moved = True
                    break
        if moved:
            self.standing_on = change[self.pos[1]][self.pos[0]]
            change[self.pos[1]][self.pos[0]] = 'B' if self.type_name == 'Goal' else 'E'
        return change

    def move_possible(self, new_coords):
        if 0 <= new_coords[0] < 10 * self.parent.map_size and \
                0 <= new_coords[1] < 10 * self.parent.map_size and \
                self.parent.game_map[new_coords[1]][new_coords[0]] in ['0', '1', '.'] and \
                (self.parent.game_map[new_coords[1]][new_coords[0]] == '1' or
                 self.standing_on == self.parent.game_map[new_coords[1]][new_coords[0]] or
                 self.standing_on == '1'):
            return True
        return False

    def get_vision(self):
        radius = 6
        return [[self.parent.game_map[i][k] if 0 <= k < self.parent.map_size * 10 else '*'
                for k in range(self.pos[0] - radius, self.pos[0] + radius + 1)]
                if 0 <= i < self.parent.map_size * 10 else list('*' * radius * 2 + '*')
                for i in range(self.pos[1] - radius, self.pos[1] + radius + 1)]

    def get_visible_objects(self, vision):
        self.visibles = {'player': None, 'goals': []}
        for i in range(13):
            for k in range(13):
                if vision[k][i] not in ['.', '0', '1', '*']:
                    if vision[k][i] == 'P':
                        self.visibles['player'] = (i - 6, k - 6)

    def on_iter(self):
        if self.pause == 0:
            self.pause = 5
            return self.move()
        else:
            self.pause -= 1
            return self.parent.game_map

    def interaction(self):
        pass


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
Класс приложения игры
"""


class Game:
    def __init__(self, display):
        self.on = True
        self.display = display
        self.mouse_down = False
        self.game = self.Game(self)
        self.screen = self.Menu(self, starting=True)
    """
    Класс самой игры
    """
    class Game:
        def __init__(self, parent, map_size=3, current_lvl=1,
                     player_pos=(-1, -1), standing_on='0', game_map=None,
                     new=True, entities=None, chest=(0, 0)):
            self.entities = {'enemies': []}
            self.parent = parent
            self.map_size = map_size
            self.current_lvl = current_lvl
            self.chest = chest
            self.map_draft = {0: [['.' for i in range(10)] for i in range(10)]}
            if game_map is None:
                self.game_map = [[0 for k in range(self.map_size)]
                                 for i in range(self.map_size)]
            else:
                self.game_map = game_map
            self.player_pos = player_pos
            self.standing_on = standing_on
            self.extract_draftables()
            if new:
                self.map_generator()
            if entities is None:
                self.find_objects()
            else:
                self.entities['enemies'].extend(entities)

        def render(self):
            self.entities_move()
            step = 40
            visible = [[self.game_map[i][k]
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
                    elif tile == 'B':
                        pygame.draw.rect(self.parent.display, pygame.Color('cyan'),
                                         (x, y, step, step), 4)

        def entities_move(self):
            for i in self.entities:
                for k in self.entities[i]:
                    self.game_map = k.on_iter()

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
            self.game_map[self.player_pos[1]][self.player_pos[0]] = self.standing_on
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
            self.standing_on = self.game_map[self.player_pos[1]][self.player_pos[0]]
            self.game_map[self.player_pos[1]][self.player_pos[0]] = 'P'

        def move_possible(self, new_coords):
            if 0 <= new_coords[0] < 10 * self.map_size and \
               0 <= new_coords[1] < 10 * self.map_size and \
               self.game_map[new_coords[1]][new_coords[0]] in ['0', '1', '.'] and \
               (self.game_map[new_coords[1]][new_coords[0]] == '1' or
                self.standing_on == self.game_map[new_coords[1]][new_coords[0]] or
               self.standing_on == '1'):
                return True
            elif new_coords == self.chest:
                self.victory()
            return False

        def extract_draftables(self):
            with open("draft.dat", 'rt') as draft:
                for i in range(1, BLOCKS + 1):
                    draft.readline()
                    self.map_draft[i] = []
                    for k in range(10):
                        self.map_draft[i].append(list(draft.readline().rstrip()))

        def map_generator(self):
            generator = dict()
            coord_seq = random.sample(range(1, self.map_size ** 2 + 1), BLOCKS)
            seq = random.sample(range(1, len(self.map_draft)), BLOCKS)
            for i in range(BLOCKS):
                generator[coord_seq[i]] = seq[i]
            for i in range(self.map_size):
                for k in range(self.map_size):
                    if i * self.map_size + k + 1 in coord_seq:
                        self.game_map[i][k] = generator[i * self.map_size + k + 1]
            self.game_constructor()

        def game_constructor(self):
            map_rows = [[] for i in range(10 * self.map_size)]
            for i in range(self.map_size):
                for k in range(self.map_size):
                    for j in range(10):
                        map_rows[i * 10 + j].extend(self.map_draft[self.game_map[i][k]][j])
                        if self.game_map[i][k] == 1 and j == 4:
                            self.player_pos = (k * 10 + 4, i * 10 + j)
            self.game_map = map_rows
            broke = False
            en = 10
            for i in random.sample(range(self.map_size * 10), self.map_size * 10):
                if broke:
                    break
                if '0' in self.game_map[i]:
                    for k in random.sample(range(self.map_size * 10), self.map_size * 10):
                        if self.game_map[i][k] == '0' and not broke:
                            self.game_map[i][k] = 'C'
                            self.chest = (k, i)
                            broke = True
                        elif self.game_map[i][k] == '.' and en > 0:
                            en -= 1
                            self.game_map[i][k] = 'E'
                            self.entities['enemies'].append(Entity((k, i), self,
                                                                   type_name='Enemy',
                                                                   standing_on='.'))

        def find_objects(self):
            for i in range(self.map_size * 10):
                for k in range(self.map_size * 10):
                    if self.game_map[k][i] not in ['.', '0', '1', 'P']:
                        if self.game_map[k][i] == 'E':
                            self.entities['enemies'].append(Entity((i, k), self,
                                                                   type_name='Enemy'))

        def victory(self):
            self.parent.change_screen(self.parent.Victory(self.parent))
    """
    Класс меню игры
    """
    class Menu:
        def __init__(self, parent, starting=False):
            self.parent = parent
            self.objects = {'buttons': [Button(self.parent.display, (50, 200), (400, 100),
                                               text="Start" if starting else "Continue",
                                               alt=(100, 0, 0)),
                                        Button(self.parent.display, (50, 350), (325, 100),
                                               text="Load", alt=(100, 0, 0), bw=2),
                                        Button(self.parent.display, (50, 500), (325, 100),
                                               text="Save", alt=(100, 0, 0), bw=2),
                                        Button(self.parent.display, (50, 650), (250, 100),
                                               text="Quit", alt=(100, 0, 0), bw=2)]}
            self.objects['buttons'][0].set_act(self.parent.change_screen,
                                               value=self.parent.game)
            self.objects['buttons'][1].set_act(self.parent.load_game)
            self.objects['buttons'][2].set_act(self.parent.save_game)
            self.objects['buttons'][3].set_act(self.parent.kill_the_game)

        def render(self):
            self.parent.display.blit(pygame.font.Font(None,
                                                      150).render("Annoying Town", 80,
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
                self.parent.change_screen(self.parent.game)
            elif key.key == pygame.K_ESCAPE:
                self.parent.kill_the_game()

        def mouse_moved(self, mouse):
            for i in self.objects:
                for k in self.objects[i]:
                    k.mouse_down_track(mouse)

    """
    Победное окно
    """

    class Victory:
        def __init__(self, parent):
            self.parent = parent

        def render(self):
            self.parent.display.blit(pygame.font.Font(None,
                                                      150).render("Победа!", 80,
                                                                  (100, 0, 0)), (50, 50))

        def mouse_move(self, mouse):
            pass

        def key_pressed(self, key):
            pass

        def mouse_pressed(self, mouse):
            pass

    """
    Методы класса Game
    """
    def load_game(self):
        with open("info.dat", 'rt') as save:
            file = save.readlines()
        map_size = int(file.pop(0).rstrip())
        current_lvl = int(file.pop(0).rstrip())
        player_pos = tuple([int(i) for i in file.pop(0).rstrip()[1:-1].split(', ')])
        standing_on = file.pop(0).rstrip()
        enemies = []
        e_d = file.pop(0).rstrip().split()
        for i in range(0, len(e_d), 3):
            enemies.append(Entity(tuple([int(k)
                                         for k in [e_d[i][1:-1], e_d[i + 1][:-1]]]),
                                  self.game, standing_on=e_d[i + 2], type_name='Enemy'))
        game_map = [i.rstrip().split() for i in file]
        self.game = self.Game(self, map_size=map_size, current_lvl=current_lvl,
                              player_pos=player_pos, standing_on=standing_on,
                              game_map=game_map, new=False, entities=enemies)
        if type(self.screen) == Game.Menu:
            self.screen.objects['buttons'][0].set_act(self.change_screen,
                                                      value=self.game)

    def save_game(self):
        with open("info.dat", 'wt') as save:
            save.write(str(self.game.map_size) + '\n' +
                       str(self.game.current_lvl) + '\n' +
                       str(self.game.player_pos) + '\n' +
                       self.game.standing_on + '\n')
            for i in self.game.entities['enemies']:
                save.write(str(i.pos) + ' ' + i.standing_on + ' ')
            save.write('\n')
            for i in self.game.game_map:
                save.write(' '.join(i) + '\n')

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
            self.mouse_moved(mouse)
        else:
            self.mouse_down = False
            self.screen.mouse_pressed(mouse)

    def mouse_moved(self, mouse):
        self.screen.mouse_moved(mouse)


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
