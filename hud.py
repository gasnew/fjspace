import logging
from gameColor import GameColor
from textRenderer import TextRenderer
from shadowedPressable import ShadowedPressable

class Hud:
  def __init__(self, top_rect, bottom_rect, shadow_dist, sys_font):
    self.top_rect = top_rect
    self.bottom_rect = bottom_rect
    self.shadow_dist = shadow_dist

    self.timer_text = TextRenderer(sys_font, 2, (top_rect.centerx, top_rect.bottom - top_rect.height * 0.2), shadow_dist / 2)
    self.perc_f_text = TextRenderer(sys_font, 4, (top_rect.width / 4, top_rect.centery), shadow_dist, color = GameColor.J.Med)
    self.perc_j_text = TextRenderer(sys_font, 4, (top_rect.width * 3 / 4, top_rect.centery), shadow_dist, color = GameColor.F.Med)

    menu_text, menu_text_shadow = ShadowedPressable.make_pressable_key("[1] menu", sys_font, 1, GameColor.F.Dark)
    self.menu_text = ShadowedPressable(menu_text.convert_alpha(), menu_text_shadow, (top_rect.width * 0.05, top_rect.height * 0.13), 0)

  def hud_stuff(self):
    pass

  def render_stuff(self, screen, timer, perc_f, perc_j, one_down, render_percs = False):
    # timer
    timer_str = str(timer).split('.')
    if len(timer_str) == 1: timer_str = [timer_str[0], "00"]
    timer_str = timer_str[0].zfill(2) + ':' + (timer_str[1].zfill(2))[:2]
    if timer == -1: timer_str = "Inf" 
    self.timer_text.render(screen, timer_str)

    # percentage
    if render_percs:
      perc_f_str = str(round(perc_f * 100)).split('.')[0] + '%' 
      self.perc_f_text.render(screen, perc_f_str)
      perc_j_str = str(round(perc_j * 100)).split('.')[0] + '%'
      self.perc_j_text.render(screen, perc_j_str)

    self.menu_text.down = one_down
    self.menu_text.render(screen)
