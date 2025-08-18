from flask import render_template, current_app
from flask_mail import Message
from . import mail

def send_email(subject, sender, recipients, text_body, html_body):
    """Função auxiliar para enviar e-mails."""
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    try:
        mail.send(msg)
    except Exception as e:
        # Log the error in a real application
        current_app.logger.error(f"Erro ao enviar e-mail: {e}")


def send_survey_email(cliente, pesquisa):
    """Envia o e-mail da pesquisa para um cliente."""
    subject = f"Queremos ouvir sua opinião: Pesquisa {pesquisa.nome}"
    sender = current_app.config['ADMINS'][0]
    recipients = [cliente.email]

    # Render the templates with the survey link
    text_body = render_template('email/survey_email.txt', cliente=cliente, pesquisa=pesquisa)
    html_body = render_template('email/survey_email.html', cliente=cliente, pesquisa=pesquisa)

    send_email(subject, sender, recipients, text_body, html_body)
