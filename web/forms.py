from wtforms import Form, validators, StringField


class TykFormSix(Form):
    default_validations = [validators.Length(min=25, max=200)]
    pro_1 = StringField('pro_1', default_validations)
    pro_2 = StringField('pro_2', default_validations)
    pro_3 = StringField('pro_3', default_validations)
    con_1 = StringField('con_1', default_validations)
    con_2 = StringField('con_2', default_validations)
    con_3 = StringField('con_3', default_validations)


class TykFormTwo(Form):
    default_validations = [validators.Length(min=25, max=200)]
    pro_1 = StringField('pro_1', default_validations)
    con_1 = StringField('con_1', default_validations)
