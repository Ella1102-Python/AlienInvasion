import pygame
import sys
from settings import Settings
from ship import Ship

class AlienInvasion(object):
    '''管理游戏资源和行为的类'''
    
    def __init__(self):
        '''初始化-Pygame'''
        pygame.init()
        self.settings = Settings()    # 实例化对象
        self.screen = pygame.display.set_mode((0,0),pygame.FULLSCREEN)    # Pygame窗口大小
        # 通过settings调用屏幕的长宽
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height
        pygame.display.set_caption('Alien Invasion')    # 窗口title
        # 设置背景色
        self.bg_color = (230,230,230)
        # 实例化飞船对象
        self.ship = Ship(self)
    
    def run_game(self):
        '''开始游戏主循环'''
        while True:
            self._check_events()
            self.ship.update()
            self._update_screen()

    def _check_events(self):
        '''响应按键和鼠标事件'''
        for event in pygame.event.get():    # get方法获取键盘事件
            if event.type == pygame.QUIT:
                sys.exit()    # 关闭窗口
            # 判断用户按键并作出反应
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)

    def _check_keydown_events(self,event):
        '''响应按键'''
        if event.key == pygame.K_RIGHT:
            # 向右移动飞船（增加x坐标）
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            # 向左移动飞船（减少x坐标）
            self.ship.moving_left = True
        elif event.key == pygame.K_q:
            sys.exit()

    def _check_keyup_events(self,event):
        if event.key == pygame.K_RIGHT:
            # 停止右移
            self.ship.moving_right = False
        if event.key == pygame.K_LEFT:
            # 停止左移
            self.ship.moving_left = False

    def _update_screen(self):                
        '''更新屏幕上的图像，并切换到新屏幕'''
        self.screen.fill(self.settings.bg_color)
        self.ship.blitme()
                    
            # 让最近绘制的屏幕可见
            pygame.display.flip()

if __name__ == '__main__':
    # 创建游戏实例并运行游戏
    ai = AlienInvasion()    # 类的实例
    ai.run_game()    #调用run方法
    
    
    
    
    
    
    
    
    
    