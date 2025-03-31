import pygame
import random
import time
import sys

# Initialize pygame
pygame.init()

# Window settings
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("John Pork Calls You")

# Load images
background = pygame.image.load("background.jpg")  # Replace with your background image
phone_icon = pygame.image.load("phone.jpg")  # Replace with phone icon
caller_images = {
    "John Pork": pygame.image.load("john_pork.jpg"),  # Replace with images
    "Skibidi Toilet": pygame.image.load("skibidi.jpg"),
    "Quandale Dingle": pygame.image.load("quandale.jpg"),
    "Jerma": pygame.image.load("jerma.jpg"),
    "???": pygame.image.load("golden.jpg")
}
jumpscare_image = pygame.image.load("jumpscare.jpg")  # Replace with your jumpscare image

# Load sounds
pygame.mixer.init()
sounds = {
    "ringtone": "ringtone.mp3",
    "jumpscare": "jumpscare.mp3",
    "pickup": "pickup.mp3",
    "static": "static.mp3",
    "knock": "knock.mp3",
    "skibidi": "skibidi.mp3",
    "quandale": "quandale.mp3",
    "jerma": "jerma.mp3",
    "golden": "golden_call.mp3"
}

# Callers and messages
callers = {
    "John Pork": ["I'm watching...", "Don't turn around.", "You shouldn't have answered."],
    "Skibidi Toilet": ["SKIBIDI DOM DOM YES YES", "You hear water splashing..."],
    "Quandale Dingle": ["Hey guys, Quandale Dingle here...", "Turn around."],
    "Jerma": ["You're acting kinda sus…", "*Laughs in Jerma*"]
}
golden_call = {"caller": "???", "message": "You have been chosen..."}

# Font
font = pygame.font.Font(None, 36)

# Button setup
button_color = (0, 255, 0)
button_hover = (0, 200, 0)
ignore_color = (255, 0, 0)
ignore_hover = (200, 0, 0)

answer_rect = pygame.Rect(200, 450, 150, 50)
ignore_rect = pygame.Rect(450, 450, 150, 50)

def play_sound(sound):
    pygame.mixer.music.stop()
    pygame.mixer.music.load(sound)
    pygame.mixer.music.play()

def display_text(text, x, y):
    text_surface = font.render(text, True, (255, 255, 255))
    screen.blit(text_surface, (x, y))

def phone_call():
    """Handles the phone call event."""
    caller = random.choice(list(callers.keys()))
    message = random.choice(callers[caller])
    image = caller_images[caller]
    
    play_sound(sounds["ringtone"])

    running = True
    while running:
        screen.blit(background, (0, 0))
        screen.blit(phone_icon, (300, 150))
        screen.blit(image, (250, 50))  # Display caller image
        
        display_text(f"Incoming Call: {caller}", 270, 320)
        display_text("Answer?", 270, 350)

        # Draw buttons
        mouse_pos = pygame.mouse.get_pos()
        answer_col = button_hover if answer_rect.collidepoint(mouse_pos) else button_color
        ignore_col = ignore_hover if ignore_rect.collidepoint(mouse_pos) else ignore_color

        pygame.draw.rect(screen, answer_col, answer_rect)
        pygame.draw.rect(screen, ignore_col, ignore_rect)

        display_text("Answer", 240, 460)
        display_text("Ignore", 490, 460)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if answer_rect.collidepoint(event.pos):
                    play_sound(sounds["pickup"])
                    time.sleep(1)
                    conversation(caller, message)
                    running = False
                elif ignore_rect.collidepoint(event.pos):
                    running = False
                    jumpscare()

def conversation(caller, message):
    """Handles the conversation after picking up the call."""
    play_sound(sounds["static"])
    
    running = True
    while running:
        screen.blit(background, (0, 0))
        screen.blit(caller_images[caller], (250, 50))  
        display_text(f"{caller} says:", 270, 320)
        display_text(f"'{message}'", 270, 350)
        display_text("Press SPACE to respond", 240, 450)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    next_move()
                    running = False

def next_move():
    """Handles next interaction."""
    screen.fill((0, 0, 0))
    display_text("The voice whispers: 'Are you alone? (yes/no)'", 200, 250)
    pygame.display.flip()
    
    answer = ""
    while answer not in ["yes", "no"]:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_y:
                    answer = "yes"
                elif event.key == pygame.K_n:
                    answer = "no"
    
    if answer == "yes":
        play_sound(sounds["knock"])
        time.sleep(1)
        jumpscare()
    else:
        if random.random() < 0.5:
            phone_call()
        else:
            play_sound(sounds["static"])
            time.sleep(1)
            jumpscare()

def jumpscare():
    """Triggers a jumpscare."""
    play_sound(sounds["jumpscare"])
    running = True
    while running:
        screen.blit(jumpscare_image, (0, 0))
        display_text("GAME OVER!", 350, 500)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                running = False
                phone_call()

def start_game():
    """Starts the game."""
    phone_call()

if __name__ == "__main__":
    start_game()
