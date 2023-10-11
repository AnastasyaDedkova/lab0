import codecs
import json
import random
import time

from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split


def clean(text):
    clean_text = ''
    for ch in text.lower():
        if ch in 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя ':
            clean_text = clean_text + ch
    return clean_text


file = codecs.open('Dataset3.json', 'r', 'utf-8')
BOT_CONFIG = json.load(file)
file.close()
print(len(BOT_CONFIG['intents'].keys()))

texts = []
y = []
for intent in BOT_CONFIG['intents'].keys():
    for example in BOT_CONFIG['intents'][intent]['examples']:
        texts.append(example)
        y.append(intent)
print(len(texts), len(y))

train_texts, test_texts, y_train, y_test = train_test_split(texts, y, random_state=42, test_size=0.2)

vectorizer = CountVectorizer(ngram_range=(2, 5), min_df=1, max_df=7, analyzer='char_wb')
X_train = vectorizer.fit_transform(train_texts)
X_test = vectorizer.transform(test_texts)

vocab = vectorizer.get_feature_names_out()
print(len(vocab))

clf = RandomForestClassifier(n_estimators=300).fit(X_train, y_train)
print(clf.score(X_train, y_train), clf.score(X_test, y_test))


def get_intent_by_model(text):
    return clf.predict(vectorizer.transform([text]))[0]


def bot(input_text):
    intent = get_intent_by_model(input_text)
    return random.choice(BOT_CONFIG['intents'][intent]['responses'])


## Добавили функцию обработки ссылок
def req(input_text):
    call2 = input_text.replace(' ', '')
    if call2[0] == 'h' and call2[4] == 's':
        call3 = call2[8:]
    elif call2[0] == 'h' and call2[4] == ':':
        call3 = call2[7:]
    else:
        call3 = call2
    if call3[-1] == '/':
        call = call3[:-1]
    else:
        call = call3
    return call


input_text = ''
while input_text != 'stop':
    input_text = input()
    if input_text != 'stop':
        response = bot(input_text)
        print(response)

#  Добавили переключатель проверки ссылок
input_site_checker_listener = False

import logging

from telegram import KeyboardButton, ReplyKeyboardMarkup
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, CallbackContext, Filters
from config import TOKEN

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments update and
# context.
def start(update: Update, context: CallbackContext) -> None:
    #     """Send a message when the command /start is issued."""
    user = update.effective_user
    sticHello = open("Hello.webp", "rb")
    update.message.reply_sticker(sticHello)
    time.sleep(1)
    update.message.reply_markdown_v2(
        fr'Привет, я Совёнок \- бот компании Ростелеком по безопасности в Интернете\!')
    time.sleep(2.5)
    update.message.reply_text(main_menu_message(),
                              reply_markup=main_menu_keyboard())


############################ Keyboards #########################################
def main_menu_keyboard():
    keyboard = [[KeyboardButton('🚨 Неотложная помощь')],
                [KeyboardButton('☝ Правила безопасности')],
                [KeyboardButton('💎 Полезные ресурсы')]]
    return ReplyKeyboardMarkup(keyboard)


def first_menu_keyboard():
    keyboard = [[KeyboardButton('😿  Взломали мою страничку')],
                [KeyboardButton('🔑  Нужен надёжный пароль')],
                [KeyboardButton('🆘  Меня атакуют мошенники')],
                [KeyboardButton('Вернуться')]]
    return ReplyKeyboardMarkup(keyboard)


def second_menu_keyboard():
    keyboard = [[KeyboardButton('💬   Общение')],
                [KeyboardButton('👜   Платежи и покупки')],
                [KeyboardButton('⭐   Госуслуги')],
                [KeyboardButton('📮   Электронная почта')],
                [KeyboardButton('Вернуться')]]
    return ReplyKeyboardMarkup(keyboard)


def third_menu_keyboard():
    keyboard = [[KeyboardButton('📚  Азбука Интернета')],
                [KeyboardButton('🎥  Видеокурсы')],
                [KeyboardButton('🏆  Тесты')],
                [KeyboardButton('Вернуться')]]
    return ReplyKeyboardMarkup(keyboard)


#############################InlineKeyboards####################################

def hacked_page_menu_inlinekeyboard():
    keyboard = [[InlineKeyboardButton('ВКонтакте', url='https://vhod.ru/vkontakte/parol/')],
                [InlineKeyboardButton('Одноклассники', url='https://vhod.ru/odnoklassniki/vzlomali/')],
                [InlineKeyboardButton('Телеграм',
                                      url='https://web-telegramm.org/telegramm/vopros-otvet-telegramm/345-chto-delat-esli-menya-vzlomali-v-telegramm.html')]]
    return InlineKeyboardMarkup(keyboard)


def password_menu_inlinekeyboard():
    keyboard = [[InlineKeyboardButton('Советы эксперта',
                                      url='https://www.kaspersky.ru/blog/false-perception-of-it-security-passwords/6460/')],
                [InlineKeyboardButton('Генератор паролей', url='https://www.roboform.com/ru/password-generator/')],
                [InlineKeyboardButton('Проверьте свой пароль', url='https://password.kaspersky.com/ru/')]]
    return InlineKeyboardMarkup(keyboard)


def scam_menu_inlinekeyboard():
    keyboard = [[InlineKeyboardButton('Как распознать мошенника',
                                      url='https://fincult.info/article/kak-bystro-raspoznat-moshennika/')],
                [InlineKeyboardButton('Сообщить о мошенничестве',
                                      url='http://www.sberbank.ru/ru/person/cybersecurity/report')],
                [InlineKeyboardButton('Проверка телефона или сайта',
                                      url='http://www.sberbank.ru/ru/person/cybersecurity/antifraud')]]
    return InlineKeyboardMarkup(keyboard)


def social_menu_inlinekeyboard():
    keyboard = [
        [InlineKeyboardButton('Социальные сети', url='https://vc.ru/social/81702-bezopasnost-v-socialnyh-setyah')],
        [InlineKeyboardButton('WhatsApp', url='https://www.whatsapp.com/safety?lang=ru/')],
        [InlineKeyboardButton('Viber', url='https://goo.su/cetP')]]
    return InlineKeyboardMarkup(keyboard)


def buy_menu_inlinekeyboard():
    keyboard = [[InlineKeyboardButton('Фишинг',
                                      url='https://fincult.info/article/fishing-chto-eto-takoe-i-kak-ot-nego-zashchititsya/')],
                [InlineKeyboardButton('Интернет-магазины',
                                      url='https://fincult.info/article/bezopasnye-pokupki-v-internete/')],
                [InlineKeyboardButton('Сайты объявлений', url='https://www.avito.ru/journal/safety#how')],
                [InlineKeyboardButton('Как ограничить расходы по карте',
                                      url='https://bankstoday.net/last-articles/na-zlo-moshennikam-kak-samomu-ustanovit-sutochnyj-limit-po-kartam-sberbanka')]]
    return InlineKeyboardMarkup(keyboard)


def public_menu_inlinekeyboard():
    keyboard = [[InlineKeyboardButton('Как зарегистрироваться', url='https://www.gosuslugi.ru/help/faq/login/1')],
                [InlineKeyboardButton('Защита от взлома',
                                      url='https://www.kaspersky.ru/blog/gosuslugi-ru-security/23371/')],
                [InlineKeyboardButton('Помощь пенсионерам',
                                      url='https://www.gosuslugi.ru/situation/pomoshch_pensioneram')],
                [InlineKeyboardButton('Осторожно:мошенники',
                                      url='https://www.gosuslugi.ru/help/news/2020_04_27_scammers')]]
    return InlineKeyboardMarkup(keyboard)


def mail_menu_inlinekeyboard():
    keyboard = [[InlineKeyboardButton('Защита от взлома', url='https://safe-surf.ru/users-of/article/335/')],
                [InlineKeyboardButton('Как бороться со спамом',
                                      url='https://www.kaspersky.ru/resource-center/threats/spam-phishing')],
                [InlineKeyboardButton('Письма мошенников', url='https://help.mail.ru/mail/security/letters/money')]]
    return InlineKeyboardMarkup(keyboard)


def video_menu_inlinekeyboard():
    keyboard = [
        [InlineKeyboardButton('Основы работы на компьютере', url='https://www.azbukainterneta.ru/guidelines/video/')],
        [InlineKeyboardButton('Уроки кибербезопасности', url='https://education.kaspersky.com/ru/')],
        [InlineKeyboardButton('Онлайн-занятия', url='https://starikam.org/trips/')]]
    return InlineKeyboardMarkup(keyboard)


def e_book_menu_inlinekeyboard():
    keyboard = [[InlineKeyboardButton('Базовый курс', url='https://azbukainterneta.ru/schoolbook/base/')],
                [InlineKeyboardButton('Расширенный курс', url='https://azbukainterneta.ru/schoolbook/extended/')]]
    return InlineKeyboardMarkup(keyboard)


def test_menu_inlinekeyboard():
    keyboard = [[InlineKeyboardButton('Кибербезопасность', url='https://public.oprosso.sberbank.ru/p/kvpni4dj')],
                [InlineKeyboardButton('Общение в сети', url='https://public.oprosso.sberbank.ru/p/nsptacoj')],
                [InlineKeyboardButton('Защита от фишинга', url='https://public.oprosso.sberbank.ru/p/0yqqefu3')],
                [InlineKeyboardButton('Безопасные покупки', url='https://public.oprosso.sberbank.ru/p/y0ax6kdd')]]
    return InlineKeyboardMarkup(keyboard)


############################# Messages #########################################
def main_menu_message():
    return 'Чем могу помочь? Выберите раздел'


def first_menu_message():
    return 'Что у вас случилось?'


def second_menu_message():
    return 'Безопасность прежде всего. О чём бы вы хотели узнать?'


def third_menu_message():
    return 'Что вас интересует?'


############################# InlineMessages ###################################

def hacked_page_inline_menu_message():
    return 'Пожалуйста, не волнуйтесь. Взломанную страничку в соцсетях можно восстановить, пользуясь следующими инструкциями'


def password_inline_menu_message():
    return 'Используйте для пароля символы, цифры, большие и маленькие буквы. Длина пароля – желательно не менее 8 знаков. Вы можете сами придумать пароль, прочитав советы эксперта по безопасности, или воспользуйтесь генератором паролей.'


def scam_inline_menu_message():
    return 'Eсли вы назвали кому-то данные своей карты или код из СМС, срочно звоните по бесплатному номеру 900 (для Сбера) или блокируйте карту в мобильном приложении банка. Можете проверить подозрительный номер телефона или сайт по базе и сообщить о мошенниках.'


def url_inline_menu_message():
    return 'Проверить ссылку на сайт?'


def social_inline_menu_message():
    return 'Главный совет – не переходить по ссылкам из неизвестных источников. Также помните, что ваша информация в социальных сетях может быть найдена и использована кем угодно, в том числе не обязательно с благими намерениями. Подробнее:'


def buy_inline_menu_message():
    return 'Будьте внимательны при совершении платежей. Не стоит отдавать свои деньги незнакомцу, верить в то, что хороший товар продается за копейки. Защитить свои деньги можно, например, ограничив сумму операций по карте за сутки'


def public_inline_menu_message():
    return 'Через портал госуслуг можно записаться к врачу, оформить льготы и компенсации , оплатить налоги и не только. Узнайте, как зарегистрироваться на портале, защитить свою страничку и не стать жертвой мошенников:'


def mail_inline_menu_message():
    return 'Письма, приходящие по электронной почте, могут содержать вирусы или ссылки, ведущие на зараженные сайты. Не открывайте письма с вложениями, полученные от неизвестных отправителей. Подробнее об угрозах и правилах безопасности:'


def video_inline_menu_message():
    return 'Здесь вы можете найти короткие видеоуроки, а также записаться на бесплатные онлайн-занятия:'


def e_book_inline_menu_message():
    return 'Это учебник для людей старшего поколения. Вы можете получить базовые знания о компьютере и Интернете, научиться общаться по видеосвязи и пользоваться электронными сервисами'


def test_inline_menu_message():
    return 'Пройдите тесты, чтобы не оставить мошенникам никаких шансов добраться до ваших денег'


############################# Commands #########################################

def help_command(update: Update, context: CallbackContext) -> None:
    #     """Send a message when the command /help is issued."""
    update.message.reply_text('Напишите сообщение или воспользуйтесь кнопками меню внизу экрана')


def echo(update: Update, context: CallbackContext) -> None:
    #     """Echo the user message."""
    input_text = update.message.text
    if input_text == '🚨 Неотложная помощь' or input_text == 'Неотложная помощь':
        update.message.reply_text(first_menu_message(),
                                  reply_markup=first_menu_keyboard())
    elif input_text == '☝ Правила безопасности' or input_text == 'Правила безопасности':
        update.message.reply_text(second_menu_message(),
                                  reply_markup=second_menu_keyboard())
    elif input_text == '💎 Полезные ресурсы' or input_text == 'Полезные ресурсы':
        update.message.reply_text(third_menu_message(),
                                  reply_markup=third_menu_keyboard())
    elif input_text == '😿  Взломали мою страничку' or input_text == 'Взломали мою страничку':
        update.message.reply_text(hacked_page_inline_menu_message(),
                                  reply_markup=hacked_page_menu_inlinekeyboard())
    elif input_text == '🔑  Нужен надёжный пароль' or input_text == 'Нужен надёжный пароль':
        update.message.reply_text(password_inline_menu_message(),
                                  reply_markup=password_menu_inlinekeyboard())
    elif input_text == '🆘  Меня атакуют мошенники' or input_text == 'Меня атакуют мошенники':
        update.message.reply_text(scam_inline_menu_message(),
                                  reply_markup=scam_menu_inlinekeyboard())
    elif input_text == '🔎  Проверить сайт' or input_text == 'Проверить сайт':
        global input_site_checker_listener
        input_site_checker_listener = True
        update.message.reply_markdown_v2(
            fr'Введите ссылку на сайт, который нужно проверить')

    elif input_site_checker_listener == True:
        output_text = req(input_text)
        keyboard = [[InlineKeyboardButton('Да', url='https://www.virustotal.com/gui/search/' + output_text)]]
        update.message.reply_text(url_inline_menu_message(),
                                  reply_markup=InlineKeyboardMarkup(keyboard))
        input_site_checker_listener = False

    elif input_text == '💬   Общение' or input_text == 'Общение':
        update.message.reply_text(social_inline_menu_message(),
                                  reply_markup=social_menu_inlinekeyboard())
    elif input_text == '👜   Платежи и покупки' or input_text == 'Платежи и покупки':
        update.message.reply_text(buy_inline_menu_message(),
                                  reply_markup=buy_menu_inlinekeyboard())
    elif input_text == '⭐   Госуслуги' or input_text == 'Госуслуги':
        update.message.reply_text(public_inline_menu_message(),
                                  reply_markup=public_menu_inlinekeyboard())
    elif input_text == '📮   Электронная почта' or input_text == 'Электронная почта':
        update.message.reply_text(mail_inline_menu_message(),
                                  reply_markup=mail_menu_inlinekeyboard())
    elif input_text == '🎥  Видеокурсы' or input_text == 'Видеокурсы':
        update.message.reply_text(video_inline_menu_message(),
                                  reply_markup=video_menu_inlinekeyboard())
    elif input_text == '📚  Азбука Интернета' or input_text == 'Азбука интернета':
        update.message.reply_text(e_book_inline_menu_message(),
                                  reply_markup=e_book_menu_inlinekeyboard())
    elif input_text == '🏆  Тесты' or input_text == 'Тесты':
        update.message.reply_text(test_inline_menu_message(),
                                  reply_markup=test_menu_inlinekeyboard())
    elif input_text == 'Вернуться':
        update.message.reply_text(main_menu_message(),
                                  reply_markup=main_menu_keyboard())
    else:
        output_text = bot(input_text)
        update.message.reply_text(output_text)


def main() -> None:
    #     """Start the bot."""
    #     # Create the Updater and pass it your bot's token.
    updater = Updater(token=TOKEN)

    #     # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    #     # on different commands - answer in Telegram
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help_command))

    #     # on non command i.e message - echo the message on Telegram
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))
    updater.dispatcher.add_handler(CommandHandler('start', start))

    #     # Start the Bot
    updater.start_polling()

    #     # Run the bot until you press Ctrl-C or the process receives SIGINT,
    #     # SIGTERM or SIGABRT. This should be used most of the time, since
    #     # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
