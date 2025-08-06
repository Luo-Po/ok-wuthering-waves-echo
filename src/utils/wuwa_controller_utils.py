def scroll_echo_list(task, direction: str = "down", amount: int = 3) -> bool:
    """滚动回音列表"""
    if direction == "down":
        task.scroll(930, 693, -amount)
        task.sleep(0.2)
    elif direction == "up":
        task.scroll(930, 693, amount)
        task.sleep(0.2)

    return True


def click_echo_box(task, x: int, y: int):
    xls = {
        1: 278,
        2: 500,
        3: 722,
        4: 945,
        5: 1167,
        6: 1389
    }
    xrs = {
        1: 470,
        2: 692,
        3: 914,
        4: 1137,
        5: 1359,
        6: 1581
    }
    yts = {
        1: 166,
        2: 439,
        3: 713,
        4: 986
    }
    ybs = {
        1: 400,
        2: 674,
        3: 947,
        4: 1220
    }
    cx = int((xls[x] + xrs[x]) / 2)
    cy = int((yts[y] + ybs[y]) / 2)
    task.click(x=cx, y=cy)
    return True
