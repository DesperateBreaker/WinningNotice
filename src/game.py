# game object
from abc import ABC, abstractmethod

# ball_rule_dict
# key: score    value: level
# score = prop_num * 1 + back_num * 10
ball_rule_dict = {
    16: 1,
    6: 2,
    15: 3,
    5: 4,
    14: 4,
    4: 5,
    13: 5,
    10: 6,
    11: 6,
    12: 6
}

# lotto_rule_dict
# key: score    value: level
# score = prop_num * 1 + back_num * 10
lotto_rule_dict = {
    25: 1,
    15: 2,
    5: 3,
    24: 4,
    14: 5,
    23: 6,
    4: 7,
    13: 8,
    22: 8,
    3: 9,
    12: 9,
    21: 9
}


# base class
class Game:
    @abstractmethod
    def __init__(self):
        self.id = 0
        self.name = ""
        self._today_num_list = [0] * 7
        self._my_num_list = [0] * 7
        self._rule_dict = {}
        self._prop_num = 0
        self._back_num = 0
        self._win_money_list = []

    def set_my_num(self, my_num):
        for index, value in enumerate(my_num):
            self._my_num_list[index] = value

    def set_today_num(self, today_num, id=0):
        for index, value in enumerate(today_num):
            self._today_num_list[index] = value
        self.id = id

    def get_proparea_num(self):
        pass

    def get_backarea_num(self):
        pass

    def calc_winning_level(self, prop_num, back_num):
        key = prop_num + 10 * back_num
        return self._rule_dict.get(key, 0)

    def crate_win_info(self):
        notice_dict = {
            "name": "",
            "id": 0,
            "today_num": [],
            "my_num": [],
            "prop_num": [],
            "prop_status": "",
            "back_num": [],
            "back_status": "",
            "win_level": 0,
            "win_money": 0,
        }

        notice_dict["name"] = self.name
        notice_dict["id"] = self.id
        notice_dict["today_num"] = self._today_num_list
        notice_dict["my_num"] = self._my_num_list

        prop_win_num = self.get_proparea_num()
        notice_dict["prop_num"] = prop_win_num
        notice_dict["prop_status"] = str(len(prop_win_num)) + " / " + str(self._prop_num)

        back_win_num = self.get_backarea_num()
        notice_dict["back_num"] = back_win_num
        notice_dict["back_status"] = str(len(back_win_num)) + " / " + str(self._back_num)

        win_level = self.calc_winning_level(len(prop_win_num), len(back_win_num))
        notice_dict["win_level"] = win_level
        notice_dict["win_money"] = self._win_money_list[win_level]

        return notice_dict


# ballgame:  6 + 1
class BallGame(Game):
    def __init__(self):
        super().__init__()
        self.name = "ball"
        self._prop_num = 6
        self._back_num = 1
        self._rule_dict = ball_rule_dict
        self._win_money_list = [0, 5000000, 200000, 3000, 200, 10, 5]  # key: win_level value: win_money

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
class LottoGame(Game):
    def __init__(self):
        super().__init__()
        self.name = "lotto"
        self._prop_num = 5
        self._back_num = 2
        self._rule_dict = lotto_rule_dict
        self._win_money_list = [0, 10000000, 200000, 10000, 3000, 300, 200, 100, 15, 5]  # key: win_level value: win_money

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
