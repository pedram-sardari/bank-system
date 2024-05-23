import inspect
import os
import pathlib
import time
from typing import Self, Union, List, Tuple, Dict, Callable


class Action:
    def __init__(self, name: str, description: str, level: Tuple, func: Callable):
        self.name = name
        self.description = description
        self.level = level
        self.func = func

    def __call__(self, menu_variables):
        print()
        return self.func(menu_variables)

    @classmethod
    def generate_list_of_actions_from_local_namespace(cls, local_namespace) -> Dict[str, Self]:
        action_list = {}
        for func_name, func in local_namespace.items():
            name, level = func_name.split('__')
            level = tuple(level.split('_'))
            name = name.strip('_').replace('_', ' ')
            if inspect.isfunction(func):
                description = inspect.getdoc(func)
                action = Action(name, description, level, func=func)
                order_number = level[-1]
                action_list[order_number] = action
            # sort action_list by the order_number(key)
            action_list = dict(sorted(list(action_list.items())))

        return action_list


class Menu:
    menu_variables = {
        'user_manager': 1,
        'account_manager': 'obj'
    }

    def __init__(self, name: str, description: str, level: Tuple, go_back_keyword: str):
        self.name = name
        self.description = description
        self.level = level
        self.go_back_keyword = go_back_keyword
        self.item_list: Dict[str, Union[Self, Action, Tuple[Action, Self]]] = {}

    @classmethod
    def set_menu_variables(cls, menu_variables: dict):
        cls.menu_variables = menu_variables

    @staticmethod
    def clear_screen():
        os.system('cls' if os.name == 'nt' else 'clear')

    @staticmethod
    def print_msg(msg):
        print(f"\033[92m{msg}\033[m")

    def __call__(self, msg=''):
        """print menus and call the choice"""
        Menu.print_msg(msg)
        input('\npress enter to continue... ')
        Menu.clear_screen()
        self._display_menu()
        choice = input('\n\033[94mYour Choice: \033[0m')  # TODO: choice validation
        Menu.clear_screen()
        if choice == '0':
            return
        try:
            self._call_chosen_item(choice)
        except Exception as e:
            print(f"\n\033[91m{str(e)}\033[0m")
            # raise
            self()

    def _display_menu(self):
        print()
        for order_number, item in self.item_list.items():
            if isinstance(item, Tuple):
                action: Action = item[0]
                print(f"{order_number}. {action.name}".ljust(15), f"\t({action.description})")
            elif isinstance(item, Menu) or isinstance(item, Action):
                print(f"{order_number}. {item.name}".ljust(15), f"\t({item.description})")
            else:
                raise TypeError
        print(f"0. {self.go_back_keyword}")

    def _call_chosen_item(self, choice):
        if item := self.item_list.get(choice):
            if isinstance(item, Tuple):
                msg = item[0](self.menu_variables)  # action call
                item[1](msg)  # menu call
                msg = item[1].go_back_keyword
            elif isinstance(item, Menu):
                item()
                msg = item.go_back_keyword
            elif isinstance(item, Action):
                msg = item(self.menu_variables)
            else:
                raise TypeError
            # Menu.print_msg(msg)
            self(msg)
        else:
            raise ValueError('invalid choice')

    @classmethod
    def generate_menu_from_local_namespace(cls, menu_path, local_namespace) -> Self:
        name, level = menu_path.name.replace('.py', '').split('__')
        level = tuple(level.split('_'))
        name = name.strip('_').replace('_', ' ')
        description = local_namespace.pop('__doc__')
        go_back_keyword = local_namespace.pop('go_back_keyword')
        return Menu(name, description, level, go_back_keyword)

    def print_tree(self):
        pass


class MenuGenerator:

    def __init__(self, menu_directory_path='menus_list'):
        self.menu_directory_path = menu_directory_path
        self.menus_list: List[Menu] = []

    def get_menus_file_name(self) -> List[pathlib.Path]:
        menu_paths = []
        for menu_file_name in os.listdir(self.menu_directory_path):
            if menu_file_name != '__init__.py':
                menu_file_path = os.path.join(self.menu_directory_path, menu_file_name)
                if os.path.isfile(menu_file_path):
                    menu_paths.append(pathlib.Path(menu_file_path))

        return menu_paths

    @staticmethod
    def get_local_namespace(menu_path) -> Dict[str, any]:
        """get the menu module local namespace"""
        with menu_path.open('r') as f:
            menu_file_content = f.read()
            local_namespace: Dict[str, any] = {}
            exec(menu_file_content, globals(), local_namespace)

        return local_namespace

    def _fill_menus_list(self):
        menu_paths = self.get_menus_file_name()
        for menu_path in menu_paths:
            local_namespace = MenuGenerator.get_local_namespace(menu_path)
            menu = Menu.generate_menu_from_local_namespace(menu_path, local_namespace)
            menu.item_list = Action.generate_list_of_actions_from_local_namespace(local_namespace)
            self.menus_list.append(menu)

    def create_composite_menu(self):
        self._fill_menus_list()
        # 1, 1_1, 1_3, 1_4, 1_2, 1_4_1, 1_4_2
        self.menus_list.sort(key=lambda menu_obj: len(menu_obj.level))

        while len(self.menus_list) > 1:
            sub_menu = self.menus_list.pop()
            candidate_super_menu_list = (menu for menu in self.menus_list
                                         if len(menu.level) == len(sub_menu.level) - 1)
            for candidate_super_menu in candidate_super_menu_list:
                order_number = sub_menu.level[-1]
                if candidate_super_menu.level[-1] == sub_menu.level[-2]:  # if this is a submenu in super-menu
                    # if this is an action-submenu item in super-menu
                    if action := candidate_super_menu.item_list.get(order_number):
                        if isinstance(action, Action) and action.level == sub_menu.level:
                            candidate_super_menu.item_list[order_number] = (action, sub_menu)
                    else:  # if this is a simple submenu
                        candidate_super_menu.item_list[order_number] = sub_menu
                    break
            else:
                raise ValueError(f"Submenu '{sub_menu.name}' has no super menu!")

        return self.menus_list.pop()  # root menu

    def __call__(self, *args, **kwargs) -> Menu:
        return self.create_composite_menu()


if __name__ == '__main__':
    m = MenuGenerator()
    menu_root = m.create_composite_menu()
    menu_root()
