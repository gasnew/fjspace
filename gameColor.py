import logging
from pygame.locals import Color

class GameColor:
  White = (255, 255, 255)
  Shadow = (50, 50, 50)
  Black = (0, 0, 0)

  Red = (255, 39, 20)
  Green = (41, 238, 0)
  Blue = (0, 181, 204)
  Pink = (255, 106, 173)
  Yellow = (242, 232, 96)
  Cyan = (17, 255, 200)
  Orange = (255, 121, 0)
  Gold = (230, 192, 106)
  Gray = (175, 175, 175)
  Black = (48, 48, 48)
  
  class F:
    Light = (221, 218, 199)
    # Med = (206, 194, 136)
    Med = (198, 186, 127)
    Dark = (168, 132, 35)
  class J:
    Light = (204, 214, 221)
    Med = (111, 134, 149)
    Dark = (28, 68, 142)
  class Space:
    Down = (135, 135, 135)

  PlayerColors = [Red, Green, Blue, Pink, Yellow, Cyan, Orange, Gold, Gray]
  Color = Color(0, 0, 0)

  def lighten(color):
    GameColor.Color.r = color[0]
    GameColor.Color.g = color[1]
    GameColor.Color.b = color[2]

    hsva = GameColor.Color.hsva
    GameColor.Color.hsva = (hsva[0], hsva[1] * 0.2, hsva[2], hsva[3])
    return (GameColor.Color.r, GameColor.Color.g, GameColor.Color.b)