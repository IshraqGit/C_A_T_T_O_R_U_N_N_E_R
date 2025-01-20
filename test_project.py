import pytest
import pygame
from project import collisions

#mocking the initials for test
start_time = 0
player_rect = None
player_walk = []
player_jump = None
egg_surf = None
sushi_surf = None

@pytest.fixture
#initializing the setup for the pytest
def setup_pygame():
    pygame.init()
    screen = pygame.display.set_mode((800, 400))
    test_font = pygame.font.Font(None, 50)

    global start_time, player_rect, player_walk, player_jump, egg_surf, sushi_surf
    start_time = 0  

    player_walk = [pygame.Surface((50, 50)), pygame.Surface((50, 50))]
    player_jump = pygame.Surface((50, 50))
    player_rect = pygame.Rect(100, 290, 50, 50)
    
    egg_surf = pygame.Surface((80, 80))
    sushi_surf = pygame.Surface((120, 120))
    
    return screen, test_font

#checking if the collision is perfectly handled via asserting
def test_collisions(setup_pygame):
    screen, test_font = setup_pygame
    player_rect = pygame.Rect(100, 300, 50, 50)
    obstacle_rects = [pygame.Rect(150, 300, 50, 50),pygame.Rect(300, 300, 50, 50),]

    assert collisions(player_rect, obstacle_rects)  


if __name__ == "__main__":
    pytest.main()
