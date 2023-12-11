import sys
import pygame
import os
from tkinter import Tk, filedialog

def choose_music_folder():
    Tk().withdraw()  # Hide the main window
    folder_selected = filedialog.askdirectory()
    return folder_selected

pygame.init()

# Initialisation de la fenêtre
width, height = 700, 500
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("playerMusic")

# Chargement de l'image de fond et redimensionnement
background_image = pygame.image.load("./images/image_fond.png")
background_image = pygame.transform.scale(background_image, (width, height))

# Chargement des images des boutons
buttons = {
    "play": pygame.image.load("./images/play.png"),
    "pause": pygame.image.load("./images/pause.png"),
    "precedent": pygame.image.load("./images/precedent.png"),
    "suivant": pygame.image.load("./images/suivant.png"),
    "dossier": pygame.image.load("./images/dossierp.png"),
    "mute": pygame.image.load("./images/mute.png"),
    "mute_off": pygame.image.load("./images/mute_off.png"),
}

# Redimensionnement des boutons
button_size = (40, 40)
for button in buttons:
    buttons[button] = pygame.transform.scale(buttons[button], button_size)

# Positions des boutons
button_positions = {
    "play": (250, 350),
    "pause": (300, 350),
    "precedent": (200, 350),
    "suivant": (350, 350),
    "dossier": (150, 350),
    "mute": (600, 360),
}

# Liste des chansons dans le dossier music_folder
music_folder = "music_folder"
audio_files = [os.path.join(music_folder, file) for file in os.listdir(music_folder) if file.endswith(".mp3")]

# Chargement des images associées à chaque chanson
song_images = {audio_file: pygame.image.load(os.path.join(music_folder, f"{os.path.splitext(os.path.basename(audio_file))[0]}.png"))
               for audio_file in audio_files if os.path.exists(os.path.join(music_folder, f"{os.path.splitext(os.path.basename(audio_file))[0]}.png"))}

# Initialisation de la musique
pygame.mixer.init()
current_track_index = 0
pygame.mixer.music.load(audio_files[current_track_index])

# Gestion du volume
volume = 0.5
pygame.mixer.music.set_volume(volume)

# Gestion de la barre de volume
volume_rect = pygame.Rect(550, 360, 20, 80)
dragging_volume = False

# Gestion du bouton mute
mute = False

# Police de caractères pour le texte
font = pygame.font.Font(None, 24)

# Boucle principale
clock = pygame.time.Clock()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            for button, position in button_positions.items():
                if pygame.Rect(position, button_size).collidepoint(x, y):
                    if button == "play":
                        pygame.mixer.music.pause() if pygame.mixer.music.get_busy() else pygame.mixer.music.unpause()
                    elif button == "pause":
                        pygame.mixer.music.pause()
                    elif button == "precedent":
                        current_track_index = (current_track_index - 1) % len(audio_files)
                        pygame.mixer.music.load(audio_files[current_track_index])
                        pygame.mixer.music.play()
                    elif button == "suivant":
                        current_track_index = (current_track_index + 1) % len(audio_files)
                        pygame.mixer.music.load(audio_files[current_track_index])
                        pygame.mixer.music.play()
                    elif button == "dossier":
                        music_folder = choose_music_folder()
                        audio_files = [os.path.join(music_folder, file) for file in os.listdir(music_folder) if file.endswith(".mp3")]
                        current_track_index = 0
                        pygame.mixer.music.load(audio_files[current_track_index])
                    elif button == "mute":
                        mute = not mute
                        if mute:
                            pygame.mixer.music.set_volume(0)
                        else:
                            pygame.mixer.music.set_volume(volume)

            # Vérification du clic sur la barre de volume
            if volume_rect.collidepoint(x, y):
                dragging_volume = True

        elif event.type == pygame.MOUSEBUTTONUP:
            dragging_volume = False

        elif event.type == pygame.MOUSEMOTION and dragging_volume:
            volume = max(0, min(1, (event.pos[1] - volume_rect.y) / volume_rect.height))
            pygame.mixer.music.set_volume(volume)

    # Effacement de l'écran
    screen.blit(background_image, (0, 0))

    # Dessin des boutons avec effets visuels
    for button, position in button_positions.items():
        button_rect = pygame.Rect(position, button_size)
        pygame.draw.rect(screen, (255, 255, 255), button_rect, 2)
        if button_rect.collidepoint(pygame.mouse.get_pos()):
            pygame.draw.rect(screen, (100, 100, 100), button_rect)
        if button == "mute":
            if mute:
                screen.blit(buttons["mute_off"], position)
            else:
                screen.blit(buttons["mute"], position)
        else:
            screen.blit(buttons[button], position)

    # Dessin de la barre de volume
    pygame.draw.rect(screen, (0, 255, 0), (volume_rect.x, volume_rect.y + volume_rect.height - volume_rect.height * volume, volume_rect.width, volume_rect.height * volume))
    pygame.draw.rect(screen, (255, 0, 0), volume_rect, 2)

    # Dessin de la liste des chansons
    for i, audio_file in enumerate(audio_files):
        text = font.render(os.path.basename(audio_file), True, (255, 255, 255))
        text_rect = text.get_rect(topleft=(50, 50 + i * 30))
        screen.blit(text, text_rect)

        # Gestion du clic sur les noms de fichiers pour changer la piste
        if text_rect.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
            current_track_index = i
            pygame.mixer.music.load(audio_files[current_track_index])
            pygame.mixer.music.play()

    # Affichage des images associées à chaque chanson
    current_audio_file = audio_files[current_track_index]
    if current_audio_file in song_images:
        image_rect = song_images[current_audio_file].get_rect(topleft=(400, 50))
        screen.blit(song_images[current_audio_file], image_rect)

    # Mise à jour de l'affichage
    pygame.display.flip()

    # Limiter la boucle principale à 30 images par seconde
    clock.tick(30)

