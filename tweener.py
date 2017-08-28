import logging

class Tweener:
  # types of tweens
  EASE_OUT = 0

  def __init__(self, waypoints = {}, first_waypoint = None):
    val = 0 if first_waypoint is None else waypoints[first_waypoint]
    self.val = self.tweened_val = val

    self.waypoints = waypoints
    self.tween_type = Tweener.EASE_OUT
    self.schmaltz = 120

  def add_waypoint(self, name, val):
    self.waypoints[name] = val

  def tween_to(self, name, tween_type = None, schmaltz = None, loop = False):
    if tween_type is None:
      tween_type = Tweener.EASE_OUT
    if schmaltz is not None:
      self.schmaltz = schmaltz

    if name in self.waypoints:
      self.val = self.waypoints[name]
      self.tween_type = tween_type
    elif isinstance(name, (int, float)):
      self.val = name
      self.tween_type = tween_type
    else:
      logging.error("waypoint {0} does not exist".format(name))

  def set_to(self, name):
    if name in self.waypoints:
      self.val = self.tweened_val = self.waypoints[name]
    else:
      logging.error("waypoint {0} does not exist".format(name))

    return self

  def tween_stuff(self, delta_t):
    if self.tween_type == Tweener.EASE_OUT:
      diff = self.val - self.tweened_val
      tween_to = self.tweened_val + (diff / self.schmaltz) * delta_t;
      
      if diff > 0 and (tween_to - self.val) * (diff / abs(diff)) > 0:
        self.tweened_val = self.val
      else:
        self.tweened_val = tween_to