import logging

class GameState:
  RUNNING = 0
  WHEEL = 1
  VICTORY = 2
  COUNTDOWN = 3
  STATE_TIMERS = [0, 2, 2, 1]

  def __init__(self, func):
    self.game_callback = func

    self.set_state(GameState.COUNTDOWN)

  def update(self, delta_t):
    self.state_timer = self.state_timer - (delta_t / 1000) if self.state_timer > 0 else 0

    if self.state_timer == 0:
      if self.state == GameState.WHEEL: self.set_state(GameState.VICTORY)
      elif self.state == GameState.VICTORY: self.set_state(GameState.COUNTDOWN)
      elif self.state == GameState.COUNTDOWN: self.set_state(GameState.RUNNING)

  def set_state(self, state):
    self.state = state
    self.state_timer = GameState.STATE_TIMERS[state]

    self.game_callback(state)
