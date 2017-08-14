from pygame.locals import *

class Keys:
  def __init__(self):
    self.f = self.j = self.s = 0

  def update(self, events):
    for event in events:
      if event.key == 102: 
        self.f = event.type == KEYDOWN
      elif event.key == 106: 
        self.j = event.type == KEYDOWN
      elif event.key == 32: 
        self.s = event.type == KEYDOWN
  