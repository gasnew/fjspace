import logging
import pygame
from pygame.locals import *
from textRenderer import TextRenderer

class Entry:
    @property
    def font_size(self):
      return (self.sys_font.size(self.name)[0] * 4, self.sys_font.size(self.name)[1] * 4)

    @property
    def top_left(self):
      return (self.text.center[0] - self.font_size[0] / 2, self.text.center[1] - self.font_size[1] / 2)

    def __init__(self, sys_font, shadow_dist, name, center = (0, 0)):
      self.sys_font = sys_font
      self.shadow_dist = shadow_dist
      self.name = name

      self.score = 0
      self.wins = 0
      self.losses = 0

      self.text = TextRenderer(sys_font, 4, center, shadow_dist)

    def render(self, screen):
      self.text.render(screen, self.name)

class PlayerList:
  def __init__(self, rect, shadow_dist, sys_font):
    self.rect = rect
    self.sys_font = sys_font
    self.shadow_dist = shadow_dist

    self.in_focus = False

    # list stuff
    self.list = []
    self.addEntry("FRAN")
    self.addEntry("JAN")
    self.selected = self.list[0]

    # outward facing stuff
    self.pf = self.list[0]
    self.pj = self.list[1]

    # render stuff
    self.background = pygame.Surface(rect.size, pygame.SRCALPHA)
    self.background.fill((0, 0, 0, 50))
    self.select_rect = pygame.Surface(self.selected.font_size, pygame.SRCALPHA)
    self.select_rect.fill((0, 0, 0, 150))

  def p_list_stuff(self):
    pass

  def focus(self):
    self.in_focus = True
    self.selected = self.list[0]

  def defocus(self):
    self.in_focus = False

  def addEntry(self, name = "AAA"):
    self.list.append(Entry(self.sys_font, self.shadow_dist, name))
    self.selected = self.list[-1]
    self.place_entries()

  def removeEntry(self, idx):
    del self.list[idx]
    self.selected = self.list[idx] if idx < len(self.list) else self.list[-1]
    self.place_entries()

  def place_entries(self):
    dist = self.rect.height / len(self.list)
    for idx, player in enumerate(self.list):
      player.text.center = (self.rect.centerx, self.rect.top + idx * dist + dist / 2)

  def input(self, char):
    if self.in_focus:
      # edit name
      if 97 <= char <= 122 and len(self.selected.name) < 8:
        self.selected.name += chr(char - 32)
      elif char == 8: # bs
        self.selected.name = self.selected.name[:-1]

      # change selected
      if char == 273 or char == 274:
        dir = -1 if char == 273 else 1
        idx = self.list.index(self.selected) + dir 
        self.selected = self.list[idx % len(self.list)]

      # add/remove names
      if char == 61: # +
        self.addEntry()
      elif char == 45 and len(self.list) > 2: # -
        self.removeEntry(self.list.index(self.selected))

    logging.debug(char)

  def swap_players(self):
    p_temp = self.pf
    self.pf = self.pj
    self.pj = p_temp

  def new_opponent(self):
    self.list.remove(self.pj)
    self.list.append(self.pj)
    self.pj = self.list[1]

  def render_stuff(self, screen): 
    screen.blit(self.background, self.rect.topleft)
    # screen.blit(self.select_rect, self.selected.top_left)
    pygame.draw.rect(screen, (0, 0, 0), Rect(self.selected.top_left, self.selected.font_size))

    for player in self.list:
      player.render(screen)