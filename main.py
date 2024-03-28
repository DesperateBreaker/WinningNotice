import datetime
import game

cur_date = datetime.date.today()

weekday = cur_date.weekday() + 1        # 星期一: 1  ...  星期日: 7

lotto_weekday = [1, 3, 6]                  # lotto 开奖日
ball_weekday = [2, 4, 7]                   # ball  开奖日

my_lotto_num1 = [4, 13, 16, 18, 23, 6, 11]
my_lotto_num2 = [5,  8, 10, 20, 23, 2,  7]
my_ball_num1 = [4, 7, 11, 16, 26, 31, 7]
my_ball_num2 = [3, 4,  7,  8, 24, 28, 4]

today_num = [10, 13, 15, 17, 19, 31, 7]


p_game1 = game.lottogame()
p_game2 = game.ballgame()

p_game1.set_my_num(today_num)
p_game2.set_my_num(today_num)

p_game1.set_today_num(today_num)
p_game2.set_today_num(today_num)


num1 = p_game1.get_proparea_num()
num2 = p_game1.get_backarea_num()
p_game1.calc_winning_level(len(num1), len(num2))

num3 = p_game2.get_proparea_num()
num4 = p_game2.get_backarea_num()


print(weekday)

