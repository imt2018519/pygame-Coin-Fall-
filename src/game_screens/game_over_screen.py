import os

from src.game_screens.screen import Screen
from src.misc.game_enums import Game_mode
from pygame.locals import QUIT, KEYUP, MOUSEBUTTONUP
from src.ui.button import Button

LEFT = 1


class Game_over_screen(Screen):
    def __init__(self, pygame, res, surface, game_manager):
        Screen.__init__(self, pygame, res, surface)
        self.game_manager = game_manager
        self.buttons['Restart'] = Button(
            pygame, res, surface, [20, 290, 300, 50], "Restart")
        self.buttons['Back'] = Button(
            pygame, res, surface, [20, 360, 300, 50], "Back")

    def update(self, events):
        if not os.path.isfile("highscore.txt"):
            with open("highscore.txt", "w") as hiscore_file:
                hiscore_file.write("0")
        hisc = open("highscore.txt", "r")
        highscore = hisc.read()
        maxscore = max(int(highscore), int(self.game_manager.score))
        if int(highscore) < int(self.game_manager.score):
            hisc.close()
            hisc = open("highscore.txt", "w")
            hisc.write(str(self.game_manager.score))
        hisc.close()

        textsurface = self.res.heading1_font.render('Game Over', True, self.res.WHITE)
        textsurface2 = self.res.body_font.render(
            'Score: ' + str(self.game_manager.score), True, self.res.WHITE)

        textsurface3 = self.res.body_font.render(
            'Highscore: ' + str(maxscore), True, self.res.WHITE)
        self.surface.blit(self.res.EBG, (0, 0))
        self.surface.blit(textsurface, (20, 0))
        self.surface.blit(textsurface2, (20, 100))
        self.surface.blit(textsurface3, (20, 150))

        for button in self.buttons:
            self.buttons[button].draw()

        mouseup_event = next(
            (x for x in events if x.type == MOUSEBUTTONUP), None)

        if mouseup_event is not None:
            if self.buttons['Restart'].check_click(mouseup_event.pos):
                return Game_mode.GAME_MODE

            if self.buttons['Back'].check_click(mouseup_event.pos):
                return Game_mode.MAIN_MENU

        self.pygame.display.flip()

        for event in events:
            if event.type == QUIT:
                return Game_mode.QUIT

        return Game_mode.GAME_OVER
