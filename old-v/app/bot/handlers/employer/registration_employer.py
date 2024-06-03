from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from bot.keyboards import *
from bot.utils.states import *
from app.database.methods import *
from bot.handlers.bot_messages import *
from aiogram.exceptions import TelegramBadRequest

from datetime import datetime, timedelta

VERIFICATION_TIMEOUT = timedelta(seconds=1)

async def register_job_seeker(user_tgid, state: FSMContext):
    """
    Регистрация работодателя.
    :param employer_tgid: Telegram ID пользователя
    :param employer_tgname: Telegram username пользователя
    """
    # Здесь код для регистрации соискателя в базе данных:
    # await db.save_user(user_tgid, user_tgname, user_fullname, user_type="JOB_SEEKER")

    # Вместо прямого вызова функций proc_age и process_location будем устанавливать состояния FSM
    await state.set_state(EmployerForm.name)

# Вопрос про имя и фамилию представителя компании (работодатель)
@router.message(EmployerForm.name)
async def process_name(msg: Message, state: FSMContext):
    await state.update_data(name=msg.text)
    # Продолжаем диалог
    await state.set_state(EmployerForm.company_type)
    await msg.answer("Каков тип вашей компании? Выберите вариант ниже:", reply_markup=company_type)


# В зависимости от ответа идем дальше к вопросу о информации компании
@router.message(EmployerForm.company_type)
async def process_company_type(msg: Message, state: FSMContext):
    await state.update_data(company_type=msg.text)
    
    if msg.text == "ИП":
        await state.set_state(EmployerForm.individual_info)
        await msg.answer("Введите ваш ИНН:", 
                         reply_markup=rmk)
        
    elif msg.text == "Физическое лицо":
        await state.set_state(EmployerForm.physical_info)
        await msg.answer("Введите ваше ФИО",
                         reply_markup=rmk)
        
    elif msg.text == "Юр лицо (ООО, АО)":
        await state.set_state(EmployerForm.entity_info)
        await msg.answer("Введите название вашей компании, ОГРН, ИНН, КПП:",
                         reply_markup=rmk)
    else:
        await msg.answer("Пожалуйста, выберите один из предложенных вариантов.",
                         reply_markup=company_type)

#Обработка ИП
@router.message(EmployerForm.individual_info)
async def process_individual_info(msg: Message, state: FSMContext):
    await state.update_data(individual_info=msg.text)
    await state.set_state(EmployerForm.company_location)
    await msg.answer("Укажите город, где находится ваша компания. Например: Москва",
                    reply_markup=rmk)

# Обработка Физического лица
@router.message(EmployerForm.physical_info)
async def process_physical_info(msg: Message, state: FSMContext):
    await state.update_data(physical_info=msg.text)
    await state.set_state(EmployerForm.company_location)
    await msg.answer("Укажите город, где находится ваша компания. Например: Москва",
                    reply_markup=rmk)

# ШагОбработка Юридического лица
@router.message(EmployerForm.entity_info)
async def process_entity_info(msg: Message, state: FSMContext):
    await state.update_data(entity_info=msg.text)
    await state.set_state(EmployerForm.company_location)
    await msg.answer("Укажите город, где находится ваша компания. Например: Москва", 
                    reply_markup=rmk)


@router.message(EmployerForm.company_location)
async def process_companyname(msg: Message, state: FSMContext):
    await state.update_data(company_location=msg.text)
    await state.set_state(EmployerForm.company_verification)
    await msg.answer("""Отлично. Пока мы верефицируем аккаунт, вы можете выпить чашку свежего кофе ;)
Обычно это занимает около 5-7 минут..""", 
                    reply_markup=rmk)

@router.message(EmployerForm.company_verification)
async def process_verification(msg: Message, state: FSMContext):
    try:
        # Все сообщения, начиная с текущего и до первого (message_id = 0)
        for i in range(msg.message_id, 0, -1):
            await bot.delete_message(msg.from_user.id, i)
    except TelegramBadRequest as ex:
        # Если сообщение не найдено (уже удалено или не существует), 
        # код ошибки будет "Bad Request: message to delete not found"
        if ex.message == "Bad Request: message to delete not found":
            print("Все сообщения удалены")
    await msg.answer("Отправляем запрос на верификацию...",
                     reply_markup=rmk)

@router.message(Command("clear"))
async def cmd_clear(message: Message, bot: Bot) -> None:
    try:
        # Все сообщения, начиная с текущего и до первого (message_id = 0)
        for i in range(message.message_id, 0, -1):
            await bot.delete_message(message.from_user.id, i)
    except TelegramBadRequest as ex:
        # Если сообщение не найдено (уже удалено или не существует), 
        # код ошибки будет "Bad Request: message to delete not found"
        if ex.message == "Bad Request: message to delete not found":
            print("Все сообщения удалены")