import pygame
from constants import *
 
class Help():
    def __init__(self):
        big_font = pygame.font.Font(None, 50)
        self.small_font = pygame.font.Font(None, 30) # этот шрифт надо помнить и для постоянной надписи
        text1 = big_font.render(" Управление: ", 1, C_RED)
        text2 = self.small_font.render(" Влево: 'a' или стрелка влево ", 1, C_RED)
        text3 = self.small_font.render(" Вправо: 'd' или стрелка влево ", 1, C_RED)
        text4 = self.small_font.render(" Прыжок: 'w' или стрелка верх ", 1, C_RED)
        text5 = self.small_font.render(" Выстрел: пробел ", 1, C_RED)
        text6 = self.small_font.render(" Музыка вкл/выкл: 'm', громче: 'u', тише: ' j ' ", 1, C_RED)
        text7 = self.small_font.render(" Подсказка вкл/выкл (игра на паузе): 'h' ", 1, C_RED)
        
        img = pygame.Surface([round(3 * win_width / 4), round(3 * win_height / 4)])
        img.fill(C_ORANGE)
        w = round(win_width / 8)
        h = round(win_height / 12)
        h1 = round(h / 2)
        img.blit(text1, (w, h))
        img.blit(text2, (w, 3 * h - h1))
        img.blit(text3, (w, 4 * h - h1))
        img.blit(text4, (w, 5 * h - h1))
        img.blit(text5, (w, 6 * h - h1))
        img.blit(text6, (w, 7 * h - h1))
        img.blit(text7, (w, 8 * h - h1))
        img.set_alpha(160)
        self.img = img

        # Добавим строки для постоянной подсказки:
        self.text_points = self.small_font.render("Очков:   ", 1, C_YELLOW)
        self.text_points_w = self.text_points.get_rect().width
        self.text_lives = self.small_font.render("Жизней:   ", 1, C_YELLOW)
        self.text_lives_w = self.text_lives.get_rect().width
        self.text_help = self.small_font.render("Пауза/подсказка: 'h'", 1, C_YELLOW)
        self.text_height = self.text_help.get_rect().height

    def line(self, points=0, lives=1):
        tab = 50
        img = pygame.Surface([win_width, self.text_height], pygame.SRCALPHA) # исходник - попиксельно прозрачный
        # пишем строку про жизни, добавляем число жизней:
        img.blit(self.text_lives, (0, 0))
        text = self.small_font.render(str(lives), 1, C_WHITE)
        img.blit(text, (self.text_lives_w, 0))
        # пишем строку про очки, добавляем число очков:
        img.blit(self.text_points, (self.text_lives_w + tab, 0))
        text = self.small_font.render(str(points), 1, C_WHITE)
        img.blit(text, (self.text_lives_w + tab + self.text_points_w, 0))
        # пишем строку про подсказку:
        img.blit(self.text_help, (self.text_lives_w + tab + self.text_points_w + tab, 0))
        return img


