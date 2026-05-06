from app.gui.app_shell import AppShell
from app.controller.main_controller import MainController

def main():
    app = AppShell()
    controller = MainController(app)
    app.mainloop()

if __name__ == "__main__":
    main()
