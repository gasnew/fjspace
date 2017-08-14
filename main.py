# ---- NECESSARY EVILS ---- #
# important things
import logging, sys
import pygame
from pygame.locals import *
from game import Game
from wheel import Wheel
from keys import Keys
from hud import Hud
from gameState import GameState
from textRenderer import TextRenderer

# init logging
logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)
# includes critical, error, warning, info, debug :)

# init pygame whatnot
pygame.init()
screen = pygame.display.set_mode((640, 480))
clock = pygame.time.Clock()

sys_font = pygame.font.Font("C:\Windows\Fonts\8514oem.fon", 50)

# ---- THE GAME ITSELF ---- #
# gameplay params
WIN_TIME = 6
COOLDOWN_TIME = 2
TOTAL_TIME = 1
FAILURE_TIME = 0.5

# visual params
top_rect = pygame.Rect(0, 0, screen.get_width(), screen.get_height() * 0.2)
top_rect_left = pygame.Rect(0, 0, screen.get_width() / 2, top_rect.height)
top_rect_right = pygame.Rect(screen.get_width() / 2, 0, screen.get_width() / 2, top_rect.height)

game_rect = pygame.Rect(0, top_rect.bottom, screen.get_width(), screen.get_height() * 0.7)

bottom_rect = pygame.Rect(0, game_rect.bottom, screen.get_width(), screen.get_height() * 0.1)

shadow_dist = screen.get_width() * 0.005

# gameplay values
f_wins = j_wins = 0

# main classes
keys = Keys()
game = Game(WIN_TIME, COOLDOWN_TIME, TOTAL_TIME, FAILURE_TIME, keys, game_rect, shadow_dist, sys_font)
wheel = Wheel(game_rect, shadow_dist, sys_font)
hud = Hud(top_rect, bottom_rect, shadow_dist, sys_font, (111, 134, 149), (206, 194, 136))

# state stuff
def state_response(state):
  if state == GameState.COUNTDOWN:
    game.reset()

game_state = GameState(state_response)

# render thing(s) (can't put this in game or hud?)
counter = TextRenderer(sys_font, 4, game_rect.center, shadow_dist)
ready_text = TextRenderer(sys_font, 2, (game_rect.centerx, game_rect.top + game_rect.height * 0.35), shadow_dist)
win_rect_size = top_rect.width * 0.02
win_rect = Rect(top_rect.centerx - win_rect_size / 2, win_rect_size, win_rect_size, win_rect_size)
f_win_rects = []
j_win_rects = []

# the loop
while 1:
  delta_t = clock.tick(60)

  # key stuff
  keys.update(pygame.event.get([KEYDOWN, KEYUP]))
  for event in pygame.event.get():
    if event.type == QUIT:
      pygame.quit()
      sys.exit()

  # game stuff
  game_over = False
  perc_f = perc_j = 0
  if game_state.state == GameState.RUNNING:
    game_over, winner, perc_f, perc_j = game.game_stuff(delta_t)

  # wheel stuff
  if game_state.state == GameState.WHEEL:
    game_over, winner = wheel.wheel_stuff(delta_t)

  # hud stuff
  hud.hud_stuff()

  # state stuff
  game_state.update(delta_t)
  if game_over:
    if winner == "stale":
      game_state.set_state(GameState.WHEEL)
      wheel.start(game_state.state_timer, perc_f, perc_j)
    else:
      game_state.set_state(GameState.VICTORY)
      if winner == "f":
        f_wins += 1
        f_win_rects.append(win_rect.move(-(win_rect.width * 2) * f_wins, 0))
      else:
        j_wins += 1
        j_win_rects.append(win_rect.move((win_rect.width * 2) * j_wins, 0))

  # render stuff
  game.render_stuff(screen, render_space = game_state.state == GameState.RUNNING)
  if game_state.state == GameState.COUNTDOWN:
    counter.render(screen, str(game_state.state_timer)[:4])
    ready_text.render(screen, "READY?!?")
  if game_state.state == GameState.WHEEL:
    wheel.render(screen, delta_t)

  pygame.draw.rect(screen, (206, 194, 136), top_rect_left)
  pygame.draw.rect(screen, (111, 134, 149), top_rect_right)
  pygame.draw.rect(screen, (50, 50, 50), bottom_rect)

  for rect in f_win_rects: pygame.draw.rect(screen, (221, 218, 199), rect)
  for rect in j_win_rects: pygame.draw.rect(screen, (204, 214, 221), rect)

  hud.render_stuff(screen, game.timer, game.perc_f, game.perc_j, render_percs = game_state.state == GameState.RUNNING)

  pygame.display.flip()
