import os

from dotenv import load_dotenv

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

load_dotenv(dotenv_path=os.path.join(BASE_DIR, '.env'))

DB_URL = conn_url = f'mysql+aiomysql://root:{os.getenv("MYSQL_ROOT_PASSWORD")}@{os.getenv("MYSQL_HOST")}/{os.getenv("MYSQL_DATABASE")}'

BOT_TOKEN = os.getenv('BOT_TOKEN')

REDIS_PORT = os.getenv('REDIS_PORT')

REDIS_HOST = os.getenv('REDIS_HOST')

DEFAULT_VOICE_MODEL = 'eleven_multilingual_v2'

DEFAULT_VOICE_SPEECH_MODEL = 'eleven_multilingual_sts_v2'


class MessageText:
    SETUP_VOICE_API = 'Отправьте API ключ'
    ADMIN_PANEL_WELCOME = 'Добро пожаловать в панель администратора.'
    SETUP_VOICE_ID = 'Отправьте ID голоса'
    SETUP_NEWSLETTER = 'Отправьте сообщение для рассылки'
    SETUP_VOICE_REPLY_ID = 'Отправьте ID чата где бот является администратором'
    PICKED_WOMAN_VOICE_WELCOME = '''
Выберите способ преобразования.
<b>Текст</b> - Бот преобразует текст, который вы напишите.
<b>Голосовое</b> - Бот сделает голосовое с женским голосом вместо вашего голоса.

Если хотите максимально сохранить акцент, знаки препинания, фоновый шум (улица, подъезд, магазин) - используйте вариант <b>Голосовое</b>.
Если нет возможности этого сделать, используйте способ <b>Текст</b>, но желательно делать короткие голосовые до 5-10 секунд и проверять нет ли каких-либо искажений голоса.    
'''
    WELCOME = '''
<b>👋 Привет! Я бот, который может преобразовывать текст в голосовое сообщение.</b>

Создатель: @imfckngkucenko     
'''
    TEXT_CONVERTING_WELCOME = '''
Вы выбрали конвертацию с помощью текста.

‼️Будьте осторожны. Текст нужно вписывать со всеми знаками препинания и правильная орфография. После полученного голосового - обязательно прослушайте его и убедитесь в том, что нет каких-то не нужных препинаний, лишнего акцента и т.д.    
'''
    SPEECH_CONVERTING_WELCOME = '''
<b>Вы выбрали конвертацию с помощью голоса.</b>
Отправьте голосовое сообщение боту (до 60 секунд) и получите готовый вариант.
'''
    CANCEL_SUCCESSFUL = 'Успешная отмена.'
    VOICE_LENGTH_ERROR = 'Длина голосового сообщение не должна превышать 60 секунд.'
    USER_ACCOUNT_STATS = '''
<b>👨‍💼 Ваш личный кабинет</b>

🚀 Telegram ID: {telegram_id}

<b>Администратор:</b> @imfckngkucenko

👥 Пользователей в боте: {bot_users_amount}

⏳ За все время Вы записали: {audio_processed_amount} голосовых
'''
    VOICE_API_CHARACTERS_LEFT = '''
<b>Лимит символов на API:</b> {characters_limit}
<b>Использовано на текущий момент:</b> {characters_count}
<b>Осталось символов:</b> {characters_left}
'''
    NEWSLETTER_START = 'Рассылка запущена. Ожидайте...'
    NEWSLETTER_FINISH = '''
<b>Успешно отправлено:</b> {successful_executed}
<b>Не удалось отправить:</b> {unsuccessful_executed}
<b>Выполнено за:</b> {finish_time}
<b>Общее количество пользователей:</b> {users_amount}
'''
    PROCESSED_VOICE_CAPTION = '''
Голосове сообщение:
<b>ID Пользователя:</b> <code>{telegram_id}</code>
<b>TAG Пользователя:</b> @{username}
'''
