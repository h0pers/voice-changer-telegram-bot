import os

from iso4217 import Currency
from pytz import timezone

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

DB_URL = f'mysql+aiomysql://root:{os.getenv("MYSQL_ROOT_PASSWORD")}@{os.getenv("MYSQL_HOST")}/{os.getenv("MYSQL_DATABASE")}'

BOT_TOKEN = os.getenv('BOT_TOKEN')

REDIS_PORT = os.getenv('REDIS_PORT')

REDIS_HOST = os.getenv('REDIS_HOST')

DEFAULT_VOICE_MODEL = 'eleven_multilingual_v2'

DEFAULT_VOICE_SPEECH_MODEL = 'eleven_multilingual_sts_v2'

TIMEZONE = timezone(os.getenv('TIMEZONE'))

DAILY_AUDIO_ATTEMPT = 5

VOICE_CHARACTERS_MIN_REQUIRED = 500

REFERRAL_INCOME = 3

STRFTIME_DEFAULT_FORMAT = '%d.%m.%Y, %H:%M'

DEFAULT_CURRENCY = Currency('USD')


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
Отправьте голосовое сообщение боту и получите готовый вариант.
'''
    CANCEL_SUCCESSFUL = 'Успешная отмена.'
    VOICE_LENGTH_ERROR = 'Вы вышли за рамки допустимого лимита, попробуйте уменьшить содержимое'
    USER_ACCOUNT_STATS = '''
<b>👨‍💼 Ваш личный кабинет</b>

<b>🚀 Telegram ID:</b> {telegram_id}
<b>🔖 Остаток голосовых сообщений:</b> {voice_attempt_left}

<b>Администратор:</b> @imfckngkucenko

<b>⏳ За все время Вы записали:</b> {audio_processed_amount} голосовых

<b>Лимит голосовых сообщений обновляется каждый день.
Получить дополнительные голосовые можно через реферальную систему.</b>    
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
    REFERRAL_ACCOUNT_INFO = '''
<b>▫️ В нашем боте действует партнёрская программа с дополнительными голосовыми сообщениями за каждое вступление по вашей ссылке.
▪️ За каждого приглашенного пользователя, вы получаете +{referal_income} бесплатных голосовых.
▫️ Ваша партнёрская ссылка:</b> {referral_link}

<b>🗣 Пригласил всего:</b> {total_referrals}
<b>🗣 Доступных голосовых за приглашения:</b> {referral_audio_attempt_left}
<b>🗣 Всего получено голосовых за приглашения:</b> {referral_audio_attempt_total}
'''
    COMMAND_SYNTAX_ERROR = 'Убедитесь что вы правильно вели данные.'
    BAN_USER_NOTIFICATION = '''
<b>❌ Вы заблокированы до</b> {block_end_time}.
<b>Причина:</b> {reason}.
<b>Для разблокировки можете обратиться к администратору.</b>
'''
    PERMANENT_BLOCK_END_TIME = 'Без срочно'
    USER_IS_NOT_EXIST = 'Пользователь не найден'
    UNBAN_SUCCESSFUL = 'Пользователь <b>{telegram_id}</b> был успешно разблокирован'
    BAN_SUCCESSFUL = 'Пользователь <b>{telegram_id}</b> был успешно заблокирован'
    NO_VOICE_ATTEMPT = 'У вас закончились все попытки.'
    VOICE_CHARACTERS_LACK = '<b>Голосовые функции станут доступны позже. Проводим техническое обновление.</b>'
    VOICE_CHARACTERS_LACK_ADMIN = '<b>Квота исчерпана</b>'
    GLOBAL_STATISTIC = '''
<b>Количество пользователей:</b> {user_count}
'''
    GIVE_VOICE_PREMIUM = 'Отправьте Telegram ID'
    GIVE_VOICE_PREMIUM_SUCCESSFUL = 'Пользователю <b>{telegram_id}</b> было выдано VOICE Premium'
    REMOVE_VOICE_PREMIUM = 'Отправьте Telegram ID'
    REMOVE_VOICE_PREMIUM_SUCCESSFUL = 'У пользователя <b>{telegram_id}</b> было убрано VOICE Premium'
    CHANGE_VOICE_LIMIT = 'Установите лимит голосового'
    CHANGE_TEXT_LIMIT = 'Установите лимит символов'
    CHANGE_LIMIT_SUCCESSFUL = 'Лимит успешно изменен'
