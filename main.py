import os

from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, ConversationHandler



TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')

if not TOKEN:
    exit(1)

QUESTION_1, QUESTION_2, QUESTION_3, QUESTION_4, QUESTION_5, QUESTION_6, QUESTION_7, QUESTION_8 = range(8)

questions = [
    "Какой у вас характер?",
    "Что вы любите делать в свободное время?",
    "Как вы относитесь к приключениям?",
    "Что для вас самое важное в жизни?",
    "Как вы общаетесь с друзьями?",
    "Как вы решаете проблемы?",
    "Что вас вдохновляет?",
    "Какой вы в критической ситуации?"
]
answers = [
    # Вопрос 1: Какой у вас характер?
    [["Энергичный и весёлый"], ["Спокойный и рассудительный"], ["Мечтательный и творческий"], ["Практичный и деловой"], ["Мудрый и философский"]],

    # Вопрос 2: Что вы любите делать в свободное время?
    [["Веселиться с друзьями"], ["Читать и учиться"], ["Творить и выдумывать"], ["Работать и строить планы"], ["Исследовать и открывать"]],

    # Вопрос 3: Как вы относитесь к приключениям?
    [["Обожаю приключения!"], ["Предпочитаю стабильность"], ["Мечтаю о приключениях"], ["Планирую приключения заранее"], ["Изучаю теорию приключений"]],

    # Вопрос 4: Что для вас самое важное в жизни?
    [["Дружба и веселье"], ["Знания и мудрость"], ["Красота и искусство"], ["Порядок и успех"], ["Гармония и здоровье"]],

    # Вопрос 5: Как вы общаетесь с друзьями?
    [["Шумные компании и вечеринки"], ["Интеллектуальные беседы"], ["Романтические разговоры"], ["Помощь и забота"], ["Спокойное общение"]],

    # Вопрос 6: Как вы решаете проблемы?
    [["Импульсивно и быстро"], ["Анализирую и взвешиваю"], ["Ищу творческий подход"], ["Составляю план действий"], ["Советуюсь с мудрецами"]],

    # Вопрос 7: Что вас вдохновляет?
    [["Новые впечатления"], ["Научные открытия"], ["Искусство и красота"], ["Технический прогресс"], ["Природа и гармония"]],

    # Вопрос 8: Какой вы в критической ситуации?
    [["Действую быстро и решительно"], ["Сохраняю хладнокровие"], ["Впадаю в раздумья"], ["Ищу практичное решение"], ["Дам мудрый совет"]]
]


characters = {
    "Крош": {
        "description": "Вы - Крош! 🐰 Энергичный, весёлый и непоседливый заяц. Обожаете приключения, всегда полны энтузиазма и готовы к новым открытиям!",
        "image": "https://funny.klev.club/smeh/uploads/posts/2024-04/funny-klev-club-ee5t-p-kartinki-smeshnoi-krosh-10.jpg"
    },
    "Ёжик": {
        "description": "Вы - Ёжик! 🦔 Умный, спокойный и рассудительный. Любите читать книги, коллекционировать кактусы и всегда даёте мудрые советы друзьям.",
        "image": "https://sun9-66.userapi.com/impg/AgWNkBKeYvI1WUTGVnEPUYkNExqoAASQQ82Qbg/KFxL6u2F9Lg.jpg?size=647x647&quality=96&sign=7442cd08871139632b89a095d36d75be&type=album"
    },
    "Бараш": {
        "description": "Вы - Бараш! 🐑 Мечтательный и творческий поэт. Обладаете тонкой душевной организацией, любите искусство и пишете стихи о прекрасном.",
        "image": "https://pm1.aminoapps.com/6866/0c607fe37428515f51c542a97fa445d461f2c842r1-1280-720v2_hq.jpg"
    },
    "Пин": {
        "description": "Вы - Пин! 🐧 Практичный и изобретательный пингвин. Любите порядок, технологию, изобретения и всегда доводите дела до конца.",
        "image": "https://funny.klev.club/uploads/posts/2024-03/funny-klev-club-p-smeshnie-kartinki-pin-kod-3.jpg"
    },
    "Лосяш": {
        "description": "Вы - Лосяш! 🦌 Учёный и философ. Обладаете глубокими знаниями, любите науку, размышления о мироздании и проводите эксперименты.",
        "image": "https://funny.klev.club/smeh/uploads/posts/2024-04/funny-klev-club-u8u3-p-smeshnie-kartinki-vsekh-smesharikov-15.jpg"
    },
    "Кар-Карыч": {
        "description": "Вы - Кар-Карыч! 🐦 Мудрый и опытный ворон. Любите рассказывать истории из прошлого, давать жизненные советы и немного драматизировать.",
        "image": "https://pm1.aminoapps.com/6691/a93217076f219d2168c84bdb4563bebad920d02e_00.jpg"
    },
    "Совунья": {
        "description": "Вы - Совунья! 🦉 Заботливая и мудрая сова. Любите спорт, здоровый образ жизни, заботитесь о друзьях и даёте полезные советы.",
        "image": "https://funny.klev.club/uploads/posts/2024-03/funny-klev-club-p-smeshnie-kartinki-sovunya-10.jpg"
    },
    "Нюша": {
        "description": "Вы - Нюша! 🐷 Романтичная и модная свинка. Обожаете красоту, моду, романтические истории и всегда следите за своим внешним видом.",
        "image": "https://img.labirint.ru/images/comments_pic/1816/1_e79416618346c0409a31dcabe57a47c3_1523900240.jpg"
    },
    "Копатыч": {
        "description": "Вы - Копатыч! 🐻 Трудолюбивый и добрый медведь. Любите садоводство, природу, заботу о растениях и всегда готовы помочь друзьям.",
        "image": "https://cs13.pikabu.ru/post_img/big/2020/01/17/5/1579242654187294635.jpg"
    }
}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text(
        "Привет! Давай узнаем, кто ты из Смешариков! 🎭\n"
        "Ответь на 8 простых вопросов и узнай результат!\n\n"
        f"📝 Вопрос 1: {questions[0]}",
        reply_markup=ReplyKeyboardMarkup(answers[0], one_time_keyboard=True, resize_keyboard=True)
    )
    return QUESTION_1

async def handle_question_1(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user_answer = update.message.text
    answer_index = answers[0].index([user_answer])
    context.user_data['answers'] = [answer_index]
    await update.message.reply_text(
        f"📝 Вопрос 2: {questions[1]}",
        reply_markup=ReplyKeyboardMarkup(answers[1], one_time_keyboard=True, resize_keyboard=True)
    )
    return QUESTION_2

async def handle_question_2(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user_answer = update.message.text
    answer_index = answers[1].index([user_answer])
    context.user_data['answers'].append(answer_index)
    await update.message.reply_text(
        f"📝 Вопрос 3: {questions[2]}",
        reply_markup=ReplyKeyboardMarkup(answers[2], one_time_keyboard=True, resize_keyboard=True)
    )
    return QUESTION_3

async def handle_question_3(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user_answer = update.message.text
    answer_index = answers[2].index([user_answer])
    context.user_data['answers'].append(answer_index)
    await update.message.reply_text(
        f"📝 Вопрос 4: {questions[3]}",
        reply_markup=ReplyKeyboardMarkup(answers[3], one_time_keyboard=True, resize_keyboard=True)
    )
    return QUESTION_4

async def handle_question_4(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user_answer = update.message.text
    answer_index = answers[3].index([user_answer])
    context.user_data['answers'].append(answer_index)
    await update.message.reply_text(
        f"📝 Вопрос 5: {questions[4]}",
        reply_markup=ReplyKeyboardMarkup(answers[4], one_time_keyboard=True, resize_keyboard=True)
    )
    return QUESTION_5

async def handle_question_5(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user_answer = update.message.text
    answer_index = answers[4].index([user_answer])
    context.user_data['answers'].append(answer_index)
    await update.message.reply_text(
        f"📝 Вопрос 6: {questions[5]}",
        reply_markup=ReplyKeyboardMarkup(answers[5], one_time_keyboard=True, resize_keyboard=True)
    )
    return QUESTION_6

async def handle_question_6(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user_answer = update.message.text
    answer_index = answers[5].index([user_answer])
    context.user_data['answers'].append(answer_index)
    await update.message.reply_text(
        f"📝 Вопрос 7: {questions[6]}",
        reply_markup=ReplyKeyboardMarkup(answers[6], one_time_keyboard=True, resize_keyboard=True)
    )
    return QUESTION_7

async def handle_question_7(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user_answer = update.message.text
    answer_index = answers[6].index([user_answer])
    context.user_data['answers'].append(answer_index)
    await update.message.reply_text(
        f"📝 Вопрос 8: {questions[7]}",
        reply_markup=ReplyKeyboardMarkup(answers[7], one_time_keyboard=True, resize_keyboard=True)
    )
    return QUESTION_8

async def handle_question_8(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user_answer = update.message.text
    answer_index = answers[7].index([user_answer])
    context.user_data['answers'].append(answer_index)

    result = calculate_result(context.user_data['answers'])
    character = characters[result]

    await update.message.reply_text("🔮 Анализирую ваши ответы...")

    try:
        await update.message.reply_photo(character['image'])
    except Exception as e:
        await update.message.reply_text(f"🖼️ {result}")

    await update.message.reply_text(
        f"🎉 Поздравляем! 🎉\n\n{character['description']}",
        reply_markup=ReplyKeyboardMarkup([['/start']], one_time_keyboard=True, resize_keyboard=True)
    )
    return ConversationHandler.END

def calculate_result(answers):
    scores = {
        "Крош": 0, "Ёжик": 0, "Бараш": 0, "Пин": 0, "Лосяш": 0,
        "Кар-Карыч": 0, "Совунья": 0, "Нюша": 0, "Копатыч": 0
    }

    question_weights = [
        {"Крош": [0], "Ёжик": [1], "Бараш": [2], "Пин": [3], "Лосяш": [4], "Кар-Карыч": [4], "Совунья": [1], "Нюша": [2], "Копатыч": [3]},
        {"Крош": [0], "Ёжик": [1], "Бараш": [2], "Пин": [3], "Лосяш": [4], "Кар-Карыч": [4], "Совунья": [3], "Нюша": [0], "Копатыч": [3]},
        {"Крош": [0], "Ёжик": [1], "Бараш": [2], "Пин": [3], "Лосяш": [4], "Кар-Карыч": [1], "Совунья": [1], "Нюша": [2], "Копатыч": [1]},
        {"Крош": [0], "Ёжик": [1], "Бараш": [2], "Пин": [3], "Лосяш": [1], "Кар-Карыч": [4], "Совунья": [4], "Нюша": [2], "Копатыч": [3]},
        {"Крош": [0], "Ёжик": [1], "Бараш": [2], "Пин": [3], "Лосяш": [1], "Кар-Карыч": [4], "Совунья": [3], "Нюша": [0], "Копатыч": [4]},
        {"Крош": [0], "Ёжик": [1], "Бараш": [2], "Пин": [3], "Лосяш": [4], "Кар-Карыч": [4], "Совунья": [1], "Нюша": [2], "Копатыч": [3]},
        {"Крош": [0], "Ёжик": [1], "Бараш": [2], "Пин": [3], "Лосяш": [1], "Кар-Карыч": [4], "Совунья": [4], "Нюша": [0], "Копатыч": [4]},
        {"Крош": [0], "Ёжик": [1], "Бараш": [2], "Пин": [3], "Лосяш": [4], "Кар-Карыч": [4], "Совунья": [1], "Нюша": [2], "Копатыч": [3]}
    ]

    for i, answer_index in enumerate(answers):
        for character, preferred_answers in question_weights[i].items():
            if answer_index in preferred_answers:
                scores[character] += 1

    return max(scores, key=scores.get)

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text(
        'Тест отменен. Если захотите попробовать снова, напишите /start',
        reply_markup=ReplyKeyboardMarkup([['/start']], one_time_keyboard=True, resize_keyboard=True)
    )
    return ConversationHandler.END

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🤖 Это бот-тест 'Кто ты из Смешариков?'\n\n"
        "📝 Используйте команды:\n"
        "/start - начать тест\n"
        "/help - показать справку\n"
        "/cancel - отменить тест\n\n"
        "🎭 Узнай, кто ты из 9 Смешариков!"
    )

async def list_characters(update: Update, context: ContextTypes.DEFAULT_TYPE):
    characters_list = [
        "🐰 Крош - энергичный заяц", "🦔 Ёжик - умный друг", "🐑 Бараш - творческий поэт",
        "🐧 Пин - изобретательный пингвин", "🦌 Лосяш - учёный философ", "🐦 Кар-Карыч - мудрый ворон",
        "🦉 Совунья - заботливая сова", "🐷 Нюша - романтичная модница", "🐻 Копатыч - трудолюбивый медведь"
    ]

    await update.message.reply_text(
        "🎭 Все Смешарики:\n\n" + "\n".join(characters_list) +
        "\n\n✨ Напишите /start чтобы узнать кто вы!"
    )

def main():
    try:
        application = Application.builder().token(TOKEN).build()

        conv_handler = ConversationHandler(
            entry_points=[CommandHandler('start', start)],
            states={
                QUESTION_1: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_question_1)],
                QUESTION_2: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_question_2)],
                QUESTION_3: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_question_3)],
                QUESTION_4: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_question_4)],
                QUESTION_5: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_question_5)],
                QUESTION_6: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_question_6)],
                QUESTION_7: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_question_7)],
                QUESTION_8: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_question_8)],
            },
            fallbacks=[CommandHandler('cancel', cancel)]
        )

        application.add_handler(conv_handler)
        application.add_handler(CommandHandler("help", help_command))
        application.add_handler(CommandHandler("characters", list_characters))

        application.run_polling()

    except Exception as e:
       
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()