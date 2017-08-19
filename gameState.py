import logging

class GameState:
  PLAYER_LIST = 0
  NEW_OPPONENT = 1
  COUNTDOWN = 2
  RUNNING = 3
  WHEEL = 4
  VICTORY = 5
  WINNER = 6
  STATE_TIMERS = [0, 0, 3, 0, 2, 2, 3]

  def __init__(self, state, func):
    self.game_callback = func

    self.set_state(state)

  def update(self, delta_t):
    self.state_timer = self.state_timer - (delta_t / 1000) if self.state_timer > 0 else 0

    if self.state_timer == 0:
      if self.state == GameState.COUNTDOWN: self.set_state(GameState.RUNNING)
      elif self.state == GameState.WHEEL: self.set_state(GameState.VICTORY)
      elif self.state == GameState.VICTORY: self.set_state(GameState.COUNTDOWN)
      elif self.state == GameState.WINNER: self.set_state(GameState.NEW_OPPONENT)

  def set_state(self, state):
    self.state = state
    self.state_timer = GameState.STATE_TIMERS[state]

    self.game_callback(state)
