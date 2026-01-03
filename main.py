# main.py
# -*- coding: utf-8 -*-

import sys
import asyncio
import logging
import qasync
from PySide6.QtWidgets import QApplication

from app_windows.main_window import MainWindow
from managers.settings_manager import SettingsManager
from db.db import close_pool


async def main_async():
    # 1️ Create SettingsManager once
    settings_manager = SettingsManager()
    settings_manager.load_from_disk()

    # 2️ Create MainWindow (ThemeManager is auto-created inside)
    window = MainWindow(settings_manager=settings_manager)
    window.show()

    logging.info("[MAIN] Application started")


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s"
    )

    # Create QApplication singleton
    app = QApplication(sys.argv)

    # Use qasync for asyncio support in Qt
    loop = qasync.QEventLoop(app)
    asyncio.set_event_loop(loop)

    async def shutdown():
        logging.info("[MAIN] Shutting down...")
        await close_pool()

    app.aboutToQuit.connect(lambda: asyncio.create_task(shutdown()))

    try:
        # Run the async main function to completion
        loop.run_until_complete(main_async())
        # Then start the event loop
        loop.run_forever()
    finally:
        loop.close()
        logging.info("[MAIN] Application exited cleanly")

