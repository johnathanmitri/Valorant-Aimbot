import pygame
import sys
import ctypes

def captureMouse(mouseHandler):
    # Initialize Pygame
    pygame.init()

    # Set up the display
    WIDTH, HEIGHT = 800, 600
    screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
    pygame.display.set_caption("Mouse Control Example")

    # Set up colors
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)

    # Set initial mouse position
    last_x, last_y = pygame.mouse.get_pos()

    # Grab the mouse input to the window
    pygame.event.set_grab(True)

    # Main game loop
    running = True
    while running:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE or event.key == pygame.K_q:
                    ctypes.windll.user32.ShowWindow(pygame.display.get_wm_info()['window'], 6)  # 6 is SW_MINIMIZE
                    pygame.display.update()

                    #running = False

        # Get current mouse position
        current_x, current_y = pygame.mouse.get_pos()

        # Calculate change in mouse position
        dx = current_x - last_x
        dy = current_y - last_y


        # Adjust mouse position if it reaches window edges
        if current_x <= 0:
            current_x = WIDTH-2
            pygame.mouse.set_pos(current_x, current_y)
        elif current_x >= WIDTH-1:
            current_x = 1
            pygame.mouse.set_pos(current_x, current_y)
        if current_y <= 0:
            current_y = HEIGHT-2
            pygame.mouse.set_pos(current_x, current_y)
        elif current_y >= HEIGHT-1:
            current_y = 1
            pygame.mouse.set_pos(current_x, current_y)
            
        # Update last mouse position
        last_x, last_y = current_x, current_y

        # Print change in mouse position
        #print(f"dx: {dx}, dy: {dy}")
        mouseHandler.addMovement(dx, -dy) # invert the y


        # Clear the screen
        screen.fill(WHITE)

        # Update the display
        pygame.display.flip()

        # Cap the frame rate
        pygame.time.Clock().tick(10)

    # Release the mouse input from the window
    pygame.event.set_grab(False)

    # Quit Pygame
    pygame.quit()
    sys.exit()
