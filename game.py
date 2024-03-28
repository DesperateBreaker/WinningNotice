# game object
from abc import ABC, abstractmethod

# base class
class game:
    @abstractmethod
    def __init__(self):
        self.id = 0
        self._today_num_list = [0] * 7
        self._my_num_list = [0] * 7
        self._rulue_dict = {}

    def set_my_num(self, my_num):
        for index, value in enumerate(my_num):
            self._my_num_list[index] = value

    def set_today_num(self, today_num):
        for index, value in enumerate(today_num):
            self._today_num_list[index] = value

    def get_proparea_num(self):
        pass

    def get_backarea_num(self):
        pass

    def calc_winning_level(self, prop_num, back_num):
        key = prop_num + 10 * back_num
        if key in self._rulue_dict:
            level = self._rulue_dict[key]
        else:
            level = 0
        
        return level


# ballgame:  6 + 1
class ballgame(game):
    def __int__(self):
        __super().__init(self)
        self._rulue_dict = {16: 1, 6: 2, 15: 3, 5: 4, 14: 4, 4: 5, 13: 5, 10: 6, 11: 6, 12: 6}          # rule: prop_num * 1 + back_num * 10

    def get_proparea_num(self):
        pro_num = self._today_num_list[0:-1]
        win_num = []
        for i in range(6):
            if self._my_num_list[i] in pro_num:
                win_num.append(self._my_num_list[i])

        return win_num

    def get_backarea_num(self):
        win_num = []
        if self._my_num_list[6] == self._today_num_list[6]:
            win_num.append(self._my_num_list[6])

        return win_num


# lottogame:  5 + 2
class lottogame(game):
    def __int__(self):
        __super().__init(self)
        self._rulue_dict = {25: 1, 15: 2, 5: 3, 24: 4, 14: 5, 23: 6, 4: 7, 13: 8, 22: 8, 3: 9, 12: 9, 21: 9}          # rule: prop_num * 1 + back_num * 10

    def get_proparea_num(self):
        pro_num = self._today_num_list[0:-2]
        win_num = []
        for i in range(5):
            if self._my_num_list[i] in pro_num:
                win_num.append(self._my_num_list[i])

        return win_num

    def get_backarea_num(self):
        back_num = self._today_num_list[-2:]
        win_num = []
        for i in range(5, 7):
            if self._my_num_list[i] in back_num:
                win_num.append(self._my_num_list[i])

        return win_num
        