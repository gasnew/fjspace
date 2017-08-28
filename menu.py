import logging
import pygame
from pygame.locals import *
from gameColor import GameColor
from textRenderer import TextRenderer
from shadowedPressable import ShadowedPressable

class Item:
    @property
    def font_size(self):
      return (self.sys_font.size(self.title)[0] * 4, self.sys_font.size(self.title)[1] * 4)

    @property
    def top_left(self):
      return (self.title_text.center[0] - self.font_size[0] / 2, self.title_text.center[1] - self.font_size[1] / 2)
    @top_left.setter
    def top_left(self, val):
      self.title_text.center = (val[0] + self.font_size[0] / 2, val[1] + self.font_size[1] / 2)

    def __init__(self, sys_font, shadow_dist, key, title, hold_time, callback, color = None):
      self.sys_font = sys_font
      self.shadow_dist = shadow_dist
      self.title = title
      self.hold_time = hold_time
      self.callback = callback
      self.color = color

      self.hold_timer = 1

      key, key_shadow = ShadowedPressable.make_pressable_key(key, sys_font, 4)
      self.key_text = ShadowedPressable(key.convert_alpha(), key_shadow, (0, 0), shadow_dist)
      self.title_text = TextRenderer(sys_font, 4, (0, 0), shadow_dist)

    def item_stuff(self, delta_t, key):

      self.key_text.down = key

      if key: self.hold_timer = self.hold_timer - (delta_t / (self.hold_time * 1000)) if self.hold_timer > 0 else 0
      else: self.hold_timer = 1

      if self.hold_timer == 0:
        self.callback()
        self.hold_timer = 1
        
        return True

      return False

    def render(self, screen):
      self.key_text.center = (self.top_left[0], self.title_text.center[1])
      self.key_text.render(screen, self.hold_timer)
      
      self.title_text.center = (self.title_text.center[0] + self.font_size[1], self.title_text.center[1])
      self.title_text.render(screen, self.title)

class Menu:
  def __init__(self, rect, keys, shadow_dist, sys_font):
    self.rect = rect
    self.keys = keys
    self.sys_font = sys_font
    self.shadow_dist = shadow_dist

    self.in_focus = False

    # render stuff
    edge_buffer = rect.width * 0.05
    self.rect_edge_buffer = rect.width * 0.01
    max_text_size = (sys_font.size("AAAAAAAA")[0] * 4, sys_font.size("AAAAAAAA")[1] * 4)
    item_rect_width = max_text_size[0] + self.rect_edge_buffer * 2
    key_width = max_text_size[1]

    self.background = pygame.Surface(rect.size, pygame.SRCALPHA)
    self.background.fill((0, 0, 0, 150))
    self.bounding_rect = pygame.Rect((edge_buffer, edge_buffer), (self.background.get_width() - edge_buffer * 2, self.background.get_height() - edge_buffer * 2))
    self.item_rect = pygame.Rect((edge_buffer * 2, self.bounding_rect.top), (item_rect_width, max_text_size[1]))

    # list stuff
    self.list = []

  def menu_stuff(self, delta_t):
    if self.in_focus:
      for idx, item in enumerate(self.list):
        key = self.keys.nums[idx + 50]
        activated = item.item_stuff(delta_t, key)

        if activated: self.defocus()

  def focus(self):
    self.in_focus = True

  def defocus(self):
    self.in_focus = False

  def add_item(self, key, title, hold_time, callback):
    self.list.append(Item(self.sys_font, self.shadow_dist, key, title, hold_time, callback, color = GameColor.White))

  def remove_item(self, idx):
    del self.list[idx]

  def render_stuff(self, screen): 
    # render background
    screen.blit(self.background, self.rect.topleft)

    # render items
    dist = (self.bounding_rect.height - self.item_rect.height) / (len(self.list) - 1)
    self.item_rect.top = self.bounding_rect.top
    for item in self.list:
      # draw text
      item.top_left = (self.item_rect.topleft[0] + self.rect_edge_buffer, self.item_rect.topleft[1])
      item.render(screen)

      # move rect for next iteration
      self.item_rect.move_ip(0, dist)
