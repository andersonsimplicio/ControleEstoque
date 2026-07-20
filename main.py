# main.py
import sys
from pathlib import Path

# Adiciona a pasta 'src' ao caminho de buscas do Python
sys.path.append(str(Path(__file__).parent / "src"))
from controller.Controller import AppController

if __name__ == "__main__":
    app_controller = AppController()
    app_controller.run()