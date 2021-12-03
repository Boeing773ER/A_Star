import numpy as np


class Node:
    matrix = np.array([])
    parent = None
    step = 0        # g(n)
    next_step = []
    m_distance = 0  # h(n)

    def __init__(self, matrix):
        self.matrix = matrix


def cal_manhattan_dis(current, target):
    row = current.shape[0]
    col = current.shape[1]
    m_distance = 0
    for i in range(row):
        for j in range(col):
            if current[i][j] != 0:
                (pos_x, pos_y) = get_pos(target, current[i, j])
                m_distance += abs(i - pos_y) + abs(j - pos_x)
    return m_distance


def next_action(matrix, parent_matrix):
    (pos_x, pos_y) = get_pos(matrix, 0)
    action_set = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    # down, up, left, right
    if pos_x == 0:
        action_set.remove((-1, 0))
    if pos_x == 3:
        action_set.remove((1, 0))
    if pos_y == 0:
        action_set.remove((0, -1))
    if pos_y == 3:
        action_set.remove((0, 1))
    parent_x, parent_y = get_pos(parent_matrix, 0)
    if (parent_x-pos_x, parent_y-pos_y) in action_set:
        action_set.remove((parent_x-pos_x, parent_y-pos_y))
    return action_set


def get_pos(matrix, num):
    for i in range(4):      # y
        for j in range(4):  # x
            if matrix[i][j] == num:
                return j, i     # x, y


def move_block(matrix, action):
    result = matrix.copy()
    (pos_x, pos_y) = get_pos(matrix, 0)
    temp = matrix[pos_y+action[1], pos_x+action[0]]
    result[pos_y + action[1], pos_x + action[0]] = 0
    result[pos_y, pos_x] = temp
    return result


def expand_node(current, target):
    children = []   # store node
    for move in current.next_step:
        temp_node = Node(move_block(current.matrix, move))
        temp_node.step = current.step + 1
        temp_node.parent = current
        temp_node.next_step = next_action(temp_node.matrix, current.matrix)
        temp_node.m_distance = cal_manhattan_dis(temp_node.matrix, target)
        children.append(temp_node)
    return children


def evaluation(node):
    # return node.m_distance
    return node.m_distance + node.step
    # return node.m_distance * 10 + node.step
    # return pow(node.m_distance, 2) + node.step


def get_path(node):
    temp_list = []
    while node.parent is not None:
        temp_list.append(node)
        node = node.parent
    print("\nsteps:", len(temp_list))
    while temp_list:
        temp_node = temp_list.pop()
        print("step-num:", temp_node.step)
        print(temp_node.matrix, '\n')


def main():
    init = np.array([[5, 1, 2, 4],
                     [9, 6, 3, 8],
                     [13, 15, 10, 11],
                     [14, 0, 7, 12]])
    # target status
    target = np.array([[1, 2, 3, 4],
                      [5, 6, 7, 8],
                      [9, 10, 11, 12],
                      [13, 14, 15, 0]])
    mode_select = input("select:\n1:default example\n2:random input\n3:manual input\n")
    if mode_select == '1':
        current = Node(init)
    elif mode_select == '2':
        current = Node(np.random.choice(16, (4, 4), replace=False))
    elif mode_select == '3':
        print("input a 4*4 matrix:")
        input_list = []
        for i in range(4):
            temp_str = input()
            temp_str = temp_str.split()
            for j in range(4):
                temp_str[j] = int(temp_str[j])
            input_list.append(temp_str)
        current = Node(np.array(input_list))
    print("init:\n", current.matrix)
    open_list = []      # open list
    close_list = []     # close list
    current.step = 0            # init step = 0
    # current.parent = current    # initial parent set as current
    current.m_distance = cal_manhattan_dis(current.matrix, target)
    # get the initial manhattan distance
    current.next_step = next_action(current.matrix, current.matrix)
    # get initial next action
    if(current.matrix == target).all():
        # judge if finished
        print("finished")
        return
    open_list.append(current)
    # add current to open_list
    while open_list != []:
        node = open_list.pop()
        # take a node from open_list
        close_list.append(node)
        # put it into close_list
        if (node.matrix == target).all():
            # check if finished
            print("finished")
            get_path(node)
            return
        else:
            expanded = expand_node(node, target)
            # judge if expanded node in open_list or close_list
            for new_node in expanded:
                in_open = False
                in_close = False
                pos = 0
                # check if in open_list
                for i in range(len(open_list)):
                    if (open_list[i].matrix == new_node.matrix).all():
                        pos = i
                        in_open = True
                        break
                # check if in close_list
                for i in range(len(close_list)):
                    if (close_list[i].matrix == new_node.matrix).all():
                        in_close = True
                        break
                if not(in_close or in_open):
                    open_list.append(new_node)
                elif in_open:
                    if evaluation(node) < evaluation(open_list[pos]):
                        del open_list[pos]
                        open_list.append(new_node)
            open_list = sorted(open_list, key=evaluation, reverse=True)


if __name__ == '__main__':
    main()
