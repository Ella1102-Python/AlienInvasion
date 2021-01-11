import pygame
# from numba import jit
from time import sleep
import sys
from settings import Settings
from game_stats import GameStats
from ship import Ship
from bullet import Bullet
from alien import Alien     

class AlienInvasion(object):
    '''管理游戏资源和行为的类'''
    # @ jit
    def __init__(self):
        '''初始化-Pygame'''
        pygame.init()
        self.settings = Settings()    # 实例化对象
        # self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        '''全屏模式代码👇👇👇'''
        self.screen = pygame.display.set_mode((0,0),pygame.FULLSCREEN)    # Pygame窗口大小
        # 通过settings调用屏幕的长宽
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height
        pygame.display.set_caption('Alien Invasion')    # 窗口title
        # 创建一个用于存储游戏统计信息的实例
        self.stats = GameStats(self)
        # 设置背景色
        self.bg_color = (230,230,230)
        # 实例化飞船对象
        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        # 存储外星人群的编组
        self.aliens = pygame.sprite.Group()
        self._create_fleet()

    def run_game(self):
        '''开始游戏主循环'''
        while True:
            self._check_events()
            if self.stats.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()
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
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()

    def _check_keyup_events(self,event):
        if event.key == pygame.K_RIGHT:
            # 停止右移
            self.ship.moving_right = False
        if event.key == pygame.K_LEFT:
            # 停止左移
            self.ship.moving_left = False

    def _ship_hit(self):
        '''响应飞船被外星人撞到'''
        if self.stats.ships_left > 0:
            # 将ships_left减1
            self.stats.ships_left -= 1
            # 清空余下的外星人和子弹
            self.aliens.empty()
            self.bullets.empty()
            # 创建一群新的外星人，并将飞船放到屏幕底部的中央
            self._create_fleet()
            self.ship.center_ship()
            # 暂停
            sleep(0.5)
        else:
            self.stats.game_active = False

    def _fire_bullet(self):
        '''创建一颗子弹并将其加入编组bullets中'''
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _update_bullets(self):
        '''更新子弹的位置并删除消失的子弹'''
        # 删除消失的子弹
        self.bullets.update()
        # 删除消失的子弹
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)
        # 检查是否有子弹击中了外星人
        # 如果是，就删除相应的子弹和外星人
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)

    def _update_aliens(self):
        '''检查是否有外星人位于屏幕边缘，并更新整群外星人的位置'''
        self._check_fleet_edges()
        self.aliens.update()
        # 检查是否有外星人撞到了飞船
        if pygame.sprite.spritecollideany(self.ship,self.aliens):
            self._ship_hit()
        # 检查是否有外星人到达了屏幕底端
        self._check_aliens_bottom()

    def _create_fleet(self):
        '''创建外星人群'''
        # 创建一个外星人并计算一行可容纳多少个外星人
        # 外星人的间距为外星人的宽度
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size 
        available_space_x = self.settings.screen_width - (2 * alien_width)
        number_aliens_x = available_space_x // (2 * alien_width)
        # 计算屏幕可以容纳多少行外星人
        ship_height = self.ship.rect.height
        available_space_y = (self.settings.screen_height - (4 * alien_height) - ship_height)
        number_rows = available_space_y // (2 * alien_height)
        # 创建外星人群
        for row_number in range(number_rows):
            for alien_number in range(number_aliens_x):
                self._create_alien(alien_number,row_number)

    def _create_alien(self,alien_number,row_number):
        '''创建一个外星人，并将其放在当前行'''
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.rect.x = alien.x
        alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
        self.aliens.add(alien)

    def _check_aliens_bottom(self):
        '''检查是否有外星人到达了屏幕底端'''
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                self._ship_hit()
                # 像飞船欸撞到一样处理
                self._ship_hit()
                break

    def _update_screen(self):                
        '''更新屏幕上的图像，并切换到新屏幕'''
        self.screen.fill(self.settings.bg_color)
        self.ship.blitme()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.aliens.draw(self.screen)

    def _check_fleet_edges(self):
        '''有外星人到达边缘时采取相应措施'''
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        '''将整群外星人下移，并改变它们的方向'''
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1
                    
        # 让最近绘制的屏幕可见
        pygame.display.flip()

if __name__ == '__main__':
    # 创建游戏实例并运行游戏
    ai = AlienInvasion()    # 类的实例
    ai.run_game()    #调用run方法
    
    
    
    
    
    
    
    
    
    