import logging
import pygame
from pygame.locals import *
from textRenderer import TextRenderer

class Scoreboard:
  def __init__(self, rect, shadow_dist, sys_font, p_list):
    self.rect = rect
    self.shadow_dist = shadow_dist
    self.sys_font = sys_font
    self.p_list = p_list

    self.background = pygame.Surface(rect.size, pygame.SRCALPHA)
    self.background.fill((0, 0, 0, 150))

    self.text = TextRenderer(sys_font, 2, (0, 0), shadow_dist)

  def to_center(self, top_left, text):
    return (top_left[0] + self.sys_font.size(text)[0], top_left[1] + self.sys_font.size(text)[1])

  def render_stuff(self, screen):
    # TODO this is awful
    p_list = self.p_list.list.copy()
    p_list.sort(key = lambda p: p.losses)
    p_list.sort(key = lambda p: p.wins, reverse = True)
    p_list.sort(key = lambda p: p.score, reverse = True)

    screen.blit(self.background, self.rect.topleft)

    name_size = self.sys_font.size("AAAAAAAAAA")
    num_dist = self.sys_font.size("AAAA")[0]

    # name
    self.text.center = self.to_center((self.rect.left, self.rect.top), "NAME")
    self.text.render(screen, "NAME")

    # score
    self.text.center = self.to_center((self.rect.left + name_size[0] + num_dist, self.rect.top), "S")
    self.text.render(screen, "S")

    # wins
    self.text.center = self.to_center((self.rect.left + name_size[0] + num_dist * 2, self.rect.top), "W")
    self.text.render(screen, "W")

    # losses
    self.text.center = self.to_center((self.rect.left + name_size[0] + num_dist * 3, self.rect.top), "L")
    self.text.render(screen, "L")

    for idx, player in enumerate(p_list):
      # name
      self.text.center = self.to_center((self.rect.left, self.rect.top + name_size[1] * (idx + 1) * 2), player.name)
      self.text.render(screen, player.name)

      # score
      self.text.center = self.to_center((self.rect.left + name_size[0] + num_dist, self.rect.top + name_size[1] * (idx + 1) * 2), str(player.score))
      self.text.render(screen, str(player.score))

      # wins
      self.text.center = self.to_center((self.rect.left + name_size[0] + num_dist * 2, self.rect.top + name_size[1] * (idx + 1) * 2), str(player.wins))
      self.text.render(screen, str(player.wins))

      # losses
      self.text.center = self.to_center((self.rect.left + name_size[0] + num_dist * 3, self.rect.top + name_size[1] * (idx + 1) * 2), str(player.losses))
      self.text.render(screen, str(player.losses))