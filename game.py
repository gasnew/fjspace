# important things
import logging, sys
import random, math
import pygame
from pygame.locals import *
from gameColor import GameColor
from shadowedPressable import *
from textRenderer import TextRenderer

class Game:
  def __init__(self, WIN_TIME, COOLDOWN_TIME, STALE_TIME, TOTAL_TIME, FAILURE_TIME, keys, game_rect, shadow_dist, sys_font):
    # -- CONSTANTS --
    self.WIN_TIME = WIN_TIME
    self.COOLDOWN_TIME = COOLDOWN_TIME
    self.STALE_TIME = STALE_TIME
    self.TOTAL_TIME = TOTAL_TIME
    self.FAILURE_TIME = FAILURE_TIME

    # -- CONTROLS --
    self.keys = keys

    # -- VISUAL PARAMS --
    # rectangles and placement
    self.game_rect = game_rect
    self.game_rect_left = pygame.Rect(0, game_rect.top, game_rect.width / 2, game_rect.height)
    self.game_rect_right = pygame.Rect(game_rect.width / 2, game_rect.top, game_rect.width / 2, game_rect.height)

    self.shadow_dist = shadow_dist
    self.bar_width = game_rect.width * 0.2
    self.bar_x_offset = game_rect.width / 2 * 0.5

    self.bf_rect = pygame.Rect(0, game_rect.bottom, self.bar_width, 0)
    self.bf_rect.centerx = game_rect.width / 2 - self.bar_x_offset
    self.bj_rect = self.bf_rect.copy()
    self.bj_rect.centerx = game_rect.width / 2 + self.bar_x_offset

    # colors
    self.f_background_color = Color(*GameColor.F.Light)
    self.fbc = Color(self.f_background_color.r, self.f_background_color.g, self.f_background_color.b)
    self.j_background_color = Color(*GameColor.J.Light)
    self.jbc = Color(self.j_background_color.r, self.j_background_color.g, self.j_background_color.b)

    # pressables
    f_text, f_text_shadow = ShadowedPressable.make_pressable_key("[F]", sys_font, 2)
    self.f_text = ShadowedPressable(f_text, f_text_shadow, (self.bf_rect.centerx, self.bf_rect.centery - f_text.get_height()), shadow_dist)

    j_text, j_text_shadow = ShadowedPressable.make_pressable_key("[J]", sys_font, 2)
    self.j_text = ShadowedPressable(j_text, j_text_shadow, (self.bj_rect.centerx, self.bj_rect.centery - j_text.get_height()), shadow_dist)

    space_text, space_text_shadow = ShadowedPressable.make_pressable_key("[SPACE]", sys_font, 4)
    space_text = pygame.transform.rotate(space_text, 90).convert_alpha()
    space_text_shadow = pygame.transform.rotate(space_text_shadow, 90).convert_alpha()
    self.space_text = ShadowedPressable(space_text, space_text_shadow, (game_rect.width / 2, game_rect.height * 0.8), shadow_dist)

    # text
    self.big_timer = TextRenderer(sys_font, 4, game_rect.center, shadow_dist)

    # sound
    self.spaced_sound = pygame.mixer.Sound("SFX/spaced.wav")
    self.inc_sounds = [pygame.mixer.Sound("SFX/inc{0}.wav".format(i)) for i in range(13)]
    self.timer_sound = pygame.mixer.Sound("SFX/beep.wav")

    # -- GAMEPLAY --
    self.reset()
    
  def game_stuff(self, delta_t):
    # mechanics stuff
    self.cooldown = self.cooldown - (delta_t / (self.COOLDOWN_TIME * 1000)) if self.cooldown > 0 else 0
    if self.keys.s and self.cooldown == 0: self.stale_timer = self.stale_timer - (delta_t / 1000) if self.stale_timer > 0 else 0
    self.timer = self.timer - (delta_t / 1000) if self.timer > 0 else 0
    if self.bf + self.bj == 0:
      self.perc_f = self.perc_j = 0.5
    else:
      self.perc_f = self.bf / (self.bf + self.bj) 
      self.perc_j = self.bj / (self.bf + self.bj)
    self.f_spaced = self.f_spaced - (delta_t / (self.FAILURE_TIME * 1000)) if self.f_spaced > 0 else 0
    self.j_spaced = self.j_spaced - (delta_t / (self.FAILURE_TIME * 1000)) if self.j_spaced > 0 else 0

    f, j, s = self.keys.f, self.keys.j, self.keys.s
    if f:
      if s and self.cooldown == 0:
        self.bf = 0
        self.f_spaced = 1
        self.spaced_sound.play()
      else: 
        self.bf += delta_t / (self.WIN_TIME * 1000)
    if j:
      if s and self.cooldown == 0:
        self.bj = 0
        self.j_spaced = 1
        self.spaced_sound.play()
      else:
        self.bj += delta_t / (self.WIN_TIME * 1000)

    if s and (f or j) and self.cooldown == 0:
      self.cooldown = 1
    elif not s or self.cooldown != 0:
      self.stale_timer = min([self.STALE_TIME, self.timer])

    # sound
    if self.stale_timer < 3:
      if self.stale_timer_channel is None:
        self.stale_timer_channel = self.timer_sound.play(loops = 2)
    elif self.stale_timer_channel is not None:
      self.stale_timer_channel.stop()
      self.stale_timer_channel = None
    
    # returns
    game_over = self.bf >= 1 or self.bj >= 1 or self.timer == 0 or self.stale_timer == 0
    winner = "j"
    if self.timer == 0 or self.stale_timer == 0: winner = "stale"
    elif self.bf > self.bj: winner = "f"

    return game_over, winner, self.perc_f, self.perc_j

  def reset(self):
    self.bf = self.bj = 0
    self.cooldown = 0
    self.f_spaced = self.j_spaced = 0
    self.stale_timer = self.STALE_TIME
    self.timer = self.TOTAL_TIME
    self.perc_f = self.perc_j = 0
    # self.f_inc_channel = self.j_inc_channel = None
    self.stale_timer_channel = None

  def render_stuff(self, screen, render_space = True, render_keys = True, disable_keys = False):
    # background rendering
    hsva = self.f_background_color.hsva
    self.fbc.hsva = (hsva[0], hsva[1], hsva[2] + (100 - hsva[2]) * self.f_spaced, hsva[3])
    pygame.draw.rect(screen, (self.fbc.r, self.fbc.g, self.fbc.b), self.game_rect_left)

    hsva = self.j_background_color.hsva
    self.jbc.hsva = (hsva[0], hsva[1], hsva[2] + (100 - hsva[2]) * self.j_spaced, hsva[3])
    pygame.draw.rect(screen, (self.jbc.r, self.jbc.g, self.jbc.b), self.game_rect_right)

    # bars rendering
    self.bf_rect.height = -self.game_rect.height * self.bf
    pygame.draw.rect(screen, GameColor.F.Dark, self.bf_rect)
    self.bj_rect.height = -self.game_rect.height * self.bj
    pygame.draw.rect(screen, GameColor.J.Dark, self.bj_rect)

    # pressables rendering
    f, j, s = self.keys.f, self.keys.j, self.keys.s
    self.f_text.down = f if not disable_keys else False
    self.j_text.down = j if not disable_keys else False
    self.space_text.down = s or self.cooldown > 0
    if render_keys:
      self.f_text.render(screen)
      self.j_text.render(screen)

    if render_space:
      self.space_text.render(screen, self.cooldown, not f and not j)

      if self.stale_timer < 3:
        self.big_timer.render(screen, str(self.stale_timer)[:4])
