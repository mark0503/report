import random

from base import BaseProcessor
from utils import logger
from utils.generate_ex_id import generate_id_of_type


class RandomUserId(BaseProcessor):

    def start_validate(self):
        self.initial_process()
        self.start_process()
        if self.percent:
            self.shuffle_process()
        else:
            self.state['result_list'] = self.state['initial_list']
        self.save_process()
        return True

    def start_process(self):
        process_count = 0
        logger.info(f'начинаем преобразовывать данные под свою структуру.')
        for row in range(2, self.sheet.max_row + 1):
            if self.column_amount:
                product_amount = float(self.sheet.cell(row=row, column=self.column_amount).value)
            else:
                product_amount = None

            if self.count_column:
                product_count = float(self.sheet.cell(row=row, column=self.count_column).value)
            else:
                product_count = None
            new_user_id = generate_id_of_type(self.id_type)

            self.state['initial_list'].append({
                'product_amount': product_amount,
                'row': row,
                'product_count': product_count,
                'new_user_id': new_user_id
            })
            process_count += 1

    def shuffle_process(self):
        random.shuffle(self.state['initial_list'])
        index_of_percent = int(self.percent / 100 * len(self.state['initial_list']))

        initial_list_12 = self.state['initial_list'][:index_of_percent]
        initial_list_88 = self.state['initial_list'][index_of_percent:]
        result_list = []
        for elem in initial_list_12:
            if self.max_amount and elem['product_amount'] > self.max_amount:
                continue
            if self.max_count and elem['product_count'] > self.max_count:
                continue
            for _ in range(500):
                elem_from_85 = random.choice(initial_list_88)

                if self.max_count:
                    sum_count = elem['product_count'] + elem_from_85['product_count']
                    if sum_count > self.max_count:
                        continue
                if self.max_amount:
                    sum_amount = elem['product_amount'] + elem_from_85['product_amount']
                    if sum_amount > self.max_count:
                        continue
                elem['new_user_id'] = elem_from_85['new_user_id']
                initial_list_88.remove(elem_from_85)
                result_list.append(elem)
                break
        self.state['result_list'] = initial_list_12 + self.state['initial_list'][index_of_percent:]
