import logging
import pygame
from pygame.locals import *
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

  @property
  def down(self):
    return self._down
  @down.setter
  def down(self, val):
    if not self.down and val: self.press_sound.play()
    elif self.down and not val: self.release_sound.play()
    self._down = val

  def __init__(self, surface, shadow, center, shadow_dist):
    self.surface = surface
    self.shadow = shadow
    self.center = center
    self.shadow_dist = shadow_dist

    self._down = False

    self.cover = pygame.Surface((self.surface.get_width(), self.surface.get_height())).convert_alpha()
    self.cover.fill(GameColor.Space.Down)

    self.press_sound = pygame.mixer.Sound("SFX/press.wav")
    self.release_sound = pygame.mixer.Sound("SFX/release.wav")

  def render(self, target, cooldown = 0, cover = False):
    if self.down:
      target.blit(self.surface, self.top_left)
    else:
      target.blit(self.shadow, self.top_left)
      target.blit(self.surface, tuple(coord - self.shadow_dist for coord in self.top_left))

    # render mask
    if cooldown > 0 or cover:
      cover_size = cooldown if cooldown > 0 else 1
      disp = 0 if self.down else self.shadow_dist

      cover_masked = pygame.transform.scale(self.cover.copy(), (self.cover.get_width(), int(self.cover.get_height() * cover_size)))
      cover_masked.blit(self.surface, (0, 0), special_flags = BLEND_RGBA_MULT)
      target.blit(cover_masked, (self.top_left[0] - disp, self.top_left[1] - disp))
