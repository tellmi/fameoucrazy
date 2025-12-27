# main.py
# -*- coding: utf-8 -*-

import sys
import asyncio
import logging
import qasync
from PySide6.QtWidgets import QApplication, QMainWindow
from qasync import QEventLoop
from ui.main_window import MainWindow
from managers.settings_manager import SettingsManager
from managers.theme_manager import ThemeManager

# Optional: configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

async def main_async():
    settings_manager = SettingsManager()
    window = MainWindow(settings_manager=settings_manager)  # MainWindow creates its own ThemeManager if needed
    window.show()
    logging.info("[MAIN] Application started")

if __name__ == "__main__":

    logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

    # Create the QApplication singleton
    app = QApplication(sys.argv)

    # Use QEventLoop for async/await support
    loop = qasync.QEventLoop(app)
    asyncio.set_event_loop(loop)

    # Create and show main window
    settings_manager = SettingsManager()
    window = MainWindow(settings_manager=settings_manager)
    window.show()
    logging.info("[MAIN] Application started")

    # Run the loop forever
    try:
        loop.run_forever()
    finally:
        # Cleanup
        tasks = [t for t in asyncio.all_tasks(loop) if t is not asyncio.current_task(loop)]
        for task in tasks:
            task.cancel()
        loop.run_until_complete(asyncio.gather(*tasks, return_exceptions=True))
        loop.close()
        logging.info("[MAIN] Application exited cleanly")
