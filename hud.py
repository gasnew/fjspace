import logging
from textRenderer import TextRenderer

class Hud:
  def __init__(self, top_rect, bottom_rect, shadow_dist, sys_font, l_color, r_color):
    self.top_rect = top_rect
    self.bottom_rect = bottom_rect
    self.shadow_dist = shadow_dist

    self.timer_text = TextRenderer(sys_font, 2, (top_rect.centerx, top_rect.bottom - top_rect.height * 0.2), shadow_dist)
    self.perc_f_text = TextRenderer(sys_font, 4, (top_rect.width / 4, top_rect.centery), shadow_dist, color = l_color)
    self.perc_j_text = TextRenderer(sys_font, 4, (top_rect.width * 3 / 4, top_rect.centery), shadow_dist, color = r_color)

  def hud_stuff(self):
    pass

  def render_stuff(self, screen, timer, perc_f, perc_j, render_percs = False):
    # timer
    timer_str = str(timer).split('.')
    if len(timer_str) == 1: timer_str = [timer_str[0], "00"]
    timer_str = timer_str[0].zfill(2) + ':' + (timer_str[1].zfill(2))[:2]
    self.timer_text.render(screen, timer_str)

    # percentage
    if render_percs:
      perc_f_str = str(round(perc_f * 100)).split('.')[0] + '%'
      self.perc_f_text.render(screen, perc_f_str)
      perc_j_str = str(round(perc_j * 100)).split('.')[0] + '%'
      self.perc_j_text.render(screen, perc_j_str)
