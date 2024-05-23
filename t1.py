from bank_system.db import db_queries as q


def filter(table_name, **kwargs):
    query = q.ALL.format(table_name)
    params = []
    filter_list = []
    if kwargs:
        for k, v in kwargs.items():
            if isinstance(v, tuple) and len(v) == 2:
                min_amount = v[0]
                max_amount = v[1]
                if min_amount and max_amount:
                    filter_list.append(f"ABS({k}) BETWEEN %s AND %s OR {k} BETWEEN %s AND %s")
                    params.append(min_amount)
                    params.append(max_amount)
                elif min_amount:
                    filter_list.append(f'{k} > %s')
                elif max_amount:
                    filter_list.append(f'{k} < %s')
            else:
                filter_list.append(q.BY_COLUMN.format(k))
                params.append(v)
        query += q.WHERE + q.AND.join(filter_list) + ' ORDER BY ABS(amount)'
        print(query)
        input()
    # with self.db_manager as cursor:
    #     cursor.execute(query, params)
    #     records = cursor.fetchall()
    #     if records:
    #         return [self.model_class(**record) for record in records]


filter(table_name='tranactions', amount=(None, 3), transaction_type='deposit')
