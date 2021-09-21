from flask import Flask
from flask import jsonify
from flask import request
from datetime import datetime
from re import sub
from decimal import Decimal
import uuid
import json
import hashlib

app = Flask(__name__)
# dictionary acting like parent table which holds association between orderId and orders
order_map = {}
# dictionary acting like a child table which holds association between member_account_number and order_id
# Note:- Like in RDBMS, need to delete the parent record first and then child association should also be deleted
item_map = {}
timestamp_map = {}
account_map = {}

@app.route('/order/create', methods=["POST"])
def create_order():
    try:
       account_number = request.json['account_number']
       timestamp = request.json['timestamp']
       item_qty = request.json['item_quantity']
       item_list = request.json['itemList']
       req_json = request.json
       if 'timestamp' in req_json:
          del req_json['timestamp']
       content = json.dumps(req_json, sort_keys = True)
       # delete timestamp before computing md5 hash of the order as same duplicate orders at different timestamps are also to be discarded
       order_id = hashlib.md5(content.encode("utf-8")).hexdigest()
       # put the timestamp back in for /last3days endpoint
       req_json['timestamp']=timestamp
       if order_id in order_map:
          return {"err_message": "duplicate order detected!! discarding.."}, 422
       else:
          if account_number not in account_map:
             account_map[account_number] = order_id
          order_map[order_id] = req_json
          print(order_map)
       return {"order_id": order_id}, 201
    except Exception as e:
       return {"error": True, "msg": str(e)}


@app.route('/order/cancel', methods=["POST"])
def cancel_order():
    try:
       deleted_count = 0
       print (order_map)
       member_account_numbers = request.json['member_account_numbers']
       print(member_account_numbers)
       try:
          for item in member_account_numbers:
             if str(item['account_number']) in account_map:
                print("&*&*&* printing account_map and order_map")
                print(account_map)
                print(order_map)
                del order_map[account_map[str(item['account_number'])]]
                del account_map[str(item['account_number'])]
                deleted_count = deleted_count + 1
                print("****************")
                print(order_map)
                print(account_map)
       except Exception as e:
          return {"internal_error" : str(e)}
       return {"order_count": deleted_count}, 200
    except Exception as e:
       return {"error": True, "msg": str(e)}


@app.route('/order/last3days', methods=["GET"])
def get_orders_from_last_three_days():
    try:
       last_three_days_orders = []
       print("before for loop")
       for key in order_map:
          print(key)
          print(order_map[key])
          ttime = datetime.fromtimestamp(int(order_map[key]['timestamp'])/1000)
          print(ttime)
          offset = ((datetime.now() - ttime).days)
          if offset > 0 and offset <= 3:
             last_three_days_orders.append(order_map[key])
    except Exception as e:
       return {"error" : True, "msg" : str(e)} 
    return {"last_three_days_orders" : last_three_days_orders, "count": len(last_three_days_orders)}
    


@app.route('/order/top3items', methods=["GET"])
def get_top_three_items_by_value():
    top_3_items = {}
    try:
       for key in order_map:
          item_list = order_map[key]['itemList']
          for item in item_list:
             item_name = item['item_name']
             item_price = item['item_price']
             print("here "+item_name)
             print("here "+item_price)
             item_total_value = item_name + '_total_value'
             #if item_name not in top_3_items:
             #  top_3_items[item_name] = item_name
             if item_total_value not in top_3_items:
                top_3_items[item_total_value] = (float(sub(r'[^\d.]', '', item_price)))
             else:
                top_3_items[item_total_value] = (float(top_3_items[item_total_value]) + float(sub(r'[^\d.]', '', item_price)))
    except Exception as e:
       return {"error" : True, "msg" : str(e)}       
    top_selling_items = list(sort_dict_by_value(top_3_items, True).items())[:3]
    return {"top_3_items" : top_selling_items}


@app.route("/")
def hello_world():
  return "Hello, World from the server!!"


def sort_dict_by_value(d, reverse = False):
  return dict(sorted(d.items(), key = lambda x: x[1], reverse = reverse))
