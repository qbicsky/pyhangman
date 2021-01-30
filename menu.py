from enum import Enum
from colors import Color


class MenuItem:
    def __init__(self, keyword, label: str, description: str = str(), alt_key=None):
        self.keyword = keyword
        self.item = {
            keyword: {
                'label': label,
                'description': description,
                'alternative key': alt_key
            }
        }


class Menu():
    def __init__(self, menu_item_list, menu_name='Generic Menu'):
        self.name = menu_name
        self.menu_dictionary = dict()

        for menu_item in menu_item_list:

            self.menu_dictionary.update(menu_item.item)

    def __getitem__(self, key):
        return self.menu_dictionary.get(key)

    def __str__(self):
        return str(self.menu_dictionary)

    def __len__(self):
        return len(self.getkeys())

    def dictionary(self):
        return self.menu_dictionary

    def getlabels(self):
        return [
            self[key].get('label')
            for key in self.dictionary()
        ]

    def getkeys(self, mode=None):
        """
        Return array of keys in Menu.

        Args:
            mode (str, optional): int -> keys are forced integers.
                                  str -> keys are forced strings.
                                  Defaults to None -> no enforced type.
        """
        if(mode == 'int'):
            return [int(key) for key in self.dictionary()]
        elif(mode == 'str'):
            return [str(key) for key in self.dictionary()]
        else:
            return [key for key in self.dictionary()]

    def key_by_label(self, label):
        Main_Menu = Enum(self.name, {
            self.menu_dictionary.get(key).get('label'): key
            for key in self.menu_dictionary})
        return Main_Menu[label].value

    def label_by_key(self, key):
        return self.dictionary().get(key).get('label')

    def get_desc_by_key(self, key):
        return self.dictionary().get(key).get('description')

    def build_list(self, align='vertical', descr=False, alt=False):
        menu_list = list()
        description_string = str()
        for key in self.getkeys():
            alt_key = self.dictionary().get(key).get('alternative key')
            if(alt is True and alt_key is not None):
                keystr = str(alt_key)
            else:
                keystr = str(key)
            if(descr is True):
                description_string = '.  ' + self.get_desc_by_key(key)
            else:
                description_string = '  '
            menu_list.append(Color.END + '[' + keystr + '] ' + Color.DARKGREY
                             + self.label_by_key(key)
                             + description_string + Color.END)
        if(align == 'horizontal'):
            menu_list = ''.join(menu_list)
        return menu_list
