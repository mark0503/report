from multiprocessing.dummy import Pool

from core import start_random_user_id, validate_count_product, start_set_user_id_for_ex_id
from utils import logger

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
                                 '3. Связка с внешним id\n'
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

            need_long_id = input('\nНужен ли длинный id обычно для ТКС используют(опционально),'
                                 ' если нужен введите "1":')

            formatted_data_list: list = [
                {
                    'file_name': report_file,
                    'column_count': column_count,
                    'column_amount': column_amount,
                    'need_long_id': need_long_id,
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
            ex_id_column: str | None | int = input('\nВведите номер столбца с внешним id:')

            if ex_id_column:
                description_column = int(ex_id_column)
            else:
                raise Exception(f'Конфликт! Номер столбца для импорта с внешним id не указан')

            save_column: str | None | int = int(input('\nВведите номер столбца в который нужно сохранять:'))

            if save_column:
                save_column = int(save_column)
            else:
                raise Exception(f'Конфликт! Номер столбца для сохранения кол-ва не указан')

            formatted_data_list: list = [
                {
                    'file_name': report_file,
                    'save_column': save_column,
                    'ex_id': ex_id_column

                } for report_file in files_list
            ]

            with Pool(processes=threads) as executor:
                tasks_result: list = executor.map(start_set_user_id_for_ex_id, formatted_data_list)
