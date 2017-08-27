import logging
import pygame
from pygame.locals import *
from math import *
import random
from gameColor import GameColor

class Wheel:
  RES = 32
  SIZE = (RES, RES) # a 64 x 64 wheel
  ANGLE_INTERVAL = 0.001 # percent-wheel interval for rendering wedges
  REVOLUTIONS = 4 # number of time the arm goes around the wheel before stopping

  def __init__(self, game_rect, shadow_dist, sys_font):
    self.game_rect = game_rect
    self.shadow_dist = shadow_dist
    self.sys_font = sys_font

    # placement
    self.rect = Rect((0, 0), (game_rect.width / 8, game_rect.width / 8))
    self.rect.center = (game_rect.centerx, game_rect.top + game_rect.height * 0.3)

    self.reset()

    self.start(2, 0.5, 0.5)

  def reset(self):
    self.spin_time = 2
    self.pf = self.pj = 0.5
    self.winning_angle = self.arm_angle = self.prev_arm_angle = self.arm_v0 = self.t_elapsed = 0.0

  def start(self, spin_time, pf, pj):
    self.reset()

    self.spin_time = spin_time
    self.pf = pf
    self.pj = pj

    self.winning_angle = random.random()
    final_angle = self.winning_angle + Wheel.REVOLUTIONS
    self.arm_v0 = 2 * final_angle / spin_time

  def wheel_stuff(self, delta_t):
    self.t_elapsed += (delta_t / 1000)
    self.prev_arm_angle = self.arm_angle
    self.arm_angle = self.arm_v0 * self.t_elapsed + 1/2 * (-self.arm_v0 / self.spin_time) * self.t_elapsed**2

    return (self.t_elapsed >= self.spin_time, "f" if self.winning_angle < self.pf else "j")

  def render(self, screen):
    # get surface
    shadow_surface = pygame.Surface(Wheel.SIZE, pygame.SRCALPHA).convert_alpha()
    surface = pygame.Surface(Wheel.SIZE, pygame.SRCALPHA).convert_alpha()
    
    # draw wedges  
    pygame.draw.polygon(shadow_surface, GameColor.Shadow, self.make_wedge(0.0, self.pf))
    pygame.draw.polygon(shadow_surface, GameColor.Shadow, self.make_wedge(self.pf, 1.0))
    pygame.draw.polygon(surface, GameColor.F.Med, self.make_wedge(0.0, self.pf))
    pygame.draw.polygon(surface, GameColor.J.Med, self.make_wedge(self.pf, 1.0))

    # draw hand
    try:
      mag = Wheel.RES / 2
      pygame.draw.polygon(surface, GameColor.Shadow, self.make_wedge(self.prev_arm_angle, self.arm_angle))
      pygame.draw.polygon(surface, GameColor.Shadow, self.make_wedge(self.prev_arm_angle, self.arm_angle), 2)
    except:
      logging.debug("ERROR")

    # scale and blit to screen
    shadow_surface = pygame.transform.scale(shadow_surface, self.rect.size)
    surface = pygame.transform.scale(surface, self.rect.size)
    screen.blit(shadow_surface, (self.rect.left + self.shadow_dist, self.rect.top + self.shadow_dist))
    screen.blit(surface, self.rect.topleft)

  def make_wedge(self, a1, a2):
    mag = Wheel.RES / 2
    center = (Wheel.RES / 2, Wheel.RES / 2)
    points = [center]

    a = a1
    while a <= a2:
      points.append((center[0] + -mag * sin(2 * pi * a), center[1] + -mag * cos(2 * pi * a)))
      a += Wheel.ANGLE_INTERVAL

    points.append(center) # must be at least 3 points long
    return points
