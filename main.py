from multiprocessing.dummy import Pool

from core import start_random_user_id, validate_count_product, start_set_user_id_for_ex_id
from utils import logger
from utils.generate_ex_id import ExIdType

if __name__ == '__main__':

    with open('file_names.txt', 'r', encoding='utf-8-sig') as file:
        files_list: list[str] = [row.strip() for row in file]

    with open('true_keywords.txt', 'r', encoding='utf-8-sig') as file:
        true_keywords_list: list[str] = [row.strip() for row in file]

    with open('incorrect_keywords.txt', 'r', encoding='utf-8-sig') as file:
        incorrect_keywords_list: list[str] = [row.strip() for row in file]

    threads: int = int(input('\nУкажите кол-во потоков\nThreads: '))

    logger.info(f'Загружено {len(files_list)} файлов / {len(true_keywords_list)} '
                f'ключевых слов / {len(incorrect_keywords_list)} слова которые надо исключить')

    user_action: int = int(input('\n1. Проставление рандомных id\n'
                                 '2. Подсчет кол-ва по ключевым словам\n'
                                 '3. Связка с внешним полем\n'
                                 'Введите ваше действие: '))

    match user_action:
        case 1:
            max_count: str | None = input('\nЕсли есть ограничение по кол-ву товаров на одного юзера введите('
                                          'опционально):')
            max_count = int(max_count) if max_count else None
            if max_count:
                column_count: str | None | int = input('\nВведите номер столбца с кол-вом:')
                if column_count:
                    column_count = int(column_count)
                else:
                    raise Exception(f'Конфликт! Номер столбца для импорта кол-ва не указан')
            else:
                column_count = None

            max_amount: str | None = input('\nЕсли есть ограничение по сумме товаров на одного юзера введите('
                                           'опционально):')

            max_amount = int(max_amount) if max_amount else None

            if max_amount:
                column_amount: str | None | int = input('\nВведите номер столбца с суммой:')
                if column_amount:
                    column_amount = int(column_amount)
                else:
                    raise Exception(f'Конфликт! Номер столбца для импорта суммы не указан')
            else:
                column_amount = None

            percent: str | None = input('\nПроцент повторяющихся id от общего кол-ва строк (опционально):')

            percent = int(percent) if percent else None

            user_id_type: str | None | int = input(
                "\nВведите тип id(1-обычный id('7cf6962da1fc43f4b2fbe8fc53816190'),"
                " 2-длинный(в четыре раза длиннее обычного),"
                " 3-числовой(124125215)):"
                "!ПО ДЕФОЛТУ БУДЕТ ВЫБРАН ОБЫЧНЫЙ!"
            )
            if user_id_type:
                if not isinstance(user_id_type, ExIdType):
                    raise Exception(f'Вы ввели неверное значение. Данного значения нет в списке типов')
            else:
                user_id_type = '1'

            formatted_data_list: list = [
                {
                    'file_name': report_file,
                    'column_count': column_count,
                    'column_amount': column_amount,
                    'id_type': user_id_type,
                    'percent': percent,
                    'max_count': max_count,
                    'max_amount': max_amount

                } for report_file in files_list
            ]

            with Pool(processes=threads) as executor:
                tasks_result: list = executor.map(start_random_user_id, formatted_data_list)
        case 2:
            description_column: str | None | int = input('\nВведите номер столбца с описанием:')

            if description_column:
                description_column = int(description_column)
            else:
                raise Exception(f'Конфликт! Номер столбца для импорта описания не указан')

            save_column: str | None | int = int(input('\nВведите номер столбца в который нужно сохранять:'))

            if save_column:
                save_column = int(save_column)
            else:
                raise Exception(f'Конфликт! Номер столбца для сохранения кол-ва не указан')

            formatted_data_list: list = [
                {
                    'file_name': report_file,
                    'description_column': description_column,
                    'save_column': save_column,
                    'incorrect_keywords_list': incorrect_keywords_list,
                    'true_keywords_list': true_keywords_list,

                } for report_file in files_list
            ]

            with Pool(processes=threads) as executor:
                tasks_result: list = executor.map(validate_count_product, formatted_data_list)
        case 3:
            ex_id_column: str | None | int = input('\nВведите номер столбца с внешним идентификатор:')

            if ex_id_column:
                description_column = int(ex_id_column)
            else:
                raise Exception(f'Конфликт! Номер столбца для импорта с внешним идентификатор не указан')

            save_column: str | None | int = int(input('\nВведите номер столбца в который нужно сохранять:'))

            if save_column:
                save_column = int(save_column)
            else:
                raise Exception(f'Конфликт! Номер столбца для сохранения кол-ва не указан')

            user_id_type: str | None = input(
                "\nВведите тип id(1-обычный id('7cf6962da1fc43f4b2fbe8fc53816190'),"
                " 2-длинный(в четыре раза длиннее обычного),"
                " 3-числовой(124125215)):"
                "!ПО ДЕФОЛТУ БУДЕТ ВЫБРАН ОБЫЧНЫЙ!"
            )
            if user_id_type:
                if not(ExIdType.BASE_ID.value == user_id_type or
                       ExIdType.LONG_ID.value == user_id_type or
                       ExIdType.DIGIT_ID.value == user_id_type):
                    raise Exception(f'Вы ввели неверное значение. Данного значения нет в списке типов')
            else:
                user_id_type = '1'

            formatted_data_list: list = [
                {
                    'file_name': report_file,
                    'save_column': save_column,
                    'ex_id': ex_id_column,
                    'id_type': user_id_type

                } for report_file in files_list
            ]

            with Pool(processes=threads) as executor:
                tasks_result: list = executor.map(start_set_user_id_for_ex_id, formatted_data_list)
