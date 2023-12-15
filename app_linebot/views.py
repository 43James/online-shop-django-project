from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import pytz
from accounts.models import MyUser
from orders.models import Order
from .models import UserLine
from linebot import LineBotApi
from linebot.models import TextSendMessage
import json


line_bot_api = LineBotApi('p/7wo/1oBrhYYteqvWuGQQJz5AADd3pnSiyTJByIju6L6rT5fWsifmzRiD8YOoPHYZkSQHNMIcnAyjMq9ad3zjL4LHn4+C5PubjxDeGXrcXO5XIYd65jHw2slPVxQ7akCkzj0ZC+8MRIJ3oIBRpHLAdB04t89/1O/w1cDnyilFU=')

@csrf_exempt
def linebot(request):
    body = request.body.decode('utf-8')
    body = json.loads(body)
    event = body['events'][0]
    text = event['message']['text']

    if text.startswith('ผูกบัญชี'):
        a = text.split()
        username = a[1]
        user = MyUser.objects.filter(username=username).first()

        if user:
            line = UserLine.objects.filter(user=user).first()
            userId = event['source']['userId']

            if not line:
                line = UserLine(user=user, userId=userId)
                line.save()
            else:
                line.userId = userId
                line.save()
    return render(request, "home_page.html")



#ส่งการแจ้งเตือนไปยังผู้ใช้งานเมื่อเช็คเอ้าท์สินค้า
def notify_user(order_id):
    try:
        order = Order.objects.get(id=order_id)
        user_line = UserLine.objects.get(user=order.user)

        message = f"{order.user.username} รายการเบิกวัสดุ ID {order_id} ของคุณ ที่ต้องได้รับการอนุมัติ.."
        line_bot_api.push_message(user_line.userId, TextSendMessage(text=message))
    except Order.DoesNotExist:
        print(f"ไม่มีคำร้อง ID {order_id}")
    except UserLine.DoesNotExist:
        print(f"ไม่มี UserLine สำหรับผู้ใช้งาน {order.user.username}")



#ส่งการแจ้งเตือนไปยังแอดมินเมื่อเช็คเอ้าท์สินค้า
def notify_admin(order_id):
    order = Order.objects.get(id=order_id)
    admin_user_id ='Ubb217fccfe04b1dbf5550e46661a8693'  # Replace with the actual Line user ID of the admin
    message = f"คำร้องใหม่จากผู้ใช้งาน {order.user.username} ID {order_id} ที่ต้องได้รับการอนุมัติ.."
    line_bot_api.push_message(admin_user_id, TextSendMessage(text=message))



#ส่งการแจ้งเตือนไปยังผู้ใช้งานเมื่อมีการอนุมัติคำร้อง
def notify_user_approved(order_id):
    try:
        order = Order.objects.get(id=order_id)
        user_line = UserLine.objects.get(user=order.user)

        # Check if order.date_receive is not None
        if order.date_receive:
            # Set timezone to the desired timezone (e.g., Asia/Bangkok)
            timezone = pytz.timezone('Asia/Bangkok')
            order_date_receive_with_timezone = order.date_receive.astimezone(timezone)

        if order.status and not order.refuse:
            if order.date_receive:
                formatted_date = order_date_receive_with_timezone.strftime("%d/%m/%Y")
                formatted_time = order_date_receive_with_timezone.strftime("%H:%M")
                message = f"รายการเบิกวัสดุของคุณ {order.user.first_name} ID {order_id} ได้รับการอนุมัติแล้ว✅ รับวัสดุในวันที่ {formatted_date} เวลา {formatted_time} น."
            else:
                message = f"รายการเบิกวัสดุของคุณ {order.user.first_name} ID {order_id} ได้รับการอนุมัติแล้ว✅"
        elif not order.status and not order.refuse:
            message = f"รายการเบิกวัสดุของคุณ {order.user.first_name} ID {order_id} ยังไม่ได้รับการดำเนินการ😓"
        elif order.refuse:
            
            message = f"รายการเบิกวัสดุของคุณ {order.user.first_name} ID {order_id} ถูกปฏิเสธ!💔 หมายเหตุ {order.other}"
        else:
            message = "สถานะไม่ระบุ"

        line_bot_api.push_message(user_line.userId, TextSendMessage(text=message))
    except Order.DoesNotExist:
        print(f"ไม่มีคำร้อง ID {order_id}")
    except UserLine.DoesNotExist:
        print(f"ไม่มี UserLine สำหรับผู้ใช้งาน {order.user.username}")