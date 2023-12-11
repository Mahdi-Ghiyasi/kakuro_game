from csp import *
import pygame
from pygame.locals import *
parameters = {'inference': None, 'variable_ordering': None, 'value_ordering': None}
parameters_name = {'inference': None, 'variable_ordering': None, 'value_ordering': None}
selected_board = None
slow = False
all_set = False

# Kakuro puzzles

easy1 = [
    ['X', 'X', [30,''], [4,''], [24,''], 'X', [4,''], [16,'']],
    ['X', [16,19], '', '', '', [9,10], '', ''],
    [['',39], '', '', '', '', '', '', ''],
    [['',15], '', '', [23,10], '', '', [10,''], 'X'],
    ['X', ['',16], '', '', [6,4], '', '', [16,'']],
    ['X', [14,''], [16,9], '', '', [4,12], '', ''],
    [['',35], '', '', '', '', '', '', ''],
    [['',16], '', '', ['',7], '', '', '', 'X']
]

easy2 = [
    ['X', 'X', [11,''], [5,''], 'X',[15,''], [15,''],'X'],
    ['X', [3,3], '', '',[4,17], '', '', 'X'],
    [['',22], '', '', '', '', '', '', 'X'],
    [['',3], '', '', [11,4], '', '', [10,''], 'X'],
    ['X', ['',8], '', '', [7,3], '', '', [8,'']],
    ['X', 'X', [4,4], '', '', [3,4], '', ''],
    ['X', ['',21], '', '', '', '', '', ''],
    ['X', ['',3], '', '', ['',4], '', '', 'X']
]
medium1 = [
    ['X', 'X', ['20',''], ['3',''], ['23',''], 'X', ['12',''], ['16','']],
    ['X', ['5','12'], '', '', '', ['24','16'], '', ''],
    [['','41'], '', '', '', '', '', '', ''],
    [['','3'], '', '', ['24','13'], '', '', ['11',''], 'X'],
    ['X', ['','17'], '', '', ['23','10'], '', '', ['16','']],
    ['X', ['14',''], ['5','16'], '', '', ['17','11'], '', ''],
    [['','42'], '', '', '', '', '', '', ''],
    [['','10'], '', '', ['','22'], '', '', '', 'X']
]

medium2 = [
    ['X', 'X', 'X', 'X', ['40',''], ['3',''], 'X', 'X'],
    ['X', 'X', 'X', ['8','6'], '', '', 'X', 'X'],
    ['X', 'X', ['','7'], '', '', '', ['3',''], ['14','']],
    ['X', ['6',''], ['4','10'], '', '', ['24','9'], '', ''],
    [['','28'], '', '', '', '', '', '', ''],
    [['','3'], '', '', ['17','17'], '', '', 'X', 'X'],
    ['X', 'X', ['','23'], '', '', '', 'X', 'X'],
    ['X', 'X', ['','16'], '', '', 'X', 'X', 'X']
]

hard1 = [
    ['X', ['10',''], ['10',''], 'X', 'X', 'X', 'X', 'X', ['23',''], ['16','']],
    [['','4'], '', '', ['17',''], 'X', 'X', 'X', ['17','16'], '', ''],
    [['','23'], '', '', '', ['20',''], 'X', ['30','24'], '', '', ''],
    ['X', ['','13'], '', '', '', ['20','23'], '', '', '', 'X'],
    ['X', 'X', 'X', ['','11'], '', '', '', '', 'X', 'X'],
    ['X', 'X', 'X', ['6','23'], '', '', '', 'X', 'X', 'X'],
    ['X', 'X', ['7','25'], '', '', '', '', ['3',''], ['9',''], 'X'],
    ['X', ['4','8'], '', '', '', ['','7'], '', '', '', ['4','']],
    [['','6'], '', '', '', 'X', 'X', ['','6'], '', '', ''],
    [['','3'], '', '', 'X', 'X', 'X', 'X', ['','4'], '', '']
]

hard2 = [
    ['X', 'X', 'X', ['15',''], ['6',''], 'X', ['21',''], ['12',''], 'X', 'X'],
    ['X', 'X', ['42','10'], '', '', ['16','16'], '', '', ['31',''], 'X'],
    ['X', ['16','42'], '', '', '', '', '', '', '', ['3','']],
    [['','16'], '', '', ['6','19'], '', '', '', ['7','5'], '', ''],
    [['','17'], '', '', '', 'X', 'X', ['','7'], '', '', ''],
    ['X', ['3','9'], '', '', 'X', 'X', ['','3'], '', '', ['10','']],
    [['','7'], '', '', '', ['24',''], ['12',''], ['24','6'], '', '', ''],
    [['','4'], '', '', ['3','24'], '', '', '', ['15','15'], '', ''],
    ['X', ['','39'], '', '', '', '', '', '', '', 'X'],
    ['X', 'X', ['','11'], '', '', ['','16'], '', '', 'X', 'X']
]

expert1 = [
    ['X', 'X', 'X', ['17',''], ['19',''], 'X', 'X', ['7',''], ['44',''], 'X'],
    ['X', ['3',''], ['37','17'], '', '', 'X', ['','10'], '', '', ['23','']],
    [['','20'], '', '', '', '', ['6',''], ['3','15'], '', '', ''],
    [['','5'], '', '', ['3','25'], '', '', '', '', '', ''],
    ['X', ['','8'], '', '', ['','3'], '', '', ['10','15'], '', ''],
    ['X', ['13','3'], '', '', ['7',''], ['5',''], ['','17'], '', '', 'X'],
    [['','9'], '', '', ['10','3'], '', '', ['16','6'], '', '', ['11','']],
    [['','38'], '', '', '', '', '', '', ['3','17'], '', ''],
    [['','7'], '', '', '', 'X', ['','12'], '', '', '', ''],
    ['X', ['','4'], '', '', 'X', ['','3'], '', '', 'X', 'X']
]

expert2 = [
    ['X', 'X', 'X', ['3',''], ['23',''], ['45',''], ['6',''], 'X', 'X', 'X'],
    ['X', 'X', ['','12'], '', '', '', '', ['4',''], 'X', 'X'],
    ['X', ['20',''], ['32','21'], '', '', '', '', '', ['15',''], 'X'],
    [['','3'], '', '', ['17','15'], '', '', ['5','4'], '', '', ['16','']],
    [['','24'], '', '', '', ['16','3'], '', '', ['4','7'], '', ''],
    [['','45'], '', '', '', '', '', '', '', '', ''],
    [['','17'], '', '', ['13','17'], '', '', ['24','6'], '', '', ''],
    ['X', ['','16'], '', '', ['17','15'], '', '', ['13','6'], '', ''],
    ['X', 'X', ['','32'], '', '', '', '', '', 'X', 'X'],
    ['X', 'X', 'X', ['','30'], '', '', '', '', 'X', 'X']
]


class Button:
    def __init__(self, x, y, width, height, text):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text

    def draw(self, surface, font, color='gray'):
        if color == 'green':
            pygame.draw.rect(surface, (50, 200, 50), self.rect)
        elif color == 'red':
            pygame.draw.rect(surface, (200, 50, 50), self.rect)
        else:
            pygame.draw.rect(surface, (200, 200, 200), self.rect)
        text = font.render(self.text, True, (0, 0, 0))
        text_rect = text.get_rect(center=self.rect.center)
        surface.blit(text, text_rect)

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

def update_grid(screen, c, cell_width, font):
    board = c.board
    rows = len(board)
    cols = len(board[0])

    # a counter label
    counter_text = font.render('assignments: ' + str(c.num_assigns), True, (0, 0, 0))
    pygame.draw.rect(screen, (255, 255, 255), (0, rows * cell_width + 5, 300,28))
    screen.blit(counter_text, (15, rows * cell_width + 10))

    for i in range(rows):
        for j in range(cols):
            cell_value = board[i][j]

            x1 = j * cell_width
            y1 = i * cell_width
            x2 = (j + 1) * cell_width
            y2 = (i + 1) * cell_width

            if cell_value != 'X' and type(cell_value) != list:
                pygame.draw.rect(screen, (255, 255, 255), (x1 + 2, y1 + 2, cell_width - 2, cell_width - 2))
                text = font.render(str(cell_value), True, (0, 0, 0))
                screen.blit(text, ((x1 + x2) / 2 - 4, (y1 + y2) / 2 - 10))


def start_graphic(problem, cell_width=50):
    global parameters
    global all_set
    global parameters_name
    global slow

    pygame.init()
    width, height = cell_width * len(problem.board[0]) + 200, 600
    screen = pygame.display.set_mode((width, height))
    clock = pygame.time.Clock()

    board = problem.board
    rows = len(board)
    cols = len(board[0])
    canvas_width = cols * cell_width
    canvas_height = rows * cell_width

    screen.fill((255, 255, 255))

    font = pygame.font.Font('font/RobotoMono.ttf', 15)

    counter_text = font.render('inference: ', True, (0, 0, 0))
    screen.blit(counter_text, (canvas_width + 20, 20))

    no_inference_button = Button(canvas_width + 20, 50, 150, 30, "No inference")
    arc_consistency_button = Button(canvas_width + 20, 100, 150, 30, "Arc consistency")
    forward_checking_button = Button(canvas_width + 20, 150, 150, 30, "Forward checking")
    no_inference_button.draw(screen, font)
    arc_consistency_button.draw(screen, font)
    forward_checking_button.draw(screen, font)

    counter_text = font.render('variable ordering: ', True, (0, 0, 0))
    screen.blit(counter_text, (canvas_width + 20, 220))

    mcv_button = Button(canvas_width + 20, 250, 150, 30, "MCV")
    no_variable_ordering_button = Button(canvas_width + 20, 300, 150, 30, "No ordering")
    mcv_button.draw(screen, font)
    no_variable_ordering_button.draw(screen, font)

    counter_text = font.render('value ordering: ', True, (0, 0, 0))
    screen.blit(counter_text, (canvas_width + 20, 370))

    lcv_button = Button(canvas_width + 20, 400, 150, 30, "LCV")
    no_value_ordering_button = Button(canvas_width + 20, 450, 150, 30, "No ordering")
    lcv_button.draw(screen, font)
    no_value_ordering_button.draw(screen, font)

    all_set_button = Button(canvas_width + 20, 500, 150, 30, "Solve")
    all_set_button.draw(screen, font, 'red')

    slow_button = Button(canvas_width + 20, 550, 150, 30, "Slow mode")
    slow_button.draw(screen, font, 'red')

    counter_text = font.render('board: ', True, (0, 0, 0))
    screen.blit(counter_text, (canvas_width + 210, 20))

    for i in range(rows):
        for j in range(cols):
            cell_value = board[i][j]

            x1 = j * cell_width
            y1 = i * cell_width
            x2 = (j + 1) * cell_width
            y2 = (i + 1) * cell_width

            if cell_value == 'X':
                pygame.draw.rect(screen, (50, 50, 50), (x1, y1, cell_width, cell_width))
            elif type(cell_value) == list:
                pygame.draw.rect(screen, (125, 125, 125), (x1, y1, cell_width, cell_width))
                pygame.draw.line(screen, (0, 0, 0), (x1, y1), (x2, y2), 2)

                text = font.render(str(cell_value[1]), True, (0, 0, 0))
                screen.blit(text, ((x1 + x2) / 2 + 5, (y1 + y2) / 2 - 13))

                text = font.render(str(cell_value[0]), True, (0, 0, 0))
                screen.blit(text, ((x1 + x2) / 2 - 13, (y1 + y2) / 2 + 5))

    # Draw grid lines
    for i in range(rows + 1):
        pygame.draw.line(screen, (0, 0, 0), (0, i * cell_width), (canvas_width, i * cell_width), 2)
    for j in range(cols + 1):
        pygame.draw.line(screen, (0, 0, 0), (j * cell_width, 0), (j * cell_width, canvas_height), 2)

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
            elif all_set == False:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # Left mouse button
                        pos = pygame.mouse.get_pos()
                        if no_inference_button.is_clicked(pos):
                             parameters['inference'] = no_inference
                             parameters_name['inference'] = 'no inference'
                             no_inference_button.draw(screen, font, 'green')
                        elif arc_consistency_button.is_clicked(pos):
                                parameters['inference'] = mac
                                parameters_name['inference'] = 'maintain arc consistency'
                                arc_consistency_button.draw(screen, font, 'green')
                        elif forward_checking_button.is_clicked(pos):
                                parameters['inference'] = forward_checking
                                parameters_name['inference'] = 'forward checking'
                                forward_checking_button.draw(screen, font, 'green')
                        elif mcv_button.is_clicked(pos):
                                parameters['variable_ordering'] = mcv_inference
                                parameters_name['variable_ordering'] = 'mcv'
                                mcv_button.draw(screen, font, 'green')
                        elif no_variable_ordering_button.is_clicked(pos):
                                parameters['variable_ordering'] = first_unassigned_variable
                                parameters_name['variable_ordering'] = 'first unassigned variable'
                                no_variable_ordering_button.draw(screen, font, 'green')
                        elif lcv_button.is_clicked(pos):
                                parameters['value_ordering'] = lcv
                                parameters_name['value_ordering'] = 'lcv'
                                lcv_button.draw(screen, font, 'green')
                        elif no_value_ordering_button.is_clicked(pos):
                                parameters['value_ordering'] = unordered_domain_values
                                parameters_name['value_ordering'] = 'unordered domain values'
                                no_value_ordering_button.draw(screen, font, 'green')
                        elif all_set_button.is_clicked(pos):
                                all_set = True
                                all_set_button.draw(screen, font, 'green')
                        elif slow_button.is_clicked(pos):
                                slow = True
                                slow_button.draw(screen, font, 'green')

                        if all_set:
                            counter_text = font.render('inference: ' + str(parameters_name['inference'] or ""), True, (0, 0, 0))
                            screen.blit(counter_text, (15, canvas_height + 30))

                            counter_text = font.render('variable ordering: ' + str(parameters_name['variable_ordering'] or ""), True, (0, 0, 0))
                            screen.blit(counter_text, (15, canvas_height + 50))

                            counter_text = font.render('value ordering: ' + str(parameters_name['value_ordering'] or ""), True, (0, 0, 0))
                            screen.blit(counter_text, (15, canvas_height + 70))


        update_grid(screen, problem, cell_width, font)

        pygame.display.flip()
        clock.tick(1000000)


def pre_start_graphic(hint=False):
    global selected_board

    pygame.init()
    width, height = 600 , 600
    screen = pygame.display.set_mode((width, height))
    clock = pygame.time.Clock()

    screen.fill((255, 255, 255))

    font = pygame.font.Font('font/RobotoMono.ttf', 15)


    counter_text = font.render('board: ', True, (0, 0, 0))
    screen.blit(counter_text, (275, 20))

    easy1_button = Button(200, 50, 200, 30, "Easy 1")
    easy2_button = Button(200, 100, 200, 30, "Easy 2")
    medium1_button = Button(200, 150, 200, 30, "Medium 1")
    medium2_button = Button(200, 200, 200, 30, "Medium 2")
    hard1_button = Button(200, 250, 200, 30, "Hard 1")
    hard2_button = Button(200, 300, 200, 30, "Hard 2")
    expert1_button = Button(200, 350, 200, 30, "Expert 1")
    expert2_button = Button(200, 400, 200, 30, "Expert 2")
    easy1_button.draw(screen, font)
    easy2_button.draw(screen, font)
    medium1_button.draw(screen, font)
    medium2_button.draw(screen, font)
    hard1_button.draw(screen, font)
    hard2_button.draw(screen, font)
    expert1_button.draw(screen, font)
    expert2_button.draw(screen, font)

    counter_text = font.render('After selection, please wait a few moments', True, (0, 0, 0))
    screen.blit(counter_text, (120, 450))

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button
                    pos = pygame.mouse.get_pos()
                    if easy1_button.is_clicked(pos):
                        selected_board = easy1
                        easy1_button.draw(screen, font, 'green')
                    elif easy2_button.is_clicked(pos):
                        selected_board = easy2
                        easy2_button.draw(screen, font, 'green')
                    elif medium1_button.is_clicked(pos):
                        selected_board = medium1
                        medium1_button.draw(screen, font, 'green')
                    elif medium2_button.is_clicked(pos):
                        selected_board = medium2
                        medium2_button.draw(screen, font, 'green')
                    elif hard1_button.is_clicked(pos):
                        selected_board = hard1
                        hard1_button.draw(screen, font, 'green')
                    elif hard2_button.is_clicked(pos):
                        selected_board = hard2
                        hard2_button.draw(screen, font, 'green')
                    elif expert1_button.is_clicked(pos):
                        selected_board = expert1
                        expert1_button.draw(screen, font, 'green')
                    elif expert2_button.is_clicked(pos):
                        selected_board = expert2
                        expert2_button.draw(screen, font, 'green')
        if selected_board is not None:
            time.sleep(1)
            pygame.quit()
            return

        pygame.display.flip()
        clock.tick(1000)
