import pygame
import sys

class AlienInvasion(object):
    '''管理游戏资源和行为的类'''
    
    def __init__(self):
        '''初始化-Pygame'''
        pygame.init()
        self.screen = pygame.display.set_mode((1200,800))    # Pygame窗口大小
        pygame.display.set_caption('Alien Invasion')    # 窗口title
        # 设置背景色
        self.bg_color = (230,230,230)
    
    def run_game(self):
        '''开始游戏主循环'''
        while True:
            # 监视键盘和鼠标事件
            for event in pygame.event.get():    # get方法获取键盘事件
                if event.type == pygame.QUIT:
                    sys.exit()    # 关闭窗口
                    
            # 每次循环时都重绘屏幕
            self.screen.fill(self.bg_color)
                    
            # 让最近绘制的屏幕可见
            pygame.display.flip()
            
if __name__ == '__main__':
    # 创建游戏实例并运行游戏
    ai = AlienInvasion()    # 类的实例
    ai.run_game()    #调用run方法
    
    
    
    
    
    
    
    
    
    