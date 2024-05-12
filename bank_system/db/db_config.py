from dotenv import dotenv_values


def load_db_confing():
    return dotenv_values()


if __name__ == '__main__':
    print(load_db_confing())
