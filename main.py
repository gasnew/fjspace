# ---- NECESSARY EVILS ---- #
# important things
import logging, sys
import random
import pygame
from pygame.locals import *
from playerList import PlayerList
from game import Game
from wheel import Wheel
from keys import Keys
from hud import Hud
from scoreboard import Scoreboard
from gameState import GameState
from textRenderer import TextRenderer
from shadowedPressable import ShadowedPressable
from gameColor import GameColor

# init logging
logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)
# includes critical, error, warning, info, debug :)

# init pygame whatnot
RESOLUTION = (640, 480)
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
INC_SOUND_TIME = 0.1
NUM_WINS = 3

# visual params
p_list_rect = pygame.Rect((0, 0), (screen.get_width(), screen.get_height()))
scoreboard_rect = pygame.Rect((screen.get_width() * 0.1, screen.get_height() * 0.1), (screen.get_width() * 0.8, screen.get_height() * 0.8))

top_rect = pygame.Rect(0, 0, screen.get_width(), screen.get_height() * 0.2)
top_rect_left = pygame.Rect(0, 0, screen.get_width() / 2, top_rect.height)
top_rect_right = pygame.Rect(screen.get_width() / 2, 0, screen.get_width() / 2, top_rect.height)

game_rect = pygame.Rect(0, top_rect.bottom, screen.get_width(), screen.get_height() * 0.7)

bottom_rect = pygame.Rect(0, game_rect.bottom, screen.get_width(), screen.get_height() * 0.1)

shadow_dist = screen.get_width() * 0.005

# gameplay values
big_f_agree = big_j_agree = 0
f_wins = j_wins = 0
score_streak = 0

# main classes
keys = Keys()
p_list = PlayerList(p_list_rect, shadow_dist, sys_font)
game = Game(WIN_TIME, COOLDOWN_TIME, STALE_TIME, TOTAL_TIME, FAILURE_TIME, INC_SOUND_TIME, keys, game_rect, shadow_dist, sys_font)
wheel = Wheel(game_rect, shadow_dist, sys_font)
hud = Hud(top_rect, bottom_rect, shadow_dist, sys_font)
scoreboard = Scoreboard(scoreboard_rect, shadow_dist, sys_font, p_list)

# state stuff
def state_response(state):
  global big_f_agree, big_j_agree, f_wins, j_wins, score_streak, f_win_rects, j_win_rects, game

  if state == GameState.COUNTDOWN:
    if NUM_WINS in {f_wins, j_wins}:
      game_state.set_state(GameState.WINNER)
      wlf.color = GameColor.Green if winner == "f" else GameColor.Red
      wlj.color = GameColor.Green if winner == "j" else GameColor.Red
      pmf.color = GameColor.Green if winner == "f" else GameColor.Red
      pmj.color = GameColor.Green if winner == "j" else GameColor.Red

      if winner == "f":
        score_streak += 1
        p_list.pf.score += score_streak
      else:
        score_streak = 1
        p_list.pj.score += score_streak
    else:
      game.reset()
      begin_sound.play()
  elif state == GameState.NEW_OPPONENT:
    if j_wins == NUM_WINS:
      p_list.swap_players()
    if not f_wins == j_wins == 0:
      p_list.new_opponent()
    else:
      p_list.shuffle()

    big_f_agree = big_j_agree = 1
    f_wins = j_wins = 0
    f_win_rects = []
    j_win_rects = []

    game.reset()

game_state = GameState(GameState.PLAYER_LIST, state_response)
p_list.focus()

# render thing(s) (can't put this in game or hud?)
namef = TextRenderer(sys_font, 2, (top_rect_left.centerx, bottom_rect.centery), shadow_dist)
namej = TextRenderer(sys_font, 2, (top_rect_right.centerx, bottom_rect.centery), shadow_dist)
streak_text = TextRenderer(sys_font, 1, (bottom_rect.width * 0.08, bottom_rect.centery + bottom_rect.height * 0.25), shadow_dist)
big_namef = TextRenderer(sys_font, 4, (top_rect_left.centerx, game_rect.centery), shadow_dist, GameColor.F.Dark)
big_namej = TextRenderer(sys_font, 4, (top_rect_right.centerx, game_rect.centery), shadow_dist, GameColor.J.Dark)
vs_text = TextRenderer(sys_font, 2, game_rect.center, shadow_dist)

big_f, big_f_shadow = ShadowedPressable.make_pressable_key("[F]", sys_font, 4)
big_f = ShadowedPressable(big_f.convert_alpha(), big_f_shadow, (top_rect_left.centerx, game_rect.top + game_rect.height * 0.8), shadow_dist)
big_j, big_j_shadow = ShadowedPressable.make_pressable_key("[J]", sys_font, 4)
big_j = ShadowedPressable(big_j.convert_alpha(), big_j_shadow, (top_rect_right.centerx, game_rect.top + game_rect.height * 0.8), shadow_dist)

counter = TextRenderer(sys_font, 4, game_rect.center, shadow_dist)
ready_text = TextRenderer(sys_font, 2, (game_rect.centerx, game_rect.top + game_rect.height * 0.35), shadow_dist)
win_rect_size = top_rect.width * 0.02
win_rect = Rect(top_rect.centerx - win_rect_size / 2, win_rect_size, win_rect_size, win_rect_size)
win_rect_shadows = [win_rect.move(win_rect.width * 2 * idx, 0) for idx in [-3, -2, -1, 1, 2, 3]]
f_win_rects = []
j_win_rects = []

wlf = TextRenderer(sys_font, 4, (top_rect_left.centerx, game_rect.top + game_rect.height * 0.35), shadow_dist)
wlj = TextRenderer(sys_font, 4, (top_rect_right.centerx, game_rect.top + game_rect.height * 0.35), shadow_dist)
pmf = TextRenderer(sys_font, 4, (top_rect_left.centerx, game_rect.top + game_rect.height * 0.65), shadow_dist)
pmj = TextRenderer(sys_font, 4, (top_rect_right.centerx, game_rect.top + game_rect.height * 0.65), shadow_dist)

# sounds
vs_sound = pygame.mixer.Sound("SFX/VS.wav")
begin_sound = pygame.mixer.Sound("SFX/begin_game.wav")
climax_sound = pygame.mixer.Sound("SFX/climax.wav")
victory_sounds = [pygame.mixer.Sound("SFX/vic{0}.wav".format(i)) for i in range(3)]

# the loop
while 1:
  delta_t = clock.tick(60)

  # key stuff
  keys.update(pygame.event.get([KEYDOWN, KEYUP]), lambda char: p_list.input(char))
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

  # player list stuff
  p_list.p_list_stuff()

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

  # non-hud weird stuff
  if game_state.state == GameState.NEW_OPPONENT:
    if keys.f: big_f_agree = big_f_agree - (delta_t / (AGREE_TIME * 1000)) if big_f_agree > 0 else 0
    else: big_f_agree = 1
    
    if keys.j: big_j_agree = big_j_agree - (delta_t / (AGREE_TIME * 1000)) if big_j_agree > 0 else 0
    else: big_j_agree = 1

  # state stuff
  game_state.update(delta_t)
  if game_state.state == GameState.PLAYER_LIST and keys.enter:
    game_state.set_state(GameState.NEW_OPPONENT)
    p_list.defocus()
    game.reset()
    vs_sound.play()
  elif game_state.state == GameState.NEW_OPPONENT and keys.f and keys.j and big_f_agree == big_j_agree == 0:
    game_state.set_state(GameState.COUNTDOWN)
  elif game_over:
    if winner == "stale":
      game_state.set_state(GameState.WHEEL)
      wheel.start(game_state.state_timer, perc_f, perc_j)
    else:
      game_state.set_state(GameState.VICTORY)
      climax_sound.play()
      random.choice(victory_sounds).play()
      if winner == "f":
        f_wins += 1
        p_list.pf.wins += 1
        p_list.pj.losses += 1

        f_win_rects.append(win_rect.move(-(win_rect.width * 2) * f_wins - shadow_dist, -shadow_dist))
      else:
        j_wins += 1
        p_list.pj.wins += 1
        p_list.pf.losses += 1
        j_win_rects.append(win_rect.move((win_rect.width * 2) * j_wins - shadow_dist, -shadow_dist))

  # render stuff
  game.render_stuff(screen, render_space = game_state.state == GameState.RUNNING, render_keys = game_state.state != GameState.NEW_OPPONENT)
  if game_state.state == GameState.COUNTDOWN:
    counter.render(screen, str(game_state.state_timer)[:4])
    ready_text.render(screen, "READY?!?")
  if game_state.state == GameState.WHEEL:
    wheel.render(screen, delta_t)

  pygame.draw.rect(screen, GameColor.F.Med, top_rect_left)
  pygame.draw.rect(screen, GameColor.J.Med, top_rect_right)
  pygame.draw.rect(screen, GameColor.Shadow, bottom_rect)

  namef.render(screen, p_list.pf.name, GameColor.lighten(p_list.pf.color))
  namej.render(screen, p_list.pj.name, GameColor.lighten(p_list.pj.color))
  streak_text.render(screen, "streak:{0}".format(score_streak))

  if game_state.state == GameState.NEW_OPPONENT:
    big_namef.render(screen, p_list.pf.name, p_list.pf.color)
    big_namej.render(screen, p_list.pj.name, p_list.pj.color)
    vs_text.render(screen, "VS")

    big_f.down = keys.f
    big_j.down = keys.j
    big_f.render(screen, big_f_agree)
    big_j.render(screen, big_j_agree)

  if game_state.state == GameState.WINNER:
    wlf.render(screen, "WIN" if winner == "f" else "LOSE")
    wlj.render(screen, "WIN" if winner == "j" else "LOSE")

    pmf.render(screen, "+{0}".format(score_streak) if winner == "f" else "")
    pmj.render(screen, "+1" if winner == "j" else "")

  for rect in win_rect_shadows: pygame.draw.rect(screen, GameColor.Shadow, rect)
  for rect in f_win_rects: pygame.draw.rect(screen, GameColor.F.Light, rect)
  for rect in j_win_rects: pygame.draw.rect(screen, GameColor.J.Light, rect)

  hud.render_stuff(screen, game.timer, game.perc_f, game.perc_j, render_percs = game_state.state in {GameState.RUNNING, GameState.WHEEL})

  if game_state.state == GameState.PLAYER_LIST:
    p_list.render_stuff(screen)

  if (not (game_state.state in {GameState.PLAYER_LIST, GameState.RUNNING})) and keys.tab:
    scoreboard.render_stuff(screen)

  pygame.display.flip()
