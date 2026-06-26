from pathlib import Path

from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    InputMediaPhoto,
    ReplyKeyboardMarkup
)
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
    MessageHandler,
    filters
)

from config import BOT_TOKEN
from datetime import datetime

BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"
IMAGES_DIR = BASE_DIR / "images"

WANT_TEXT = "Менеджер уже спешит к вам с предложением!!!"

PRODUCTS = {
    "dresses": [
        {
            "name": "Платье двойка макси",
            "price": "12 900 ₽",
            "sizes": "XS, S, M",
            "photo": "products/dresses/1.jpg",
        },
        {
            "name": "Платье двойка черное",
            "price": "14 300 ₽",
            "sizes": "S, M, L",
            "photo": "products/dresses/2.webp",
        },
        {
            "name": "Платье жакетное",
            "price": "17 700 ₽",
            "sizes": "S, M, L",
            "photo": "products/dresses/3.webp",
        },
        {
            "name": "Платье корректирующее серое",
            "price": "12 200 ₽",
            "sizes": "S, M, L",
            "photo": "products/dresses/4.jpg",
        },
        {
            "name": "Платье корректирующее белое",
            "price": "12 200 ₽",
            "sizes": "S, M, L",
            "photo": "products/dresses/5.webp",
        },
    ],
    "suits": [
        {
            "name": "Костюм вязаный КРАСНЫЙ",
            "price": "18 900 ₽",
            "sizes": "S, M, L",
            "photo": "products/suits/1.webp",
        },
        {
            "name": "Костюм вязаный СЕРЫЙ",
            "price": "17 000 ₽",
            "sizes": "S, M, L",
            "photo": "products/suits/2.webp",
        },
        {
            "name": "Костюм вязаный СИНИЙ",
            "price": "16 900 ₽",
            "sizes": "S, M, L",
            "photo": "products/suits/3.webp",
        },
        {
            "name": "Лонгслив с юбкой мини",
            "price": "13 700 ₽",
            "sizes": "S, M, L",
            "photo": "products/suits/4.webp",
        },
        {
            "name": "Топ с юбкой мини",
            "price": "22 500 ₽",
            "sizes": "S, M, L",
            "photo": "products/suits/5.webp",
        },
    ],
    "shoes": [
        {
            "name": "Туфли Maison Classic",
            "price": "11 900 ₽",
            "sizes": "36, 37, 38, 39",
            "photo": "shoes1.jpg",
        },
    ],
    "accessories": [
        {
            "name": "Сумка Karma Mini",
            "price": "8 900 ₽",
            "sizes": "one size",
            "photo": "accessories1.jpg",
        },
    ],
}

BESTSELLERS = [
    {
        "name": "Бестселлер #1 — Корсет утягивающий",
        "price": "12 900 ₽",
        "sizes": "XS, S, M",
        "photo": "bestcellers/1.jpg",
    },
    {
        "name": "Бестселлер #2 — Костюм Вязаный",
        "price": "18 900 ₽",
        "sizes": "S, M, L",
        "photo": "bestcellers/2.webp",
    },
    {
        "name": "Бестселлер #3 — Платье жакет",
        "price": "8 900 ₽",
        "sizes": "S, M, L",
        "photo": "bestcellers/3.webp",
    },
    {
        "name": "Бестселлер #4 — Платье корректирующее",
        "price": "15 500 ₽",
        "sizes": "S, M, L",
        "photo": "bestcellers/4.jpg",
    },
    {
        "name": "Бестселлер #5 — Топ с юбкой миди",
        "price": "11 900 ₽",
        "sizes": "S, M, L",
        "photo": "bestcellers/5.jpg",
    },
]

LOOKS = [
    {
        "name": "Образ #1 — Корсет с юбкой мини",
        "price": "24 900 ₽",
        "sizes": "XS–M",
        "photo": "looks/1.webp",
    },
    {
        "name": "Образ #2 — Костюм вязаный серый",
        "price": "29 900 ₽",
        "sizes": "S–L",
        "photo": "looks/2.webp",
    },
    {
        "name": "Образ #3 — Лонгслив с юбкой мини",
        "price": "21 900 ₽",
        "sizes": "XS–L",
        "photo": "looks/3.webp",
    },
    {
        "name": "Образ #4 — Платье корректирующее белое",
        "price": "26 900 ₽",
        "sizes": "S–M",
        "photo": "looks/4.webp",
    },
    {
        "name": "Образ #5 — Топ с юбкой мини",
        "price": "32 900 ₽",
        "sizes": "XS–M",
        "photo": "looks/5.webp",
    },
]


def read_text_file(filename: str) -> str:
    path = DATA_DIR / filename
    return path.read_text(encoding="utf-8")


def main_menu_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("Каталог", callback_data="menu:catalog")],
        [InlineKeyboardButton("Бестселлеры", callback_data="menu:bestsellers")],
        [InlineKeyboardButton("Готовые образы", callback_data="menu:looks")],
        [InlineKeyboardButton("О нас", callback_data="menu:about")],
    ])


def catalog_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("Платья", callback_data="catalog:dresses")],
        [InlineKeyboardButton("Костюмы", callback_data="catalog:suits")],
        [InlineKeyboardButton("Обувь", callback_data="catalog:shoes")],
        [InlineKeyboardButton("Аксессуары", callback_data="catalog:accessories")],
        [InlineKeyboardButton("Назад в меню", callback_data="back:menu")],
    ])


def want_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("Хочу", callback_data="want")]
    ])


async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    text = update.message.text

    if text == "Меню":
        context.user_data["waiting_for_question"] = False
        await menu(update, context)
        return

    if context.user_data.get("waiting_for_question"):
        user = update.effective_user

        questions_file = DATA_DIR / "questions.txt"

        question_record = (
            "\n--- Новый вопрос ---\n"
            f"Дата: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
            f"User ID: {user.id}\n"
            f"Username: @{user.username if user.username else 'нет'}\n"
            f"Имя: {user.full_name}\n"
            f"Вопрос: {text}\n"
        )

        with questions_file.open("a", encoding="utf-8") as file:
            file.write(question_record)

        context.user_data["waiting_for_question"] = False

        await update.message.reply_text(
            "Менеджер скоро ответит на ваш вопрос"
        )
        return


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    text = read_text_file("welcome.txt")

    keyboard = ReplyKeyboardMarkup(
        [["Меню"]],
        resize_keyboard=True
    )

    logo_path = IMAGES_DIR / "logo.jpg"

    with logo_path.open("rb") as photo:
        await update.message.reply_photo(
            photo=photo,
            caption=text,
            reply_markup=keyboard
        )


async def menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "Выберите раздел:",
        reply_markup=main_menu_keyboard(),
    )


async def send_products(
        query,
        products: list[dict],
) -> None:
    for product in products:
        caption = (
            f"{product['name']}\n\n"
            f"Цена: {product['price']}\n"
            f"Размеры: {product['sizes']}"
        )

        photo_path = IMAGES_DIR / product["photo"]

        if photo_path.exists():
            with photo_path.open("rb") as photo:
                await query.message.reply_photo(
                    photo=photo,
                    caption=caption,
                    reply_markup=want_keyboard(),
                )
        else:
            await query.message.reply_text(
                caption + "\n\nФото пока не добавлено.",
                reply_markup=want_keyboard(),
            )


async def handle_buttons(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()

    data = query.data

    if data == "menu:catalog":
        await query.message.reply_text(
            "Выберите категорию:",
            reply_markup=catalog_keyboard(),
        )

    elif data.startswith("catalog:"):
        category = data.split(":")[1]
        products = PRODUCTS.get(category, [])

        if not products:
            await query.message.reply_text("В этой категории пока нет товаров.")
            return

        await send_products(query, products)

    elif data == "menu:bestsellers":
        await query.message.reply_text("Топ-5 бестселлеров месяца:")
        await send_products(query, BESTSELLERS)

    elif data == "menu:looks":
        await query.message.reply_text("Готовые образы Maison Karma:")
        await send_products(query, LOOKS)

    elif data == "about:question":
        context.user_data["waiting_for_question"] = True
        await query.message.reply_text("Напишите ваш вопрос одним сообщением:")

    elif data == "menu:about":
        about_text = read_text_file("about.txt")
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("Наши красотки", callback_data="about:beauties")],
            [InlineKeyboardButton("Задать вопрос", callback_data="about:question")],
            [InlineKeyboardButton("Назад в меню", callback_data="back:menu")],
        ])
        await query.message.reply_text(about_text, reply_markup=keyboard)

    elif data == "about:beauties":
        collage_path = IMAGES_DIR / "beauties_collage.jpg"

        if collage_path.exists():
            with collage_path.open("rb") as photo:
                await query.message.reply_photo(
                    photo=photo,
                    caption="Наши красотки Maison Karma 💔",
                )
        else:
            await query.message.reply_text("Коллаж пока не добавлен.")

    elif data == "want":
        await query.message.reply_text(WANT_TEXT)

    elif data == "back:menu":
        await query.message.reply_text(
            "Главное меню:",
            reply_markup=main_menu_keyboard(),
        )


def main() -> None:
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("menu", menu))
    app.add_handler(CallbackQueryHandler(handle_buttons))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))

    print("Bot started...")
    app.run_polling()


if __name__ == "__main__":
    main()
