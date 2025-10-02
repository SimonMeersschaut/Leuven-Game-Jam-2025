# Leuven-Game-Jam-2025

Submission for KUL Game Jam 2025

## Getting Started

Deze gids helpt je om het project op te zetten en je eerste code bij te dragen.

### Vereisten

- Python 3.8+

### Installatie

1.  Clone de repository naar je lokale machine.
2.  Open een terminal in de root-directory van het project.
3.  Installeer de nodige packages met pip:
    ```bash
    pip install -r requirements.txt
    ```

### De Game Draaien

Je kan de game starten door het `src` package uit te voeren vanuit de root-directory:

```bash
python -m src
```

## Projectstructuur

Het project is opgedeeld in een aantal kerncomponenten:

-   `src/`: Bevat alle broncode van de game.
    -   `__main__.py`: Het startpunt van de applicatie. Dit bestand initialiseert de `Engine` en start de game.
    -   `engine/`: De core van de game.
        -   `engine.py`: Beheert de game loop, scenes, en events.
        -   `scene.py`: Definieert de `Scene` basisklasse waar alle andere scenes van overerven.
    -   `scenes/`: Bevat de verschillende schermen of "levels" van de game, zoals het hoofdmenu (`menu.py`) of het spel zelf (`game.py`).
    -   `effects/`: Code voor visuele effecten, zoals particles.
-   `resources/`: Bevat alle assets zoals afbeeldingen, audio, en fonts.
-   `requirements.txt`: Lijst alle Python-dependencies op die het project nodig heeft.

## Hoe kan ik bijdragen?

De game is opgebouwd rond een "scene-based" architectuur. Elke scene is een onafhankelijk scherm in de game, zoals het hoofdmenu, een level, of de credits. De `Engine` beheert welke scene op welk moment actief is.

Een nieuwe feature toevoegen (bv. een "Game Over" scherm) komt meestal neer op het creëren van een nieuwe scene.

### Een Nieuwe Scene Maken

1.  **Maak een nieuw bestand aan** in de `src/scenes/` map (bv. `game_over.py`).
2.  **Creëer een klasse** die overerft van de `Scene` basisklasse.

    ```python
    # src/scenes/game_over.py
    from engine.scene import Scene
    import pygame

    class GameOverScene(Scene):
        def __init__(self):
            super().__init__()
            # Initialiseer hier je variabelen

        def load(self, engine):
            # Deze methode wordt één keer aangeroepen wanneer de scene wordt geladen.
            # Gebruik dit om bijvoorbeeld fonts of afbeeldingen in te laden.
            self.font = pygame.font.SysFont("Arial", 60)
            self.text = self.font.render("Game Over", True, (255, 255, 255))

        def render(self, engine):
            # Deze methode wordt elke frame aangeroepen.
            # Teken hier alles op het scherm.
            engine.screen.fill((0, 0, 0)) # Zwarte achtergrond
            text_rect = self.text.get_rect(center=engine.screen.get_rect().center)
            engine.screen.blit(self.text, text_rect)

            # Verwerk hier input om bijvoorbeeld terug naar het menu te gaan.
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    engine.switch_scene("MENU")

    ```

3.  **Registreer je nieuwe scene** in `src/engine/engine.py`.
    -   Importeer je nieuwe klasse.
    -   Voeg een instantie toe aan de `self.scenes` dictionary.

    ```python
    # src/engine/engine.py
    import pygame

    from scenes.menu import MenuScene
    from scenes.game import GameScene
    from scenes.loading import LoadingScene
    from scenes.game_over import GameOverScene # <-- 1. Importeer je scene

    class Engine:
        def __init__(self):
            # ...
            self.scenes = {
                "MENU": MenuScene(),
                "GAME": GameScene(),
                "LOADING": LoadingScene(),
                "GAME_OVER": GameOverScene(), # <-- 2. Voeg toe aan de dictionary
            }
            self.current_scene = self.scenes["MENU"]
        # ...
    ```

4.  **Schakel naar je scene** vanuit een andere scene. Je kan de `engine.switch_scene("SCENE_NAAM")` methode gebruiken om van scene te wisselen. In het voorbeeld hierboven schakelen we vanuit `GameOverScene` terug naar `MENU` met een druk op de spatiebalk.

## Compileer

```bash
pyinstaller -y compile.spec; rm -r build/
```
