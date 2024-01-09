import uuid

import openpyxl

from utils import logger


class SetUserIdAtExID:

    def __init__(self, source_data):

        self.user_ex_id_dict = None
        self.file_name = source_data['file_name']
        self.save_column = source_data['save_column']
        self.ex_id = source_data['ex_id']
        self.workbook = None
        self.sheet = None

    async def initial_process(self):
        try:
            self.workbook = openpyxl.load_workbook(self.file_name, data_only=True,
                                                   keep_links=False)
            self.sheet = self.workbook.active
        except Exception as err:
            logger.error(f'Ошибка обработки файла {self.file_name}: {err}')
        else:
            logger.success(f'Файл {self.file_name} успешно обработан. Кол-во строк: {self.sheet.max_row}')

    async def start_validate(self):
        self.user_ex_id_dict = {}
        await self.initial_process()
        await self.start_process()
        await self.save_process()
        return True

    async def start_process(self):
        for row in range(2, self.sheet.max_row + 1):
            user_ex_id = int(self.sheet.cell(row=row, column=5).value)

            if self.user_ex_id_dict.get(user_ex_id):
                uuids_user_id = self.user_ex_id_dict[user_ex_id]
            else:
                uuids_user_id = uuid.uuid4().__str__().replace('-', '')
                self.user_ex_id_dict[user_ex_id] = uuids_user_id

            self.sheet.cell(row=row, column=self.save_column).value = uuids_user_id

    async def save_process(self):
        self.workbook.save(f'{self.file_name.replace(".xlsx", "")}_patch.xlsx')
