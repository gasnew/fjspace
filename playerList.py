import logging
import random
import pygame
from pygame.locals import *
from gameColor import GameColor
from textRenderer import TextRenderer
from shadowedPressable import ShadowedPressable

class Entry:
    @property
    def font_size(self):
      return (self.sys_font.size(self.name)[0] * 4, self.sys_font.size(self.name)[1] * 4)

    @property
    def top_left(self):
      return (self.text.center[0] - self.font_size[0] / 2, self.text.center[1] - self.font_size[1] / 2)
    @top_left.setter
    def top_left(self, val):
      self.text.center = (val[0] + self.font_size[0] / 2, val[1] + self.font_size[1] / 2)

    def __init__(self, sys_font, shadow_dist, name, color = None):
      self.sys_font = sys_font
      self.shadow_dist = shadow_dist
      self.name = name
      self.color = color

      self.score = 0
      self.wins = 0
      self.losses = 0

      self.text = TextRenderer(sys_font, 4, (0, 0), shadow_dist)

    def render(self, screen):
      self.text.render(screen, self.name)

class PlayerList:
  DEFAULT_NAMES = ["FRAN", "JAN", "STEVE", "WARBUCKS", "OLAF", "EVE", "ALICE", "WIZARD"]

  def __init__(self, rect, shadow_dist, sys_font):
    self.rect = rect
    self.sys_font = sys_font
    self.shadow_dist = shadow_dist

    self.in_focus = False

    # render stuff
    edge_buffer = rect.width * 0.05
    self.rect_edge_buffer = rect.width * 0.01
    max_text_size = (sys_font.size("AAAAAAAA")[0] * 4, sys_font.size("AAAAAAAA")[1] * 4)
    player_rect_width = max_text_size[0] + self.rect_edge_buffer * 2

    self.background = pygame.Surface(rect.size, pygame.SRCALPHA)
    self.background.fill((0, 0, 0, 100))
    self.bounding_rect = pygame.Rect((edge_buffer, edge_buffer * 2), (self.background.get_width() - edge_buffer * 2, self.background.get_height() - edge_buffer * 3))
    self.player_rect = pygame.Rect((self.bounding_rect.centerx - player_rect_width / 2, self.bounding_rect.top), (player_rect_width, max_text_size[1]))

    self.title_text = TextRenderer(sys_font, 2, (rect.centerx, rect.top + max_text_size[1] / 2), shadow_dist)

    plus_text, plus_text_shadow = ShadowedPressable.make_pressable_key("[+] to add", sys_font, 1)
    self.plus_text = ShadowedPressable(plus_text.convert_alpha(), plus_text_shadow, (rect.centerx * 1.75, rect.height * 0.45), shadow_dist / 2)
    minus_text, minus_text_shadow = ShadowedPressable.make_pressable_key("[-] to subtract", sys_font, 1)
    self.minus_text = ShadowedPressable(minus_text.convert_alpha(), minus_text_shadow, (rect.centerx * 1.75, rect.height * 0.5), shadow_dist / 2)
    enter_text, enter_text_shadow = ShadowedPressable.make_pressable_key("[ENTER] to proceed", sys_font, 1)
    self.enter_text = ShadowedPressable(enter_text.convert_alpha(), enter_text_shadow, (rect.centerx * 1.75, rect.height * 0.6), shadow_dist / 2)

    # list stuff
    self.list = []
    self.addEntry()
    self.addEntry()
    self.selected = self.list[0]

    # sound stuff
    self.press_sound = pygame.mixer.Sound("SFX/press_soft.wav")
    self.release_sound = pygame.mixer.Sound("SFX/release.wav")

    # outward facing stuff
    self.pf = self.list[0]
    self.pj = self.list[1]

  def p_list_stuff(self, plus, minus):
    self.plus_text.down = plus
    self.minus_text.down = minus

  def focus(self):
    self.in_focus = True
    self.selected = self.list[0]

  def defocus(self):
    self.in_focus = False

  def addEntry(self, name = None):
    if name is None:
      unique_names = [name for name in PlayerList.DEFAULT_NAMES if name not in [p.name for p in self.list]]      
      name = random.choice(unique_names) if len(unique_names) > 0 else random.choice(PlayerList.DEFAULT_NAMES)

    unique_colors = [color for color in GameColor.PlayerColors if color not in [p.color for p in self.list]]
    color = random.choice(unique_colors) if len(unique_colors) > 0 else random.choice(GameColor.PlayerColors)

    self.list.append(Entry(self.sys_font, self.shadow_dist, name, color = color))
    self.selected = self.list[-1]

  def removeEntry(self, idx):
    del self.list[idx]
    self.selected = self.list[idx] if idx < len(self.list) else self.list[-1]

  def input(self, char):
    if self.in_focus:
      # edit name
      if 97 <= char <= 122 and len(self.selected.name) < 8:
        self.selected.name += chr(char - 32)
        self.press_sound.play()
      elif char == 8: # bs
        self.selected.name = self.selected.name[:-1]
        self.release_sound.play()

      # change selected
      if char == 273 or char == 274:
        dir = -1 if char == 273 else 1
        idx = self.list.index(self.selected) + dir 
        self.selected = self.list[idx % len(self.list)]

      # add/remove names
      if char == 61: # +
        self.addEntry()
      elif char == 45: # -
        if self.selected not in {self.pf, self.pj}:
          self.removeEntry(self.list.index(self.selected))

  def shuffle(self):
    random.shuffle(self.list)
    self.pf = self.list[0]
    self.pj = self.list[1]

  def swap_players(self):
    p_temp = self.pf
    self.pf = self.pj
    self.pj = p_temp

  def new_opponent(self):
    self.list.remove(self.pj)
    self.list.append(self.pj)
    self.pj = self.list[1]

  def render_stuff(self, screen): 
    # render background
    screen.blit(self.background, self.rect.topleft)

    # render players
    dist = (self.bounding_rect.height - self.player_rect.height) / (len(self.list) - 1)
    self.player_rect.top = self.bounding_rect.top
    for player in self.list:
      # draw rect
      pygame.draw.rect(screen, player.color, self.player_rect)

      # draw text
      player.top_left = (self.player_rect.topleft[0] + self.rect_edge_buffer, self.player_rect.topleft[1])
      player.render(screen)

      # move rect for next iteration
      self.player_rect.move_ip(0, dist)

    # render selected again
    self.player_rect.top = self.selected.top_left[1]
    self.player_rect.move_ip(self.shadow_dist * 2, self.shadow_dist * 2)
    pygame.draw.rect(screen, GameColor.Shadow, self.player_rect)
    self.player_rect.move_ip(-self.shadow_dist * 2, -self.shadow_dist * 2)
    pygame.draw.rect(screen, self.selected.color, self.player_rect)
    self.selected.render(screen)

    # title text
    self.title_text.render(screen, "PLAYERS")
    self.plus_text.render(screen)
    self.minus_text.render(screen)
    self.enter_text.render(screen)
