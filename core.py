import asyncio
import traceback

from random_user_id import RandomUserId
from set_user_id_for_ex_id import SetUserIdAtExID
from utils import logger
from validate_count_product import ValidateCountProduct


def validate_count_product(source_data: dict) -> bool:
    try:

        return asyncio.run(ValidateCountProduct(source_data=source_data).start_validate())

    except Exception as error:
        logger.error(f'{source_data["file_name"]} | Неизвестная ошибка: {error}')
        print(traceback.print_exc())


def start_random_user_id(source_data: dict) -> bool:
    try:

        return asyncio.run(RandomUserId(source_data=source_data).start_validate())

    except Exception as error:
        logger.error(f'{source_data["file_name"]} | Неизвестная ошибка: {error}')
        print(traceback.print_exc())


def start_set_user_id_for_ex_id(source_data: dict) -> bool:
    try:

        return asyncio.run(SetUserIdAtExID(source_data=source_data).start_validate())

    except Exception as error:
        logger.error(f'{source_data["file_name"]} | Неизвестная ошибка: {error}')
        print(traceback.print_exc())
