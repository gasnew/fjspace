import logging
from pygame.locals import *

class Keys:
  def __init__(self):
    self.f = self.j = self.s = self.enter = self.tab = self.alt = self.f4 = self.f11_toggle = 0

  def update(self, events, callback = lambda *args: None):
    for event in events:
      if event.key == 102: 
        self.f = event.type == KEYDOWN
      elif event.key == 106: 
        self.j = event.type == KEYDOWN
      elif event.key == 32: 
        self.s = event.type == KEYDOWN
      elif event.key == 13:
        self.enter = event.type == KEYDOWN
      elif event.key == 9:
        self.tab = event.type == KEYDOWN
      elif event.key == 308:
        self.alt = event.type == KEYDOWN
      elif event.key == 285:
        self.f4 = event.type == KEYDOWN
      elif event.key == 292:
        self.f11_toggle = (not self.f11_toggle) if event.type == KEYDOWN else self.f11_toggle

      if event.type == KEYDOWN:
        callback(event.key)
  