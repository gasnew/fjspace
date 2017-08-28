import logging
import pygame
from pygame.locals import *
from math import *
import random
from textRenderer import TextRenderer
from gameColor import GameColor
from tweener import Tweener

class Wheel:
  RES = 32
  SIZE = (RES, RES) # a 64 x 64 wheel
  ANGLE_INTERVAL = 0.001 # percent-wheel interval for rendering wedges
  REVOLUTIONS = 4 # number of times the arm goes around the wheel before stopping
  HIGHLIGHT_TIME = 0.3 # period of flashing

  def __init__(self, game_rect, shadow_dist, sys_font):
    self.game_rect = game_rect
    self.shadow_dist = shadow_dist
    self.sys_font = sys_font

    # placement
    self.rect = Rect((0, 0), (game_rect.width / 8, game_rect.width / 8))
    self.rect.center = (game_rect.centerx, game_rect.top + game_rect.height * 0.3)

    # text
    self.pf_text = TextRenderer(sys_font, 2, (0, 0), shadow_dist, color = GameColor.F.Med)
    self.pj_text = TextRenderer(sys_font, 2, (0, 0), shadow_dist, color = GameColor.J.Med)

    # tweening
    self.pf_tweener = Tweener({"start": 0})
    self.pj_tweener = Tweener({"start": 0})
    self.highlight_timer = 0

    self.reset()

    self.start(2, 0.5, 0.5)

  def reset(self):
    self.spin_time = 2
    self.pf = self.pj = 0.5
    self.winning_angle = self.arm_angle = self.prev_arm_angle = self.arm_v0 = self.t_elapsed = 0.0
    self.winner = ""
    self.pf_tweener.set_to("start")
    self.pj_tweener.set_to("start")

  def start(self, spin_time, pf, pj):
    self.reset()

    self.spin_time = spin_time
    self.pf = pf
    self.pj = pj

    self.winning_angle = random.random()
    final_angle = self.winning_angle + Wheel.REVOLUTIONS
    self.arm_v0 = 2 * final_angle / spin_time

    self.pf_tweener.set_to("start").tween_to(self.pf)
    self.pj_tweener.set_to("start").tween_to(1)

  def wheel_stuff(self, delta_t):
    self.t_elapsed += (delta_t / 1000)

    self.pf_tweener.tween_stuff(delta_t)
    self.pj_tweener.tween_stuff(delta_t)

    if self.t_elapsed <= self.spin_time:
      self.prev_arm_angle = self.arm_angle
      self.arm_angle = self.arm_v0 * self.t_elapsed + 1/2 * (-self.arm_v0 / self.spin_time) * self.t_elapsed**2

      self.highlight_timer = 0
    else:
      self.prev_arm_angle = self.arm_angle = self.winning_angle

      self.highlight_timer = self.highlight_timer - (delta_t / (self.HIGHLIGHT_TIME * 1000)) if self.highlight_timer > 0 else 1

    game_over, self.winner = (self.t_elapsed >= self.spin_time, "f" if self.winning_angle < self.pf else "j")
    return game_over, self.winner

  def render(self, screen):
    # get surface
    shadow_surface = pygame.Surface(Wheel.SIZE, pygame.SRCALPHA).convert_alpha()
    surface = pygame.Surface(Wheel.SIZE, pygame.SRCALPHA).convert_alpha()
    
    # draw wedges  
    a = self.pf_tweener.tweened_val
    b = self.pj_tweener.tweened_val
    pygame.draw.polygon(shadow_surface, GameColor.Shadow, self.make_wedge(0.0, a))
    pygame.draw.polygon(shadow_surface, GameColor.Shadow, self.make_wedge(a, b))

    f_color = GameColor.White if self.winner == "f" and round(self.highlight_timer) == 1 else GameColor.F.Med
    j_color = GameColor.White if self.winner == "j" and round(self.highlight_timer) == 1 else GameColor.J.Med
    pygame.draw.polygon(surface, f_color, self.make_wedge(0.0, a))
    pygame.draw.polygon(surface, j_color, self.make_wedge(a, b))

    # draw hand
    mag = Wheel.RES / 2
    pygame.draw.polygon(surface, GameColor.Shadow, self.make_wedge(self.prev_arm_angle, self.arm_angle))
    pygame.draw.polygon(surface, GameColor.Shadow, self.make_wedge(self.prev_arm_angle, self.arm_angle), 2)

    # scale and blit to screen
    shadow_surface = pygame.transform.scale(shadow_surface, self.rect.size)
    surface = pygame.transform.scale(surface, self.rect.size)
    screen.blit(shadow_surface, (self.rect.left + self.shadow_dist, self.rect.top + self.shadow_dist))
    screen.blit(surface, self.rect.topleft)

    # render text
    pf_a = self.pf_tweener.tweened_val / 2
    self.pf_text.center = (self.rect.centerx + -self.rect.width * sin(2 * pi * pf_a), self.rect.centery + -self.rect.width * cos(2 * pi * pf_a))
    pf_str = str(round(self.pf_tweener.tweened_val * 100)).split('.')[0] + '%' 
    self.pf_text.render(screen, pf_str)
    
    pj_a = 1 - (self.pj_tweener.tweened_val - self.pf_tweener.tweened_val) / 2
    self.pj_text.center = (self.rect.centerx + -self.rect.width * sin(2 * pi * pj_a), self.rect.centery + -self.rect.width * cos(2 * pi * pj_a))
    pj_str = str(round((self.pj_tweener.tweened_val - self.pf_tweener.tweened_val) * 100)).split('.')[0] + '%'
    self.pj_text.render(screen, pj_str)

  def make_wedge(self, a1, a2):
    mag = Wheel.RES / 2
    center = (Wheel.RES / 2, Wheel.RES / 2)
    points = [center]

    a1, a2 = sorted([a1, a2])
    a = a1
    while a <= a2:
      points.append((center[0] + -mag * sin(2 * pi * a), center[1] + -mag * cos(2 * pi * a)))
      a += Wheel.ANGLE_INTERVAL

    points.append(center) # must be at least 3 points long
    return points
