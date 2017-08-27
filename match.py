import logging
import random
import pygame
from pygame.locals import *
from playerList import PlayerList
from game import Game
from wheel import Wheel
from hud import Hud
from scoreboard import Scoreboard
from matchState import MatchState
from textRenderer import TextRenderer
from shadowedPressable import ShadowedPressable
from gameColor import GameColor

class Match:
  def __init__(self, AGREE_TIME, WIN_TIME, COOLDOWN_TIME, STALE_TIME, TOTAL_TIME, FAILURE_TIME, INC_SOUND_TIME, NUM_WINS,
               keys, p_list_rect, scoreboard_rect, top_rect, top_rect_left, top_rect_right, game_rect, bottom_rect, shadow_dist, sys_font):
    # -- IMPORTS --
    self.keys = keys
    self.top_rect_left = top_rect_left
    self.top_rect_right = top_rect_right
    self.bottom_rect = bottom_rect
    self.AGREE_TIME = AGREE_TIME
    self.NUM_WINS = NUM_WINS
    self.shadow_dist = shadow_dist

    # -- MATCH INFO --
    self.big_f_agree = self.big_j_agree = 0
    self.f_wins = self.j_wins = 0
    self.score_streak = 0

    # -- NECESSARY CLASSES --
    self.p_list = PlayerList(p_list_rect, shadow_dist, sys_font)
    self.game = Game(WIN_TIME, COOLDOWN_TIME, STALE_TIME, TOTAL_TIME, FAILURE_TIME, INC_SOUND_TIME, self.keys, game_rect, shadow_dist, sys_font)
    self.wheel = Wheel(game_rect, shadow_dist, sys_font)
    self.hud = Hud(top_rect, bottom_rect, shadow_dist, sys_font)
    self.scoreboard = Scoreboard(scoreboard_rect, shadow_dist, sys_font, self.p_list)
    self.match_state = MatchState(MatchState.PLAYER_LIST, self.state_response)

    # -- RENDERING --
    self.f_name_text = TextRenderer(sys_font, 2, (top_rect_left.centerx, bottom_rect.centery), shadow_dist)
    self.j_name_text = TextRenderer(sys_font, 2, (top_rect_right.centerx, bottom_rect.centery), shadow_dist)
    self.streak_text = TextRenderer(sys_font, 1, (bottom_rect.width * 0.08, bottom_rect.centery + bottom_rect.height * 0.25), shadow_dist)
    self.f_name_big_text = TextRenderer(sys_font, 4, (top_rect_left.centerx, game_rect.centery), shadow_dist, GameColor.F.Dark)
    self.j_name_big_text = TextRenderer(sys_font, 4, (top_rect_right.centerx, game_rect.centery), shadow_dist, GameColor.J.Dark)
    self.vs_text = TextRenderer(sys_font, 2, game_rect.center, shadow_dist)

    big_f, big_f_shadow = ShadowedPressable.make_pressable_key("[F]", sys_font, 4)
    self.big_f = ShadowedPressable(big_f.convert_alpha(), big_f_shadow, (top_rect_left.centerx, game_rect.top + game_rect.height * 0.8), shadow_dist)
    big_j, big_j_shadow = ShadowedPressable.make_pressable_key("[J]", sys_font, 4)
    self.big_j = ShadowedPressable(big_j.convert_alpha(), big_j_shadow, (top_rect_right.centerx, game_rect.top + game_rect.height * 0.8), shadow_dist)

    self.counter = TextRenderer(sys_font, 4, game_rect.center, shadow_dist)
    self.ready_text = TextRenderer(sys_font, 2, (game_rect.centerx, game_rect.top + game_rect.height * 0.35), shadow_dist)
    win_rect_size = top_rect.width * 0.02
    self.win_rect = Rect(top_rect.centerx - win_rect_size / 2, win_rect_size, win_rect_size, win_rect_size)
    self.win_rect_shadows = [self.win_rect.move(self.win_rect.width * 2 * idx, 0) for idx in [-3, -2, -1, 1, 2, 3]]
    self.f_win_rects = []
    self.j_win_rects = []

    self.f_win_loss_text = TextRenderer(sys_font, 4, (top_rect_left.centerx, game_rect.top + game_rect.height * 0.35), shadow_dist)
    self.j_win_loss_text = TextRenderer(sys_font, 4, (top_rect_right.centerx, game_rect.top + game_rect.height * 0.35), shadow_dist)
    self.f_plus_minus_text = TextRenderer(sys_font, 4, (top_rect_left.centerx, game_rect.top + game_rect.height * 0.65), shadow_dist)
    self.j_plus_minus_text = TextRenderer(sys_font, 4, (top_rect_right.centerx, game_rect.top + game_rect.height * 0.65), shadow_dist)

    # -- SOUND --
    self.vs_sound = pygame.mixer.Sound("SFX/VS.wav")
    self.begin_sound = pygame.mixer.Sound("SFX/begin_game.wav")
    self.climax_sound = pygame.mixer.Sound("SFX/climax.wav")
    self.victory_sounds = [pygame.mixer.Sound("SFX/vic{0}.wav".format(i)) for i in range(3)]
    self.win_sound = pygame.mixer.Sound("SFX/win.wav")

    self.reset()

  def reset(self):
    self.winner = ""

    self.p_list.focus()
    self.match_state.set_state(MatchState.PLAYER_LIST)

  def state_response(self, state):
    if state == MatchState.COUNTDOWN:
      if self.NUM_WINS in {self.f_wins, self.j_wins}:
        self.match_state.set_state(MatchState.WINNER)
        self.f_win_loss_text.color = GameColor.Green if self.winner == "f" else GameColor.Red
        self.j_win_loss_text.color = GameColor.Green if self.winner == "j" else GameColor.Red
        self.f_plus_minus_text.color = GameColor.Green if self.winner == "f" else GameColor.Red
        self.j_plus_minus_text.color = GameColor.Green if self.winner == "j" else GameColor.Red

        if self.winner == "f":
          self.score_streak += 1
          self.p_list.pf.score += self.score_streak
        else:
          self.score_streak = 1
          self.p_list.pj.score += self.score_streak

        self.win_sound.play()
      else:
        self.game.reset()
        self.begin_sound.play()
    elif state == MatchState.NEW_OPPONENT:
      if self.j_wins == self.NUM_WINS:
        self.p_list.swap_players()
      if not self.f_wins == self.j_wins == 0:
        self.p_list.new_opponent()
        self.vs_sound.play()
      else:
        self.p_list.shuffle()

      self.big_f_agree = self.big_j_agree = 1
      self.f_wins = self.j_wins = 0
      self.f_win_rects = []
      self.j_win_rects = []

      self.game.reset()

  def match_stuff(self, delta_t):
    # player list stuff
    self.p_list.p_list_stuff()

    # self.game stuff
    game_over = False
    perc_f = perc_j = 0
    if self.match_state.state == MatchState.RUNNING:
      game_over, self.winner, perc_f, perc_j = self.game.game_stuff(delta_t)

    # self.wheel stuff
    if self.match_state.state == MatchState.WHEEL:
      game_over, self.winner = self.wheel.wheel_stuff(delta_t)

    # self.hud stuff
    self.hud.hud_stuff()

    # non-self.hud weird stuff
    if self.match_state.state == MatchState.NEW_OPPONENT:
      if self.keys.f: self.big_f_agree = self.big_f_agree - (delta_t / (self.AGREE_TIME * 1000)) if self.big_f_agree > 0 else 0
      else: self.big_f_agree = 1
      
      if self.keys.j: self.big_j_agree = self.big_j_agree - (delta_t / (self.AGREE_TIME * 1000)) if self.big_j_agree > 0 else 0
      else: self.big_j_agree = 1

    # state stuff
    self.match_state.update(delta_t)
    if self.match_state.state == MatchState.PLAYER_LIST and self.keys.enter:
      self.match_state.set_state(MatchState.NEW_OPPONENT)
      self.p_list.defocus()
      self.game.reset()
      self.vs_sound.play()
    elif self.match_state.state == MatchState.NEW_OPPONENT and self.keys.f and self.keys.j and self.big_f_agree == self.big_j_agree == 0:
      self.match_state.set_state(MatchState.COUNTDOWN)
    elif game_over:
      if self.winner == "stale":
        self.match_state.set_state(MatchState.WHEEL)
        self.wheel.start(self.match_state.state_timer, perc_f, perc_j)
      else:
        self.match_state.set_state(MatchState.VICTORY)
        self.climax_sound.play()
        random.choice(self.victory_sounds).play()
        if self.winner == "f":
          self.f_wins += 1
          self.p_list.pf.wins += 1
          self.p_list.pj.losses += 1

          self.f_win_rects.append(self.win_rect.move(-(self.win_rect.width * 2) * self.f_wins - self.shadow_dist, -self.shadow_dist))
        else:
          self.j_wins += 1
          self.p_list.pj.wins += 1
          self.p_list.pf.losses += 1
          self.j_win_rects.append(self.win_rect.move((self.win_rect.width * 2) * self.j_wins - self.shadow_dist, -self.shadow_dist))
    
  def render_stuff(self, screen):
    self.game.render_stuff(screen, render_space = self.match_state.state == MatchState.RUNNING, render_keys = self.match_state.state != MatchState.NEW_OPPONENT)
    if self.match_state.state == MatchState.COUNTDOWN:
      self.counter.render(screen, str(self.match_state.state_timer)[:4])
      self.ready_text.render(screen, "READY?!?")
    if self.match_state.state == MatchState.WHEEL:
      self.wheel.render(screen)

    pygame.draw.rect(screen, GameColor.F.Med, self.top_rect_left)
    pygame.draw.rect(screen, GameColor.J.Med, self.top_rect_right)
    pygame.draw.rect(screen, GameColor.Shadow, self.bottom_rect)

    self.f_name_text.render(screen, self.p_list.pf.name, GameColor.lighten(self.p_list.pf.color))
    self.j_name_text.render(screen, self.p_list.pj.name, GameColor.lighten(self.p_list.pj.color))
    self.streak_text.render(screen, "streak:{0}".format(self.score_streak))

    if self.match_state.state == MatchState.NEW_OPPONENT:
      self.f_name_big_text.render(screen, self.p_list.pf.name, self.p_list.pf.color)
      self.j_name_big_text.render(screen, self.p_list.pj.name, self.p_list.pj.color)
      self.vs_text.render(screen, "VS")

      self.big_f.down = self.keys.f
      self.big_j.down = self.keys.j
      self.big_f.render(screen, self.big_f_agree)
      self.big_j.render(screen, self.big_j_agree)

    if self.match_state.state == MatchState.WINNER:
      self.f_win_loss_text.render(screen, "WIN" if self.winner == "f" else "LOSE")
      self.j_win_loss_text.render(screen, "WIN" if self.winner == "j" else "LOSE")

      self.f_plus_minus_text.render(screen, "+{0}".format(self.score_streak) if self.winner == "f" else "")
      self.j_plus_minus_text.render(screen, "+1" if self.winner == "j" else "")

    for rect in self.win_rect_shadows: pygame.draw.rect(screen, GameColor.Shadow, rect)
    for rect in self.f_win_rects: pygame.draw.rect(screen, GameColor.F.Light, rect)
    for rect in self.j_win_rects: pygame.draw.rect(screen, GameColor.J.Light, rect)

    self.hud.render_stuff(screen, self.game.timer, self.game.perc_f, self.game.perc_j, render_percs = self.match_state.state in {MatchState.RUNNING, MatchState.WHEEL})

    if self.match_state.state == MatchState.PLAYER_LIST:
      self.p_list.render_stuff(screen)

    if (not (self.match_state.state in {MatchState.PLAYER_LIST, MatchState.RUNNING})) and self.keys.tab:
      self.scoreboard.render_stuff(screen)