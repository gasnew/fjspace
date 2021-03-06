import logging
import pygame
from pygame.locals import *
from textRenderer import TextRenderer
from gameColor import GameColor

class Scoreboard:
  def __init__(self, rect, shadow_dist, sys_font, p_list):
    self.rect = rect
    self.shadow_dist = shadow_dist
    self.sys_font = sys_font
    self.p_list = p_list

    self.background = pygame.Surface(rect.size, pygame.SRCALPHA)
    self.background.fill((0, 0, 0, 150))

    self.edge_buffer = rect.height / 20

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

    name_size = self.sys_font.size("AAAAAAAAAAAAAA")
    num_dist = self.sys_font.size("AAAA")[0]

    # name
    self.text.center = self.to_center((self.rect.left + self.edge_buffer, self.rect.top + self.edge_buffer), "NAME")
    self.text.render(screen, "NAME")

    # score
    self.text.center = self.to_center((self.rect.left + self.edge_buffer + name_size[0] + num_dist, self.rect.top + self.edge_buffer), "S")
    self.text.render(screen, "S")

    # wins
    self.text.center = self.to_center((self.rect.left + self.edge_buffer + name_size[0] + num_dist * 2, self.rect.top + self.edge_buffer), "W")
    self.text.render(screen, "W")

    # losses
    self.text.center = self.to_center((self.rect.left + self.edge_buffer + name_size[0] + num_dist * 3, self.rect.top + self.edge_buffer), "L")
    self.text.render(screen, "L")

    for idx, player in enumerate(p_list):
      # name
      self.text.center = self.to_center((self.rect.left + self.edge_buffer, self.rect.top + self.edge_buffer + name_size[1] * (idx + 1) * 2), player.name)
      self.text.render(screen, player.name, GameColor.lighten(player.color))

      # score
      self.text.center = self.to_center((self.rect.left + self.edge_buffer + name_size[0] + num_dist, self.rect.top + self.edge_buffer + name_size[1] * (idx + 1) * 2), str(player.score))
      self.text.render(screen, str(player.score), GameColor.lighten(player.color))

      # wins
      self.text.center = self.to_center((self.rect.left + self.edge_buffer + name_size[0] + num_dist * 2, self.rect.top + self.edge_buffer + name_size[1] * (idx + 1) * 2), str(player.wins))
      self.text.render(screen, str(player.wins), GameColor.lighten(player.color))

      # losses
      self.text.center = self.to_center((self.rect.left + self.edge_buffer + name_size[0] + num_dist * 3, self.rect.top + self.edge_buffer + name_size[1] * (idx + 1) * 2), str(player.losses))
      self.text.render(screen, str(player.losses), GameColor.lighten(player.color))