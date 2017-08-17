import logging
import pygame
from gameColor import GameColor

class ShadowedPressable:
  def make_pressable_key(string, font, scale, color = GameColor.White):
    text = font.render(string, 0, color)
    text = pygame.transform.scale(text, (text.get_width() * scale, text.get_height() * scale))
    text_shadow = font.render(string, 0, GameColor.Shadow)
    text_shadow = pygame.transform.scale(text_shadow, (text_shadow.get_width() * scale, text_shadow.get_height() * scale))

    return text, text_shadow

  @property
  def top_left(self):
    return (self.center[0] - self.surface.get_width() / 2, self.center[1] - self.surface.get_height() / 2)

  def __init__(self, surface, shadow, center, shadow_dist):
    self.surface = surface
    self.shadow = shadow
    self.center = center
    self.shadow_dist = shadow_dist

    self.down = False

  def render(self, target):
    if self.down:
      target.blit(self.surface, self.top_left)
    else:
      target.blit(self.shadow, self.top_left)
      target.blit(self.surface, tuple(coord - self.shadow_dist for coord in self.top_left))
