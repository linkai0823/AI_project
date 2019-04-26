import numpy as np
import re
import random

# 获得一个新棋盘，黑手做花月开局，白手正常守态。做映射优先队列分数在队列中 可下点映射分数以分数排位，队列数为2一个为攻击点 一个为防守点，每次获得新点后
# 更新改点以及周围9*9的可下点数据 做分数评估挑选

#########################################################
# 方法设定

# 1.确定下子位置/我方落子得分/对方落子得分

# 2.匹配 我方对方棋型 得到点进攻分数 防守分数。四个方向匹配分数记录分数

# 3.判断位置是否在已有记录中 在已有记录则更新

# 4.遍历9*9中的空点类推

# 5。找到最大得分点

# 评分细则  1.具体棋型 2.向棋盘中心的分数递增3.一定范围内我方旗子和对方棋子的数目差4.我方棋子密集程度 1+2+3*4
COLOR_BLACK = -1
COLOR_WHITE = 1
COLOR_NONE = 0
find_black_5 = ['22222']
find_whit_5 = ['11111']
find_black_4 = ['022220']
find_whit_4 = ['011110']
find_black_poor_4 = ['022221', '122220', '22022', '20222', '22202']
find_whit_poor_4 = ['011112', '211110', '11011', '10111', '11101']
find_black_3 = ['002220', '022200', '022020', '020220']
find_whit_3 = ['001110', '011100', '011010', '010110']
find_black_poor_3 = ['122200', '002221', '022021', '020221', '122020', '120220', '20022',
                     '22002', '20202', '1022201']
find_whit_poor_3 = ['211100', '001112', '011012', '010112', '211010', '210110', '10011', '11001', '10101',
                    '2011102']
find_black_2 = ['02200', '00220', '0020200']  #
find_whit_2 = ['01100', '00110', '0010100']  #
find_black_poor_2 = ['000221', '122000', '002021', '120200', '0020021', '1200200', '0200020']
find_whit_poor_2 = ['000112', '211000', '001012', '210100', '010012', '210010', '0100010']
mode_goal = [0] * 7


# (1)寻找棋型
def mode(color, list_give):
    if color == -1:
        for i in find_black_5:
            if re.search(i, list_give):
                mode_goal[0] += 1
                return
        for i in find_black_4:
            if re.search(i, list_give):
                mode_goal[1] += 1
                return
        for i in find_black_poor_4:
            if re.search(i, list_give):
                mode_goal[2] += 1
                return
        for i in find_black_3:
            if re.search(i, list_give):
                mode_goal[3] += 1
                return
        for i in find_black_poor_3:
            if re.search(i, list_give):
                mode_goal[4] += 1
                return
        for i in find_black_2:
            if re.search(i, list_give):
                mode_goal[5] += 1
                return
        for i in find_black_poor_2:
            if re.search(i, list_give):
                mode_goal[6] += 1
                return
    else:
        for i in find_whit_5:
            if re.search(i, list_give):
                mode_goal[0] += 1
                return
        for i in find_whit_4:
            if re.search(i, list_give):
                mode_goal[1] += 1
                return
        for i in find_whit_poor_4:
            if re.search(i, list_give):
                mode_goal[2] += 1
                return
        for i in find_whit_3:
            if re.search(i, list_give):
                mode_goal[3] += 1
                return
        for i in find_whit_poor_3:
            if re.search(i, list_give):
                mode_goal[4] += 1
                return
        for i in find_whit_2:
            if re.search(i, list_give):
                mode_goal[5] += 1
                return
        for i in find_whit_poor_2:
            if re.search(i, list_give):
                mode_goal[6] += 1
                return
    # （2）获得四个方向旗子


def find_goal(chessboard, row, columd, color, fuck, go_long):
    if color == -1:
        color_use = 2
    else:
        color_use = 1
    row_list = str(color_use)
    # 横向
    # left
    zero_point = 0
    if columd >= 4:
        left_bound = 5
    else:
        left_bound = columd + 1
    for i in range(1, left_bound):
        if chessboard[row][columd - i] == -color:
            row_list = str(3 - color_use) + row_list
            break
        if chessboard[row][columd - i] == color:
            row_list = str(color_use) + row_list

            zero_point = 0
            continue
        if chessboard[row][columd - i] == 0:
            if zero_point == 3:
                break
            row_list = '0' + row_list
            zero_point += 1
    if columd - left_bound == -1:
        row_list = str(3 - color_use) + row_list
    # right
    zero_point = 0
    if columd <= 10:
        right_bound = 5
    else:
        right_bound = 15 - columd
    for i in range(1, right_bound):
        if chessboard[row][columd + i] == -color:
            row_list = row_list + str(3 - color_use)
            break
        if chessboard[row][columd + i] == color:
            row_list = row_list + str(color_use)
            zero_point = 0
            continue
        if chessboard[row][columd + i] == 0:
            if zero_point == 3:
                break
            row_list = row_list + '0'
            zero_point += 1
    if columd + right_bound == 15:
        row_list = row_list + str(3 - color_use)
    # 得到完整一行形式进行判断

    # 纵向
    columd_list = str(color_use)

    # left
    zero_point = 0
    if row >= 4:
        left_bound = 5
    else:
        left_bound = row + 1
    for i in range(1, left_bound):
        if chessboard[row - i][columd] == -color:
            columd_list = str(3 - color_use) + columd_list
            break
        if chessboard[row - i][columd] == color:
            columd_list = str(color_use) + columd_list
            zero_point = 0
            continue
        if chessboard[row - i][columd] == 0:
            if zero_point == 3:
                break
            columd_list = '0' + columd_list
            zero_point += 1
    if row - left_bound == -1:
        columd_list = str(3 - color_use) + columd_list
    # right
    zero_point = 0
    if row <= 10:
        right_bound = 5
    else:
        right_bound = 15 - row
    for i in range(1, right_bound):
        if chessboard[row + i][columd] == -color:
            columd_list = columd_list + str(3 - color_use)
            break
        if chessboard[row + i][columd] == color:
            columd_list = columd_list + str(color_use)
            zero_point = 0
            continue
        if chessboard[row + i][columd] == 0:
            if zero_point == 3:
                break
            columd_list = columd_list + '0'
            zero_point += 1
    if row + right_bound == 15:
        columd_list = columd_list + str(3 - color_use)
    # 得到完整一行形式进行判断

    # /向
    right_up_list = str(color_use)
    # left
    zero_point = 0
    if columd >= 4 and row <= 10:
        left_bound = 5
    else:
        left_bound = min(columd + 1, 15 - row)

    for i in range(1, left_bound):
        if chessboard[row + i][columd - i] == -color:
            right_up_list = str(3 - color_use) + right_up_list
            break
        if chessboard[row + i][columd - i] == color:
            right_up_list = str(color_use) + right_up_list
            zero_point = 0
            continue
        if chessboard[row + i][columd - i] == 0:
            if zero_point == 3:
                break
            right_up_list = '0' + right_up_list
            zero_point += 1
    if left_bound + row == 15 or left_bound - columd == 1:
        right_up_list = str(3 - color_use) + right_up_list
    # right
    zero_point = 0
    if columd <= 10 and row >= 4:
        right_bound = 5
    else:
        right_bound = min(15 - columd, row + 1)
    for i in range(1, right_bound):
        if chessboard[row - i][columd + i] == -color:
            right_up_list = right_up_list + str(3 - color_use)
            break
        if chessboard[row - i][columd + i] == color:
            right_up_list = right_up_list + str(color_use)
            zero_point = 0
            continue
        if chessboard[row - i][columd + i] == 0:
            if zero_point == 3:
                break
            right_up_list = right_up_list + '0'
            zero_point += 1
    if left_bound + columd == 15 or left_bound - row == 1:
        right_up_list = right_up_list + str(3 - color_use)
    # 得到完整一行形式进行判断

    # \向
    right_down_list = str(color_use)
    # left
    zero_point = 0
    if columd >= 4 and row >= 4:
        left_bound = 5
    else:
        left_bound = min(row + 1, columd + 1)
    for i in range(1, left_bound):
        if chessboard[row - i][columd - i] == -color:
            right_down_list = str(3 - color_use) + right_down_list
            break
        if chessboard[row - i][columd - i] == color:
            right_down_list = str(color_use) + right_down_list
            zero_point = 0
            continue
        if chessboard[row - i][columd - i] == 0:
            if zero_point == 3:
                break
            right_down_list = '0' + right_down_list
            zero_point += 1
    if left_bound - row == 1 or left_bound - columd == 1:
        right_down_list = str(3 - color_use) + right_down_list
    # right
    zero_point = 0
    if columd <= 10 and row <= 10:
        right_bound = 5
    else:
        right_bound = min(15 - columd, 15 - row)
    for i in range(1, right_bound):
        if chessboard[row + i][columd + i] == -color:
            right_down_list = right_down_list + str(3 - color_use)
            break
        if chessboard[row + i][columd + i] == color:
            right_down_list = right_down_list + str(color_use)
            zero_point = 0
            continue
        if chessboard[row + i][columd + i] == 0:
            if zero_point == 3:
                break
            right_down_list = right_down_list + '0'
            zero_point += 1
    if left_bound + row == 15 or left_bound + columd == 15:
        right_down_list = right_down_list + str(3 - color_use)

    # 得到完整一行形式进行判断
    # 对四个做同时判断
    for i in range(7):
        mode_goal[i] = 0
    mode(color, row_list)

    mode(color, columd_list)

    mode(color, right_up_list)

    mode(color, right_down_list)

    # 0 5 , 1 4 , 2 p4 ,3 3 ,4 p3,5 2, 6 p2
    ok2 = random.random()
    ok1 = random.random()

    if fuck == -1:
        while 1:
            if mode_goal[0] >= 1:
                goal_sum = 100000
                break

            if mode_goal[1] >= 1:
                if mode_goal[2] > 0:
                    goal_sum = 30000 + 3000 * mode_goal[2]
                    break
                if mode_goal[3] > 0:
                    goal_sum = 30000 + 2000 * mode_goal[3]
                    break
                if mode_goal[4] > 0:
                    goal_sum = 30000 + 1000 * mode_goal[4]
                    break
                if mode_goal[5] > 0:
                    goal_sum = 30000 + 400 * mode_goal[5]
                    break
                if mode_goal[6] > 0:
                    goal_sum = 30000 + 50 * mode_goal[6]
                    break
                goal_sum = 30000
                break

            if mode_goal[2] >= 2:
                goal_sum = 30000
                break
            if mode_goal[2] >= 1 and mode_goal[3] >= 1:
                goal_sum = 30000
                break
            if mode_goal[3] >= 2:
                goal_sum = 15000
                break
            if mode_goal[2] >= 1 and mode_goal[4] >= 2:  # 3 #1
                goal_sum = 14500
                break
            if mode_goal[2] >= 1 and mode_goal[5] >= 2:
                goal_sum = 14000
                break
            if mode_goal[3] >= 1 and mode_goal[4] >= 2:  # 3 #2
                goal_sum = 13500
                break
            if mode_goal[3] >= 1 and mode_goal[4] >= 1 and mode_goal[5] >= 1:
                goal_sum = 13000
                break
            if mode_goal[3] >= 1 and mode_goal[5] >= 2:  # 4
                goal_sum = 12800
                break

            if mode_goal[2] >= 1:
                if mode_goal[5] >= 1:
                    goal_sum = 6000
                    break
            if mode_goal[2] >= 1:

                if mode_goal[4] >= 1:
                    goal_sum = 4000
                    break
            if mode_goal[3] >= 1 and mode_goal[5] >= 1:
                goal_sum = 3500
                break
            if mode_goal[5] >= 3:  # 4
                goal_sum = 2000
                break
            if mode_goal[3] >= 1 and mode_goal[4] >= 1:
                goal_sum = 1000
                break
            if mode_goal[3] >= 1 and mode_goal[6] >= 2:
                goal_sum = 500
                break



            if mode_goal[3] >= 1 and mode_goal[6] >= 1:
                goal_sum = 240
                break
            if mode_goal[5] >= 2 and mode_goal[6] >= 1:  # 5
                goal_sum = 200
                break

            if mode_goal[3] >= 1 :
                goal_sum = 195
                break
            if mode_goal[5] >= 2:
                goal_sum = 190
                break
            if mode_goal[2] >= 1 and mode_goal[6] >= 1:
                goal_sum = 195
                break

            if mode_goal[5] >= 1 and mode_goal[6] >= 1:
                goal_sum = 100
                break
            if mode_goal[5] >= 1 :
                goal_sum = 90
                break
            if mode_goal[4] >= 1 :
                goal_sum = 50
                break

            if mode_goal[6] >= 1:
                goal_sum = -2
                break
            if mode_goal[2] >= 1 :
                goal_sum = 150
                break
            if mode_goal[4] >= 1 :
                goal_sum = 50
                break
            goal_sum = 1
            break

    if fuck == 1:
        while 1:
            if mode_goal[0] >= 1:
                goal_sum = 100000
                break

            if mode_goal[1] >= 1:
                if mode_goal[2] > 0:
                    goal_sum = 30000 + 3000 * mode_goal[2]
                    break
                if mode_goal[3] > 0:
                    goal_sum = 30000 + 2000 * mode_goal[3]
                    break
                if mode_goal[4] > 0:
                    goal_sum = 30000 + 1000 * mode_goal[4]
                    break
                if mode_goal[5] > 0:
                    goal_sum = 30000 + 400 * mode_goal[5]
                    break
                if mode_goal[6] > 0:
                    goal_sum = 30000 + 50 * mode_goal[6]
                    break
                goal_sum = 30000
                break

            if mode_goal[2] >= 2:
                goal_sum = 30000
                break
            if mode_goal[2] >= 1 and mode_goal[3] >= 1:
                goal_sum = 30000
                break
            if mode_goal[3] >= 2:
                goal_sum = 15000
                break
            if mode_goal[2] >= 1 and mode_goal[4] >= 2:  # 3 #1
                goal_sum = 14500
                break
            if mode_goal[2] >= 1 and mode_goal[5] >= 2:
                goal_sum = 14000
                break
            if mode_goal[3] >= 1 and mode_goal[4] >= 2:  # 3 #2
                goal_sum = 13500
                break
            if mode_goal[3] >= 1 and mode_goal[4] >= 1 and mode_goal[5] >= 1:
                goal_sum = 13000
                break
            if mode_goal[3] >= 1 and mode_goal[5] >= 2:  # 4
                goal_sum = 12800
                break
            if mode_goal[2] >= 1:
                if mode_goal[5] >= 1:
                    goal_sum = 12000
                    break
                if mode_goal[4] >= 1:
                    goal_sum = 11500
                    break

            if mode_goal[2] >= 1 and ok2 > 0.05:
                goal_sum = 11000
                break
            if mode_goal[3] >= 1 and mode_goal[5] >= 1:
                goal_sum = 3500
                break
            if mode_goal[5] >= 3:  # 4
                goal_sum = 2000
                break
            if mode_goal[3] >= 1 and mode_goal[4] >= 1:
                goal_sum = 1000
                break
            if mode_goal[3] >= 1 and mode_goal[6] >= 2:
                goal_sum = 500
                break



            if mode_goal[3] >= 1 and mode_goal[6] >= 1:
                goal_sum = 240
                break
            if mode_goal[5] >= 2 and mode_goal[6] >= 1:  # 5
                goal_sum = 200
                break
            if mode_goal[5] >= 2:
                goal_sum = 195
                break

            if mode_goal[3] >= 1 and ok2 > 0.5:
                goal_sum = 185
                break

            if mode_goal[2] >= 1 and mode_goal[6] >= 1:
                goal_sum = 160
                break

            if mode_goal[5] >= 1 and mode_goal[6] >= 1:
                goal_sum = 100
                break
            if mode_goal[5] >= 1 and ok2 > 0.1:
                goal_sum = 95
                break
            if mode_goal[4] >= 1 and ok2 > 0.9:
                goal_sum = 50
                break

            if mode_goal[6] >= 1:
                goal_sum = -2
                break
            if mode_goal[2] >= 1 and ok2 > 0.9:
                goal_sum = 300
                break
            if mode_goal[4] >= 1 and ok2 > 0.9:
                goal_sum = 50
                break
            goal_sum = 1
            break
    # 添加棋盘中心度评分
    goal_sum += ((7 - max(abs(7 - row), abs(7 - columd))) / 2)
    # 添加旗子密集度
    return goal_sum


# don't change the class name
class AI(object):
    # chessboard_size, color, time_out passed from agent
    def __init__(self, chessboard_size, color, time_out):
        self.chessboard_size = chessboard_size
        # You are white or black
        self.color = color
        # the max time you should use, your algorithm's run time must not exceed the time limit.
        self.time_out = time_out
        # You need add your decision into your candidate_list. System will get the end of your candidate_list as your decision .
        self.candidate_list = []
        # 旧棋盘的记录

    # self.history = [[0 for i in range(chessboard_size)] for j in range(chessboard_size)]

    # If your are the first, this function will be used.
    def first_chess(self):
        assert self.color == COLOR_BLACK
        self.candidate_list.clear()
        # ==================================================================
        # Here you can put your first piece
        # for example, you can put your piece on sun（天元）
        self.candidate_list.append((self.chessboard_size // 2, self.chessboard_size // 2))
        self.chessboard[self.candidate_list[-1][0], self.candidate_list[-1][0]] = self.color

    # 1.找到下子位置
    def find_point(self, chessboard):
        find = chessboard - self.history
        for i in range(self.chessboard_size):
            for j in range(self.chessboard_size):
                if find[i][j] != 0:
                    return (i, j)

    # 2.匹配 我方对方棋型 得到点进攻分数 防守分数。四个方向匹配分数记录分数
    # 3.判断位置是否在已有记录中 在已有记录则更新
    # 做进攻得分 防守得分

    # The input is current chessboard.
    def go(self, chessboard):
        go_long = 0
        self.candidate_list.clear()

        for i in range(self.chessboard_size):
            for o in range(self.chessboard_size):
                if chessboard[i][o] == 0:
                    go_long += 1
        do = random.random() + ((225 - go_long) / 225)

        if go_long == 223 and self.color == -1:
            go_long = 0
            for i in range(self.chessboard_size):
                for o in range(self.chessboard_size):
                    if chessboard[i][o] == -1:
                        # 蒲月
                        if chessboard[i - 1][o - 1] == 1:
                            self.candidate_list.append((i + 1, o - 1))
                            return
                        if chessboard[i + 1][o - 1] == 1:
                            self.candidate_list.append((i - 1, o - 1))
                            return
                        if chessboard[i - 1][o + 1] == 1:
                            self.candidate_list.append((i + 1, o + 1))
                            return
                        if chessboard[i + 1][o + 1] == 1:
                            self.candidate_list.append((i - 1, o + 1))
                            return
                        # 花月
                        if chessboard[i - 1][o] == 1:
                            self.candidate_list.append((i - 1, o + 1))
                            return
                        if chessboard[i + 1][o] == 1:
                            self.candidate_list.append((i + 1, o + 1))
                            return
                        if chessboard[i][o - 1] == 1:
                            self.candidate_list.append((i + 1, o - 1))
                            return
                        if chessboard[i][o + 1] == 1:
                            self.candidate_list.append((i - 1, o + 1))
                            return
        if go_long == 224 and self.color == 1:
            for i in range(self.chessboard_size):
                for o in range(self.chessboard_size):
                    if chessboard[i][o] == -1:
                        self.candidate_list.append((i - 1, o + 1))
                        return
        self.candidate_list.clear()
        # ==================================================================
        # To write your algorithm here
        # Here is the simplest sample:Random decision
        old_goal = -1
        old_attack = 0
        for i in range(self.chessboard_size):
            for o in range(self.chessboard_size):
                if chessboard[i][o] == 0:
                    attact = find_goal(chessboard, i, o, self.color, 1, go_long)
                    defen = find_goal(chessboard, i, o, -self.color, -1, go_long)

                    if attact >= 100000:
                        self.candidate_list.append((i, o))
                        old_goal = 999999999999999
                        break

                    if defen >= 100000 and defen > old_goal:
                        self.candidate_list.append((i, o))
                        old_goal = 999999999999999
                        continue
                    if attact >= 30000 and attact > old_attack and old_goal < 100000:
                        self.candidate_list.append((i, o))
                        old_attack = attact
                        old_goal = attact + 60000
                        continue
                    if defen >= 30000 and defen > old_goal:
                        self.candidate_list.append((i, o))
                        old_goal = defen
                        continue
                    if attact >= 10000 and old_goal < 30000 and attact > old_attack:
                        old_goal = 20000
                        old_attack = attact
                        self.candidate_list.append((i, o))
                        continue
                    if defen >= 10000 and defen > old_goal:
                        self.candidate_list.append((i, o))
                        old_goal = defen
                        continue
                    if attact >= 10000 or defen >= 10000:
                        continue
                    else:  # 添加三步剪枝博弈判断对方最高得分子若必胜则-10000分 下一手对方无必胜且
                        d = 1
                        h = 1

                        # self.color == 1 and
                        if go_long>=200:
                            do-=0.8
                        if go_long >= 185 and self.color==1:
                            do -= 1
                        if self.color == 1:

                                new_goal = max(attact * (0.2+ ((225 - go_long) / 1125)), defen * (0.3-((225 - go_long) / 2250)))
                                new_goal += min(attact * 1, defen) * 0.001

                        else:
                                new_goal = max(attact * (0.2+((225 - go_long) / 1125)), defen * (0.32-((225 - go_long) / 1125)))
                                new_goal += min(attact * 1, defen) * 0.001


                        if new_goal >= old_goal:
                            old_goal = new_goal

                            self.candidate_list.append((i, o))

        # ==============Find new pos========================================
        # Make sure that the position of your decision in chess board is empty.
        # If not, return error.
        # Add your decision into candidate_list, Records the chess board
# chessboard = np.zeros((15, 15), dtype=np.int)
# chessboard[0, 0:2] = -1
# chessboard[0, 7] = -1
# chessboard[1, 1:4] = 1
# print(chessboard)
