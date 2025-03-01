import argparse
import asyncio
import logging
from aiopath import AsyncPath
from aioshutil import copyfile
import os

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger()


async def read_folder(source_folder: AsyncPath, output_folder: AsyncPath):
    try:

        if not await source_folder.exists():
            logger.error(f"Вихідна папка {source_folder} не існує.")
            return

        if not await output_folder.exists():
            await output_folder.mkdir(parents=True)

        async for file_path in source_folder.rglob("*"):
            if await file_path.is_file():
                await copy_file(file_path, output_folder)

    except Exception as e:
        logger.error(f"Помилка при читанні папки: {e}")


async def copy_file(file_path: AsyncPath, output_folder: AsyncPath):
    try:

        extension = file_path.suffix.lstrip(".").lower()

        extension_folder = output_folder / extension
        if not await extension_folder.exists():
            await extension_folder.mkdir()

        destination_path = extension_folder / file_path.name
        await copyfile(file_path, destination_path)
        logger.info(f"Файл {file_path} успішно скопійовано в {destination_path}")

    except Exception as e:
        logger.error(f"Помилка при копіюванні файлу {file_path}: {e}")


def main():
    parser = argparse.ArgumentParser(description="Асинхронне сортування файлів за розширенням.")
    parser.add_argument("source_folder", type=str, help="Шлях до вихідної папки")
    parser.add_argument("output_folder", type=str, help="Шлях до цільової папки")

    args = parser.parse_args()

    source_folder = AsyncPath(args.source_folder)
    output_folder = AsyncPath(args.output_folder)

    asyncio.run(read_folder(source_folder, output_folder))


if __name__ == "__main__":
    main()

