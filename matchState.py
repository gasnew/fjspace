import logging

class MatchState:
  PLAYER_LIST = 0
  NEW_OPPONENT = 1
  COUNTDOWN = 2
  RUNNING = 3
  WHEEL = 4
  VICTORY = 5
  WINNER = 6
  STATE_TIMERS = [0, 0, 3, 0, 2, 2, 4]

  def __init__(self, state, func):
    self.game_callback = func

    self.set_state(state)

  def update(self, delta_t):
    self.state_timer = self.state_timer - (delta_t / 1000) if self.state_timer > 0 else 0

    if self.state_timer == 0:
      if self.state == MatchState.COUNTDOWN: self.set_state(MatchState.RUNNING)
      elif self.state == MatchState.WHEEL: self.set_state(MatchState.VICTORY)
      elif self.state == MatchState.VICTORY: self.set_state(MatchState.COUNTDOWN)
      elif self.state == MatchState.WINNER: self.set_state(MatchState.NEW_OPPONENT)

  def set_state(self, state):
    self.state = state
    self.state_timer = MatchState.STATE_TIMERS[state]

    self.game_callback(state)