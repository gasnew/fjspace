# ---- NECESSARY EVILS ---- #
# important things
import logging, sys
import random
import pygame
from pygame.locals import *
from keys import Keys
from match import Match

# init logging
logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)
# includes critical, error, warning, info, debug :)

# init pygame whatnot
RESOLUTION = (853, 480)
pygame.init()
screen = pygame.display.set_mode(RESOLUTION)
pygame.mixer.quit() 
pygame.mixer.init(frequency=44100, buffer=0)

clock = pygame.time.Clock()

sys_font = pygame.font.Font("C:\Windows\Fonts\8514oem.fon", 100)

# ---- THE GAME ITSELF ---- #
# gameplay params
AGREE_TIME = 0.5
WIN_TIME = 6
COOLDOWN_TIME = 2
STALE_TIME = 5
TOTAL_TIME = 35
FAILURE_TIME = 0.5
NUM_WINS = 3

# visual params
p_list_rect = pygame.Rect((0, 0), (screen.get_width(), screen.get_height()))
scoreboard_rect = pygame.Rect((screen.get_width() * 0.3125, screen.get_height() * 0.1), (screen.get_width() * 0.375, screen.get_height() * 0.8))

top_rect = pygame.Rect(0, 0, screen.get_width(), screen.get_height() * 0.2)
top_rect_left = pygame.Rect(0, 0, screen.get_width() / 2, top_rect.height)
top_rect_right = pygame.Rect(screen.get_width() / 2, 0, screen.get_width() / 2, top_rect.height)

game_rect = pygame.Rect(0, top_rect.bottom, screen.get_width(), screen.get_height() * 0.7)

bottom_rect = pygame.Rect(0, game_rect.bottom, screen.get_width(), screen.get_height() * 0.1)

shadow_dist = screen.get_width() * 0.005

# main classes
keys = Keys()
match = Match(AGREE_TIME, WIN_TIME, COOLDOWN_TIME, STALE_TIME, TOTAL_TIME, FAILURE_TIME, NUM_WINS,
              keys, p_list_rect, scoreboard_rect, top_rect, top_rect_left, top_rect_right, game_rect, bottom_rect, shadow_dist, sys_font)

# the loop
while 1:
  delta_t = clock.tick(60)

  # key stuff
  keys.update(pygame.event.get([KEYDOWN, KEYUP]), lambda char: match.p_list.input(char))
  for event in pygame.event.get():
    if event.type == QUIT:
      pygame.quit()
      sys.exit()
  if keys.alt and keys.f4:
    pygame.quit()
    sys.exit()
  if keys.f11_toggle and not (screen.get_flags() & pygame.FULLSCREEN):
    pygame.display.set_mode(RESOLUTION, pygame.FULLSCREEN)
  elif not keys.f11_toggle and screen.get_flags() & pygame.FULLSCREEN:
    pygame.display.set_mode(RESOLUTION)

  # update stuff
  match.match_stuff(delta_t)

  # render stuff
  match.render_stuff(screen)

  pygame.display.flip()
