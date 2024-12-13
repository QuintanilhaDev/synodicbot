import asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
from flask import Flask


app = Flask(__name__)

@app.route('/')
def index():
    return "Bot está ativo!", 200

import threading

def run_flask():
    app.run(host="0.0.0.0", port=5000)

# Executar Flask em uma thread separada
thread = threading.Thread(target=run_flask)
thread.start()

TOKEN = '7619451682:AAH_A1bCWIMhs9-7thGUM7AVCKnwR2lmLQM'


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    message_text = "Oi! Tudo certo? \n Eu sou o Synodic Bot! Possuo informações sobre nosso projeto. Ah, quase me esqueci! Por favor, diga o que achou do nosso projeto no botão abaixo!"
    
    # Criar os botões do menu principal
    keyboard = [
        [
            InlineKeyboardButton("Sobre o projeto", callback_data='new_message'),
            InlineKeyboardButton("Avalie-nos", url='https://docs.google.com/forms/d/e/1FAIpQLSeaCn6Uo1jPLu2COQs5YqUWwNhV0tb4aIeE86_YjYZs-sIflw/viewform')
        ]
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    # Enviar a mensagem com os botões
    await update.message.reply_text(message_text, reply_markup=reply_markup)

# Função de callback para o botão "Enviar nova mensagem"
async def new_message_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.callback_query.answer()
    
    # Texto da nova mensagem
    new_message_text = "Sobre o SYNODIC \n \n O SYNODIC é uma ferramenta inovadora que facilita a prototipagem de projetos eletrônicos, permitindo que usuários importem circuitos em formato PDF e os convertam automaticamente em código Arduino. Com uma interface intuitiva, o SYNODIC simplifica o processo de desenvolvimento, tornando a criação de projetos acessível tanto para iniciantes quanto para entusiastas da eletrônica."
    
    # Criar o botão para voltar ao menu principal
    keyboard = [
        [InlineKeyboardButton("Voltar ao menu principal", callback_data='back_to_menu')]
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    # Editar a mensagem original ou enviar nova mensagem com o botão
    await update.callback_query.edit_message_text(new_message_text, reply_markup=reply_markup)

# Função de callback para o botão "Voltar ao menu principal"
async def back_to_menu_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.callback_query.answer()

    # Recriar o teclado do menu principal
    message_text = "Oi! Tudo certo? Eu sou o Synodic Bot! Possuo informações sobre nosso projeto. Ah, quase me esqueci! Por favor, diga o que achou do nosso projeto no botão abaixo!"
    keyboard = [
        [
            InlineKeyboardButton("Sobre o projeto", callback_data='new_message'),
            InlineKeyboardButton("Avalie-nos", url='https://docs.google.com/forms/d/e/1FAIpQLSeaCn6Uo1jPLu2COQs5YqUWwNhV0tb4aIeE86_YjYZs-sIflw/viewform')
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    # Editar a mensagem do botão "Voltar ao menu principal" para o menu principal
    await update.callback_query.edit_message_text(message_text, reply_markup=reply_markup)

# Função principal para rodar o bot
async def main() -> None:
    application = Application.builder().token(TOKEN).build()
    
    # Adiciona os handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(new_message_callback, pattern='new_message'))
    application.add_handler(CallbackQueryHandler(back_to_menu_callback, pattern='back_to_menu'))
    
    # Inicia o bot
    await application.run_polling()

# Rodando o bot diretamente, sem criar um loop manual
if __name__ == '__main__':
    application = Application.builder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(new_message_callback, pattern='new_message'))
    application.add_handler(CallbackQueryHandler(back_to_menu_callback, pattern='back_to_menu'))
    
    # Inicia o polling sem asyncio.run
    application.run_polling()
