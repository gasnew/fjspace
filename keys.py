import logging
from pygame.locals import *

class Keys:
  def __init__(self):
    self.f = self.j = self.s = self.enter = self.tab = 0

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

      if event.type == KEYDOWN:
        callback(event.key)
  