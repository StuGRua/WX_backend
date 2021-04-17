from utils.timestampFix import *
def OrderToDict_withP(pre_res):
    if not pre_res:
        return
    res = []
    for x in pre_res:
        # print(x.Order.start_time)
        temp = {
            'order_id': x.Order.order_id,
            'order_title': x.Order.order_title,
            'pub_id': x.Order.pub_id,
            'rec_id': x.Order.rec_id,
            # 'start_time': x.Order.start_time.strftime('%Y-%m-%d %H:%M'),
            # 'end_time': x.Order.end_time.strftime('%Y-%m-%d %H:%M'),
            'start_time':StamptoStr(x.Order.start_time),
            'end_time':StamptoStr(x.Order.end_time),
            'order_stat': x.Order.order_stat,
            'order_payment': x.Order.order_payment,
            'order_info': x.Order.order_info,
            'phonenumber': x.User.phonenumber
        }
        res.append(temp)
    # print('multi:',res)
    return res


def OrderToDict(pre_res):
    if not pre_res:
        return
    res = []
    for x in pre_res:
        # print(x.start_time)
        temp = {
            'order_id': x.order_id,
            'order_title': x.order_title,
            'pub_id': x.pub_id,
            'rec_id': x.rec_id,
            # 'start_time': x.start_time.strftime('%Y-%m-%d %H:%M'),
            # 'end_time': x.end_time.strftime('%Y-%m-%d %H:%M'),
            'start_time': StamptoStr(x.start_time),
            'end_time': StamptoStr(x.end_time),
            'order_stat': x.order_stat,
            'order_payment': x.order_payment,
            'order_info': x.order_info,
        }
        res.append(temp)
    # print(res)
    return res

def SimpleOrderToDict(pre_res):
    if not pre_res:
        return
    res = []
    for x in pre_res:
        print(x)
        temp = {
            'order_id': x.order_id,
            'order_title': x.order_title,
            'pub_id': x.pub_id,
            'start_time': x.start_time,
            'end_time': x.end_time,
            'order_stat': x.order_stat,
            'order_payment': x.order_payment,

        }
        res.append(temp)
    return res