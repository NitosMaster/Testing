mport pygame
import math
import sys

pygame.init()

info = pygame.display.Info()
WIDTH, HEIGHT = info.current_w, info.current_h
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ballistics Sim")

NAVY = (130, 130, 255)
BLACK = (0, 0, 0)
GOLD = (212, 175, 55)
SILVER = (192, 192, 192)

clock = pygame.time.Clock()
FPS = 5000

bullet_density = 9400
size_mm = 4.5
tip_radius = 5 * size_mm
casing_width = 10 * size_mm
casing_height = 20 * size_mm

d_m = size_mm / 1000.0
L_m = casing_height / 1000.0
volume = math.pi * (d_m / 2) ** 2 * L_m
mass = volume * bullet_density

gun_energy = 400.0
velocity = math.sqrt(2.0 * gun_energy / mass)
angle = math.radians(85)
vel_x = velocity * math.cos(angle)
vel_y = -velocity * math.sin(angle)

gravity = 9.81
drag_coefficient = 0.05
air_density = 1.2
cross_sectional = math.pi * (d_m / 2) ** 2

bullet_x = WIDTH // 2
bullet_y = HEIGHT - (casing_height + tip_radius)

bullet_surf = pygame.Surface((casing_width, casing_height + tip_radius * 2), pygame.SRCALPHA)
pygame.draw.circle(bullet_surf, SILVER, (casing_width // 2, tip_radius), tip_radius)
pygame.draw.rect(bullet_surf, GOLD, (0, tip_radius, casing_width, casing_height))
bullet_surf = pygame.transform.rotate(bullet_surf, -90)

prev_angle = 0.0

running = True
while running:
        for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                                    running = False

                                        WINDOW.fill(BLACK)

                                            speed = math.hypot(vel_x, vel_y)
                                                if speed != 0:
                                                            drag_mag = 0.5 * drag_coefficient * air_density * cross_sectional * speed**2
                                                                    drag_x = -drag_mag * (vel_x / speed)
                                                                            drag_y = -drag_mag * (vel_y / speed)
                                                                                else:
                                                                                            drag_x = drag_y = 0

                                                                                                acc_x = drag_x / mass
                                                                                                    acc_y = gravity + drag_y / mass

                                                                                                        vel_x += acc_x / FPS
                                                                                                            vel_y += acc_y / FPS

                                                                                                                if vel_y > 0:
                                                                                                                            vel_y = 0

                                                                                                                                bullet_x += vel_x * 20 / FPS
                                                                                                                                    bullet_y += vel_y * 20 / FPS

                                                                                                                                        current_angle = -math.degrees(math.atan2(vel_y, vel_x))
                                                                                                                                            if current_angle > 160:
                                                                                                                                                        current_angle = 160
                                                                                                                                                            elif current_angle < 0:
                                                                                                                                                                        current_angle = 0

                                                                                                                                                                            prev_angle = current_angle

                                                                                                                                                                                rotated_bullet = pygame.transform.rotate(bullet_surf, current_angle)
                                                                                                                                                                                    rect = rotated_bullet.get_rect(center=(bullet_x, bullet_y))
                                                                                                                                                                                        WINDOW.blit(rotated_bullet, rect)

                                                                                                                                                                                            if bullet_y > HEIGHT:
                                                                                                                                                                                                        bullet_x = WIDTH // 2
                                                                                                                                                                                                                bullet_y = HEIGHT - (casing_height + tip_radius)
                                                                                                                                                                                                                        angle = math.radians(85)
                                                                                                                                                                                                                                vel_x = velocity * math.cos(angle)
                                                                                                                                                                                                                                        vel_y = -velocity * math.sin(angle)
                                                                                                                                                                                                                                                prev_angle = -math.degrees(math.atan2(vel_y, vel_x))

                                                                                                                                                                                                                                                    pygame.display.flip()
                                                                                                                                                                                                                                                        clock.tick(FPS)

                                                                                                                                                                                                                                                        pygame.quit()
                                                                                                                                                                                                                                                        sys.exit()
