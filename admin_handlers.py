from telegram import Update
from telegram.ext import CommandHandler, CallbackContext
from database import Database
from utils import is_admin

db = Database()

async def admin_approve(update: Update, context: CallbackContext):
    """موافقة المطور على مجموعة"""
    if not is_admin(update.effective_user.id):
        return
    
    group_id = int(context.args[0])
    db.approve_group(group_id)
    
    # إرسال إشعار للمستخدم
    group = db.get_group(group_id)
    await context.bot.send_message(
        chat_id=group.owner_id,
        text=f"✅ تمت الموافقة على مجموعتك: {group.name}"
    )
    await update.message.reply_text(f"تمت الموافقة على المجموحة #{group_id}")

async def admin_broadcast(update: Update, context: CallbackContext):
    """إذاعة رسالة للمستخدمين"""
    if not is_admin(update.effective_user.id):
        return
    
    message = ' '.join(context.args)
    users = db.get_all_users()
    
    for user in users:
        try:
            await context.bot.send_message(chat_id=user.user_id, text=message)
        except:
            pass
    
    await update.message.reply_text(f"تم الإرسال لـ {len(users)} مستخدم")

def get_admin_handlers():
    return [
        CommandHandler('approve', admin_approve),
        CommandHandler('broadcast', admin_broadcast),
        CommandHandler('stats', admin_stats)
    ]
