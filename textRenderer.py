import logging
from shadowedPressable import ShadowedPressable

class TextRenderer:
  def __init__(self, font, scale, center, shadow_dist, color = (255, 255, 255)):
    self.font = font
    self.scale = scale
    self.center = center
    self.shadow_dist = shadow_dist
    self.color = color

  def render(self, target, string):
    text, shadow = ShadowedPressable.make_pressable_key(string, self.font, self.scale, color = self.color)
    ShadowedPressable(text, shadow, self.center, self.shadow_dist).render(target)
