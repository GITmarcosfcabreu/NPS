from flask_wtf import FlaskForm
from wtforms import RadioField, TextAreaField, SubmitField
from wtforms.validators import DataRequired

class SurveyForm(FlaskForm):
    """Formulário de pesquisa NPS."""
    score = RadioField(
        'Em uma escala de 0 a 10, o quão provável você é de nos recomendar a um amigo ou colega?',
        choices=[(i, str(i)) for i in range(11)],
        validators=[DataRequired(message="Por favor, selecione uma nota.")]
    )
    comment = TextAreaField(
        'O que poderíamos fazer para melhorar sua experiência? (opcional)'
    )
    submit = SubmitField('Enviar Resposta')
