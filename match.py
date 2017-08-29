import logging
import random
import pygame
from pygame.locals import *
from playerList import PlayerList
from game import Game
from wheel import Wheel
from hud import Hud
from scoreboard import Scoreboard
from menu import Menu
from matchState import MatchState
from textRenderer import TextRenderer
from shadowedPressable import ShadowedPressable
from gameColor import GameColor
from tweener import Tweener

class Match:
  # -- NECESSARY CONSTANTS --
  ENCOURAGEMENTS = ["Nice!", "Better than I expected...", "[REDACTED]", "Congratulations!", "Have a slice of 3.1415926535897932384626.",
                    "[VICTORY MESSAGE]", "Wow!", "Great, kid! Don't get cocky.", "Gnarly!", "I love you."]
  CONSOLATIONS = ["The other guy's cheating!", "You've got red on you!", "'Tis but a scratch!", "Help, I'm trapped in a universe factory.",
                  "It was the best of times, it was the worst of times, it was the age of wisdom, it was the age of foolishness",
                  "I know.", "Not like this...", "Huh?", "Not my tempo.", "Don't grumble; give a whistle!", "At least you're just practicing."]

  def __init__(self, AGREE_TIME, WIN_TIME, COOLDOWN_TIME, STALE_TIME, TOTAL_TIME, FAILURE_TIME, NUM_WINS,
               keys, p_list_rect, scoreboard_rect, top_rect, top_rect_left, top_rect_right, game_rect, bottom_rect, shadow_dist, sys_font):
    # -- IMPORTS --
    self.keys = keys
    self.top_rect_left = top_rect_left
    self.top_rect_right = top_rect_right
    self.bottom_rect = bottom_rect
    self.AGREE_TIME = AGREE_TIME
    self.NUM_WINS = NUM_WINS
    self.shadow_dist = shadow_dist

    # -- MATCH INFO --
    self.match_num = 0
    self.big_f_agree = self.big_j_agree = 0
    self.f_wins = self.j_wins = 0
    self.score_streak = 0

    # -- NECESSARY CLASSES --
    self.p_list = PlayerList(p_list_rect, shadow_dist, sys_font)
    self.game = Game(WIN_TIME, COOLDOWN_TIME, STALE_TIME, TOTAL_TIME, FAILURE_TIME, self.keys, game_rect, shadow_dist, sys_font)
    self.wheel = Wheel(game_rect, shadow_dist, sys_font)
    self.hud = Hud(top_rect, bottom_rect, shadow_dist, sys_font)
    self.scoreboard = Scoreboard(scoreboard_rect, shadow_dist, sys_font, self.p_list)
    self.menu = Menu(p_list_rect, self.keys, shadow_dist, sys_font)
    self.match_state = MatchState(MatchState.PLAYER_LIST, self.state_response)

    # -- MENU ACTIONS --
    self.menu.add_item("[2]", "PRACTICE MODE", 0.5, lambda : self.match_state.set_state(MatchState.PRACTICE_MODE))
    self.menu.add_item("[3]", "RESET MATCHUP", 0.5, lambda : self.match_state.set_state(MatchState.NEW_OPPONENT, same_match = True))
    self.menu.add_item("[4]", "NEXT OPPONENT", 0.5, lambda : self.match_state.set_state(MatchState.NEW_OPPONENT, next = True))
    self.menu.add_item("[5]", "CHANGE PLAYERS", 0.5, lambda : self.match_state.set_state(MatchState.PLAYER_LIST))

    # -- RENDERING --
    # bottom bar
    self.f_name_text = TextRenderer(sys_font, 2, (top_rect_left.centerx, bottom_rect.centery), shadow_dist)
    self.j_name_text = TextRenderer(sys_font, 2, (top_rect_right.centerx, bottom_rect.centery), shadow_dist)
    self.streak_text = TextRenderer(sys_font, 1, (bottom_rect.width * 0.08, bottom_rect.centery + bottom_rect.height * 0.25), shadow_dist)

    self.practice_mode_text = TextRenderer(sys_font, 2, bottom_rect.center, 0)
    self.practice_inst_rect = Rect((game_rect.left + game_rect.height * 0.05, game_rect.top + game_rect.height * 0.05), (game_rect.width, game_rect.height * 0.25))
    self.practice_inst_0 = ShadowedPressable.make_pressable_key("1. Hold your key to build your bar.", sys_font, 1, GameColor.Pink)[0].convert_alpha()
    self.practice_inst_1 = ShadowedPressable.make_pressable_key("2. Press [SPACE] to reset moving bars.", sys_font, 1, GameColor.Cyan)[0].convert_alpha()
    self.practice_inst_2 = ShadowedPressable.make_pressable_key("3. Build the biggest bar to win!", sys_font, 1, GameColor.Yellow)[0].convert_alpha()
    
    # vs
    self.new_match_text = TextRenderer(sys_font, 4, (game_rect.centerx, game_rect.top + game_rect.height / 6), shadow_dist, GameColor.White)

    self.vs_left_bar = Rect((0, game_rect.y + game_rect.height / 3), (top_rect_left.width, game_rect.height / 5))
    self.vs_right_bar = Rect((game_rect.centerx, self.vs_left_bar.bottom), (self.vs_left_bar.width, self.vs_left_bar.height))
    vs_par_width = game_rect.height / 7
    self.vs_parallelogram = ((game_rect.centerx, self.vs_left_bar.top), (game_rect.centerx - vs_par_width, self.vs_right_bar.bottom), (game_rect.centerx, self.vs_right_bar.bottom), (game_rect.centerx + vs_par_width, self.vs_left_bar.top))
    self.f_name_big_text = TextRenderer(sys_font, 4, (top_rect_left.centerx + shadow_dist, self.vs_left_bar.centery + shadow_dist), shadow_dist, GameColor.F.Dark)
    self.j_name_big_text = TextRenderer(sys_font, 4, (top_rect_right.centerx + shadow_dist, self.vs_right_bar.centery + shadow_dist), shadow_dist, GameColor.J.Dark)
    self.vs_text = TextRenderer(sys_font, 2, (game_rect.centerx + shadow_dist, self.vs_left_bar.bottom + shadow_dist), shadow_dist)
    self.vs_left_bar.move_ip((top_rect_left.width, 0))

    big_f, big_f_shadow = ShadowedPressable.make_pressable_key("[F]", sys_font, 4)
    self.big_f = ShadowedPressable(big_f.convert_alpha(), big_f_shadow, (top_rect_left.centerx, game_rect.top + game_rect.height * 0.85), shadow_dist)
    big_j, big_j_shadow = ShadowedPressable.make_pressable_key("[J]", sys_font, 4)
    self.big_j = ShadowedPressable(big_j.convert_alpha(), big_j_shadow, (top_rect_right.centerx, game_rect.top + game_rect.height * 0.85), shadow_dist)

    # counter
    self.counter = TextRenderer(sys_font, 4, game_rect.center, shadow_dist)
    self.ready_text = TextRenderer(sys_font, 2, (game_rect.centerx, game_rect.top + game_rect.height * 0.35), shadow_dist)

    # win rects
    win_rect_size = top_rect.height * 0.15
    self.win_rect = Rect(top_rect.centerx - win_rect_size / 2, win_rect_size, win_rect_size, win_rect_size)
    self.win_rect_shadows = [self.win_rect.move(self.win_rect.width * 2 * idx, 0) for idx in [-3, -2, -1, 1, 2, 3]]
    self.f_win_rects = []
    self.j_win_rects = []

    # win text
    self.f_win_loss_text = TextRenderer(sys_font, 4, (top_rect_left.centerx, game_rect.top + game_rect.height * 0.35), shadow_dist)
    self.j_win_loss_text = TextRenderer(sys_font, 4, (top_rect_right.centerx, game_rect.top + game_rect.height * 0.35), shadow_dist)
    self.f_plus_minus_text = TextRenderer(sys_font, 4, (top_rect_left.centerx, game_rect.top + game_rect.height * 0.65), shadow_dist)
    self.j_plus_minus_text = TextRenderer(sys_font, 4, (top_rect_right.centerx, game_rect.top + game_rect.height * 0.65), shadow_dist)
    self.f_enc_cons_text = TextRenderer(sys_font, 1, (top_rect_left.centerx, game_rect.top + game_rect.height * 0.5), shadow_dist / 8)
    self.j_enc_cons_text = TextRenderer(sys_font, 1, (top_rect_right.centerx, game_rect.top + game_rect.height * 0.5), shadow_dist / 8)

    # tweens
    self.vs_bar_w = Tweener({"retracted": 0, "extended": top_rect_left.width}, "retracted")
    self.f_name_big_x = Tweener({"out": 0, "in": self.f_name_big_text.center[0]}, "out")
    self.j_name_big_x = Tweener({"out": game_rect.right, "in": self.j_name_big_text.center[0]}, "out")

    # -- SOUND --
    self.vs_sound = pygame.mixer.Sound("SFX/VS.wav")
    self.timer_sound = pygame.mixer.Sound("SFX/beep.wav")
    self.begin_sound = pygame.mixer.Sound("SFX/begin_game.wav")
    self.climax_sound = pygame.mixer.Sound("SFX/climax.wav")
    self.victory_sounds = [pygame.mixer.Sound("SFX/vic{0}.wav".format(i)) for i in range(3)]
    self.win_sound = pygame.mixer.Sound("SFX/win.wav")

    self.reset()

  def reset(self):
    self.match_num = 0
    self.big_f_agree = self.big_j_agree = 0
    self.f_wins = self.j_wins = 0
    self.score_streak = 0

    self.winner = ""
    self.hold_wheel_render = False

    self.p_list.focus()
    self.match_state.set_state(MatchState.PLAYER_LIST)

    self.encouragement = ""
    self.consolation = ""

  def state_response(self, state, **kwargs):
    self.p_list.defocus()
    if state not in {MatchState.VICTORY_0, MatchState.VICTORY_1}: self.hold_wheel_render = False

    if state == MatchState.PLAYER_LIST:
      self.p_list.focus()
    elif state == MatchState.COUNTDOWN:
      if self.NUM_WINS in {self.f_wins, self.j_wins}:
        self.match_state.set_state(MatchState.WINNER)
        self.f_win_loss_text.color = GameColor.Green if self.winner == "f" else GameColor.Red
        self.j_win_loss_text.color = GameColor.Green if self.winner == "j" else GameColor.Red
        self.f_plus_minus_text.color = GameColor.Green if self.winner == "f" else GameColor.Red
        self.j_plus_minus_text.color = GameColor.Green if self.winner == "j" else GameColor.Red

        if self.winner == "f":
          self.score_streak += 1
          self.p_list.pf.score += self.score_streak
        else:
          self.score_streak = 1
          self.p_list.pj.score += self.score_streak

        self.win_sound.play()
      else:
        self.game.reset()
        self.begin_sound.play()
        self.timer_sound.play(loops = 2)
    elif state == MatchState.NEW_OPPONENT:
      if self.j_wins == self.NUM_WINS:
        self.p_list.swap_players()

      if kwargs.get("next"):
        self.p_list.new_opponent()
      elif kwargs.get("shuffle"):
        self.p_list.shuffle()
      
      self.p_list.defocus()

      if not kwargs.get("same_match"): self.match_num += 1
      self.big_f_agree = self.big_j_agree = 1
      self.f_wins = self.j_wins = 0
      self.f_win_rects = []
      self.j_win_rects = []

      self.game.reset()

      self.vs_bar_w.set_to("retracted").tween_to("extended", schmaltz = 70)
      self.f_name_big_x.set_to("out").tween_to("in", schmaltz = 300)
      self.j_name_big_x.set_to("out").tween_to("in", schmaltz = 300)

      self.vs_sound.play()
    elif state == MatchState.WHEEL:
      self.wheel.start(self.match_state.state_timer, self.game.perc_f, self.game.perc_j)
      self.hold_wheel_render = True
    elif state == MatchState.VICTORY_0:
      self.climax_sound.play()
    elif state == MatchState.VICTORY_1:
      if self.winner == "f":
        self.f_wins += 1
        self.p_list.pf.wins += 1
        self.p_list.pj.losses += 1

        self.f_win_rects.append(self.win_rect.move(-(self.win_rect.width * 2) * self.f_wins - self.shadow_dist, -self.shadow_dist))
      else:
        self.j_wins += 1
        self.p_list.pj.wins += 1
        self.p_list.pf.losses += 1
        self.j_win_rects.append(self.win_rect.move((self.win_rect.width * 2) * self.j_wins - self.shadow_dist, -self.shadow_dist))

      random.choice(self.victory_sounds).play()
    elif state == MatchState.PRACTICE_MODE:
      self.game.reset(practice = True)
      self.begin_sound.play()
    elif state == MatchState.PRACTICE_VICTORY:
      self.climax_sound.play()
      
      self.f_enc_cons_text.color = GameColor.Green if self.winner == "f" else GameColor.Red
      self.j_enc_cons_text.color = GameColor.Green if self.winner == "j" else GameColor.Red
      self.encouragement = random.choice(Match.ENCOURAGEMENTS)
      self.consolation = random.choice(Match.CONSOLATIONS)

  def match_stuff(self, delta_t):
    # player list stuff
    self.p_list.p_list_stuff(self.keys.plus, self.keys.minus)

    # game stuff
    game_over = False
    perc_f = perc_j = 0
    if self.match_state.state in {MatchState.RUNNING, MatchState.PRACTICE_MODE}:
      game_over, self.winner, perc_f, perc_j = self.game.game_stuff(delta_t)

    # wheel stuff
    if self.match_state.state == MatchState.WHEEL or self.hold_wheel_render:
      game_over, self.winner = self.wheel.wheel_stuff(delta_t)

    # hud stuff
    self.hud.hud_stuff()

    # non-hud weird stuff
    if self.match_state.state == MatchState.NEW_OPPONENT:
      if self.keys.f: self.big_f_agree = self.big_f_agree - (delta_t / (self.AGREE_TIME * 1000)) if self.big_f_agree > 0 else 0
      else: self.big_f_agree = 1
      
      if self.keys.j: self.big_j_agree = self.big_j_agree - (delta_t / (self.AGREE_TIME * 1000)) if self.big_j_agree > 0 else 0
      else: self.big_j_agree = 1

    # state stuff
    self.match_state.update(delta_t)
    if self.match_state.state == MatchState.PLAYER_LIST and self.keys.enter:
      self.match_state.set_state(MatchState.NEW_OPPONENT, shuffle = self.match_num == 0, same_match = self.match_num != 0)
    elif self.match_state.state == MatchState.NEW_OPPONENT and self.keys.f and self.keys.j and self.big_f_agree == self.big_j_agree == 0:
      self.match_state.set_state(MatchState.COUNTDOWN)
    elif game_over and self.match_state.state in {MatchState.RUNNING, MatchState.WHEEL, MatchState.PRACTICE_MODE}:
      if self.winner == "stale":
        self.match_state.set_state(MatchState.WHEEL)
      elif self.match_state.state == MatchState.PRACTICE_MODE:
        self.match_state.set_state(MatchState.PRACTICE_VICTORY)
      else:
        self.match_state.set_state(MatchState.VICTORY_0)

    # menu stuff
    if self.keys.nums[49]:
      if not self.menu.in_focus and self.menu.can_focus: self.menu.focus()
      self.menu.can_focus = False
    else:
      self.menu.defocus()
      self.menu.can_focus = True

    self.menu.menu_stuff(delta_t)

    # tween stuff
    self.vs_bar_w.tween_stuff(delta_t)
    self.f_name_big_x.tween_stuff(delta_t)
    self.j_name_big_x.tween_stuff(delta_t)
    
  def render_stuff(self, screen):
    self.game.render_stuff(
      screen,
      render_space = self.match_state.state in {MatchState.RUNNING, MatchState.PRACTICE_MODE},
      render_keys = self.match_state.state != MatchState.NEW_OPPONENT,
      disable_keys = self.match_state.state == MatchState.PLAYER_LIST)
    
    if self.match_state.state == MatchState.COUNTDOWN and self.match_state.state_timer >= 0:
      self.counter.render(screen, str(self.match_state.state_timer)[:4])
      self.ready_text.render(screen, "READY?!?")
    if self.match_state.state == MatchState.WHEEL or self.hold_wheel_render:
      self.wheel.render(screen)

    pygame.draw.rect(screen, GameColor.F.Med, self.top_rect_left)
    pygame.draw.rect(screen, GameColor.J.Med, self.top_rect_right)
    pygame.draw.rect(screen, GameColor.Shadow, self.bottom_rect)

    if self.match_state.state not in {MatchState.PRACTICE_MODE, MatchState.PRACTICE_VICTORY}:
      self.f_name_text.render(screen, self.p_list.pf.name, GameColor.lighten(self.p_list.pf.color))
      self.j_name_text.render(screen, self.p_list.pj.name, GameColor.lighten(self.p_list.pj.color))
      self.streak_text.render(screen, "STREAK:{0}".format(self.score_streak))
    else:
      self.practice_mode_text.render(screen, "PRACTICE MODE", GameColor.Gold)

      diff = (self.practice_inst_rect.height - self.practice_inst_0.get_height()) / (3 - 1)
      screen.blit(self.practice_inst_0, self.practice_inst_rect.topleft, special_flags = BLEND_RGB_SUB)
      screen.blit(self.practice_inst_1, (self.practice_inst_rect.left, self.practice_inst_rect.top + diff), special_flags = BLEND_RGB_SUB)
      screen.blit(self.practice_inst_2, (self.practice_inst_rect.left, self.practice_inst_rect.top + 2 * diff), special_flags = BLEND_RGB_SUB)

    if self.match_state.state == MatchState.NEW_OPPONENT:
      self.new_match_text.render(screen, "MATCH {0}!".format(self.match_num))

      self.vs_left_bar.width = -self.vs_bar_w.tweened_val
      self.vs_right_bar.width = self.vs_bar_w.tweened_val
      pygame.draw.rect(screen, GameColor.White, self.vs_left_bar)
      pygame.draw.rect(screen, GameColor.White, self.vs_right_bar)
      pygame.draw.polygon(screen, GameColor.Shadow, self.vs_parallelogram)

      self.f_name_big_text.center = (self.f_name_big_x.tweened_val, self.f_name_big_text.center[1])
      self.f_name_big_text.render(screen, self.p_list.pf.name, self.p_list.pf.color)
      self.j_name_big_text.center = (self.j_name_big_x.tweened_val, self.j_name_big_text.center[1])
      self.j_name_big_text.render(screen, self.p_list.pj.name, self.p_list.pj.color)
      self.vs_text.render(screen, "VS")

      self.big_f.down = self.keys.f
      self.big_j.down = self.keys.j
      self.big_f.render(screen, self.big_f_agree)
      self.big_j.render(screen, self.big_j_agree)

    if self.match_state.state == MatchState.WINNER:
      self.f_win_loss_text.render(screen, "WIN" if self.winner == "f" else "LOSE")
      self.j_win_loss_text.render(screen, "WIN" if self.winner == "j" else "LOSE")

      self.f_plus_minus_text.render(screen, "+{0}".format(self.score_streak) if self.winner == "f" else "")
      self.j_plus_minus_text.render(screen, "+1" if self.winner == "j" else "")

    if self.match_state.state not in {MatchState.PRACTICE_MODE, MatchState.PRACTICE_VICTORY}:
      for rect in self.win_rect_shadows: pygame.draw.rect(screen, GameColor.Shadow, rect)
      for rect in self.f_win_rects: pygame.draw.rect(screen, GameColor.F.Light, rect)
      for rect in self.j_win_rects: pygame.draw.rect(screen, GameColor.J.Light, rect)

    self.hud.render_stuff(screen, self.game.timer, self.game.perc_f, self.game.perc_j, self.keys.nums[49], render_percs = self.match_state.state in {MatchState.RUNNING, MatchState.PRACTICE_MODE})

    if self.match_state.state == MatchState.PRACTICE_VICTORY:
      self.f_enc_cons_text.render(screen, self.encouragement if self.winner == "f" else self.consolation)
      self.j_enc_cons_text.render(screen, self.encouragement if self.winner == "j" else self.consolation)

    if self.match_state.state == MatchState.PLAYER_LIST:
      self.p_list.render_stuff(screen)

    if self.keys.tab:
      self.scoreboard.render_stuff(screen)

    if self.menu.in_focus:
      self.menu.render_stuff(screen)