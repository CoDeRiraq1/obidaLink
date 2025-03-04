from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    filters,
    ConversationHandler,
    CallbackContext
)
from config import *
from database import Database
from utils import *

db = Database()
GET_GROUP_NAME, GET_GROUP_TYPE = range(2)

async def start(update: Update, context: CallbackContext):
    """رسالة البدء مع نظام الإحالة"""
    user = update.effective_user
    if not await is_member(update, user.id):
        await context.bot.send_message(
            chat_id=user.id,
            text=f"⚡️ يرجى الاشتراك في {CHANNEL_USERNAME} أولاً",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("✅ التحقق", callback_data="check_sub")]
            )
        )
        return
    
    # معالجة الإحالة
    referrer_id = int(context.args[0]) if context.args else None
    db.add_user(user.id, user.username, referrer_id)
    
    # إنشاء رابط الإحالة
    referral_link = generate_referral_link(user.id, context.bot.username)
    
    # واجهة المستخدم الرئيسية
    keyboard = [
        [InlineKeyboardButton("➕ إضافة مجموعة", callback_data="add_group")],
        [InlineKeyboardButton("🔍 تصفح المجموعات", callback_data="browse")],
        [InlineKeyboardButton("📤 مشاركة رابط الإحالة", callback_data="share_ref")],
        [InlineKeyboardButton("🏆 نقاطي", callback_data="my_points")]
    ]
    
    await update.message.reply_text(
        f"""
        🚀 *مرحبًا {user.first_name}!*
        
        📌 **رابط الإحالة الخاص بك**:
        `{referral_link}`
        
        💎 **المميزات**:
        - أضف مجموعتك واحصل على أعضاء جدد
        - احصل على نقاط مقابل كل إحالة
        - صنِّف مجموعتك حسب التخصص
        
        📊 **رصيدك الحالي**: {db.get_user_points(user.id)} نقطة
        """,
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def handle_add_group(update: Update, context: CallbackContext):
    """بدء عملية إضافة مجموعة"""
    await update.callback_query.answer()
    await update.effective_message.reply_text("📤 أرسل رابط المجموحة:")
    return GET_GROUP_NAME

# ... (بقية الدوال)

def get_user_handlers():
    return [
        CommandHandler('start', start),
        CallbackQueryHandler(handle_add_group, pattern='add_group'),
        ConversationHandler(
            entry_points=[CallbackQueryHandler(handle_add_group, pattern='add_group')],
            states={
                GET_GROUP_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, process_group_link)],
                GET_GROUP_TYPE: [CallbackQueryHandler(process_group_type)]
            },
            fallbacks=[]
        ),
        CallbackQueryHandler(show_my_points, pattern='my_points'),
        CallbackQueryHandler(share_referral, pattern='share_ref')
    ]
