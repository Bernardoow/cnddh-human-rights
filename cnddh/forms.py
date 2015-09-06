# coding=latin-1

from wtforms import Form

from wtforms import validators
from wtforms_components import DateRange
from wtforms import SelectField, TextField, DateField, TextAreaField, BooleanField, RadioField, FormField, SubmitField, FieldList, StringField, HiddenField, SelectMultipleField, FileField, PasswordField, IntegerField
from utils import NonLazyFormField
from mapeamentos import estados_choices, sexo_choices, cor_choices, situacao_choices, periodo_choices, tipoassistencia_choices, politicas_choices

from datetime import date

# Widgets
class RequiredIf(object):

    def __init__(self, other_field_name):
        self.other_field_name = other_field_name

    def __call__(self, form, field):        
        other_field = form._fields.get(self.other_field_name)        
        if other_field is None:            
            raise Exception('no field named "%s" in form' % self.other_field_name)
        if bool(other_field.data):            
            if not field.data:
                raise validators.ValidationError(u'Campo requerido.')    

class RequiredIfNot(object):

    def __init__(self, other_field_name):
        self.other_field_name = other_field_name

    def __call__(self, form, field):        
        other_field = form._fields.get(self.other_field_name)        
        if other_field is None:            
            raise Exception('no field named "%s" in form' % self.other_field_name)
        if not bool(other_field.data):            
            if not field.data:
                raise validators.ValidationError(u'Campo requerido.')                     
                
class AttrDict(dict):
    def __init__(self, *args, **kwargs):
        super(AttrDict, self).__init__(*args, **kwargs)
        self.__dict__ = self           

class DateShouldGreatherThan(object):

    def __init__(self, other_field_name):
        self.other_field_name = other_field_name

    def __call__(self, form, field):        
        other_field = form._fields.get(self.other_field_name)          
        if other_field is None:            
            raise Exception('no field named "%s" in form' % self.other_field_name)
        if field.data <= other_field.data:            
            raise validators.ValidationError(u'A data deve ser maior que %s.' %self.other_field_name)    
        
   
class EnderecoSomenteForm(Form):   
    tipolocal = SelectField(u"Tipo local", [validators.Required(u"Este campo � obrigat�rio.")], choices=[]) 
    endereco = TextField(u"Endere�o")
    num = TextField(u"N�", [validators.Length(max=6, message=u'Favor insira no m�ximo 5 n�meros.')])
    complemento = TextField(u"Complemento")    
    referencia = TextField(u"Refer�ncia", description=u"Exemplo: Pr�ximo a rododiv�ria.")   
    bairro = TextField(u"Bairro")    
    estado = SelectField(u"Estado", [validators.Required(u"Este campo � obrigat�rio.")], choices=estados_choices) 
    cidade = SelectField(u"Cidade", choices=[], default="")
    cep = TextField(u"CEP")               
    pais = TextField(u"Pais")               
    
class VitimaForm(Form):
    denuncia_id = HiddenField("Denuncia")
    vitima_id = HiddenField("Vitima")
    tipovitima = SelectField(u"Tipo", choices=[], default="")   
    qtdevitimas = SelectField(u"Quantidade de vitimas", choices=[(str(i),str(i)) for i in range(1,1001)], default="1") 
    qtdenaoespecificado = BooleanField(u"Quantidade n�o especificada")        
    nomenaoidentificado = BooleanField(u"Nome n�o identificado")    
    nome =  TextField(u"Nome ou apelido",  validators=[RequiredIfNot('nomenaoidentificado')]) 
    idade =  IntegerField(u"Idade", [validators.NumberRange(min=0, max=100, message=u"Digite um valor n�mero entre 0 e 100 anos.")])    
    sexo =  SelectField(u"Sexo", [validators.Required(u"Este campo � obrigat�rio.")], choices=sexo_choices)  
    cor =  SelectField(u"Cor", [validators.Required(u"Este campo � obrigat�rio.")], choices=cor_choices) 
    
class SuspeitoForm(Form):
    denuncia_id = HiddenField("Denuncia")
    suspeito_id = HiddenField("Suspeito")
    tiposuspeito = SelectField(u"Tipo", [validators.Required("Escolha o tipo do suspeito")], choices=[])
    qtdenaoespecificado = BooleanField(u"Quantidade n�o especificada")        
    qtdesuspeitos = SelectField(u"Quantidade de suspeitos", choices=[(str(i),str(i)) for i in range(1,1001)], default="1") 
    instituicao = SelectField(u"Institui��o", [validators.Required(u"Este campo � obrigat�rio.")], choices=[]) 
    classificacao = SelectField(u"Classifica��o do suspeito",[validators.Required(u"Este campo � obrigat�rio.")], choices=[])   
    nomeinstituicao =  TextField(u"Nome do org�o")     
    nomenaoidentificado = BooleanField(u"Nome n�o identificado")
    nome =  TextField(u"Nome ou apelido do suspeito")      
    idade =  IntegerField(u"Idade", [validators.NumberRange(min=0, max=100, message=u"Digite um valor n�mero entre 0 e 100 anos.")])  
    sexo =  SelectField(u"Sexo", [validators.Required(u"Este campo � obrigat�rio.")], choices=sexo_choices)  
    cor =  SelectField(u"Cor", [validators.Required(u"Este campo � obrigat�rio.")], choices=cor_choices)     
    
class DenunciaForm(Form):
    numero = TextField(u"N�mero", [validators.Required(u"Este campo � obrigat�rio.")])    
    dtdenuncia = DateField(u"Data da ocorr�ncia da den�ncia", [validators.Required(u"Este campo � obrigat�rio.")], format="%d/%m/%Y")
    resumo = TextField(u"Resumo", [validators.Required(u"Este campo � obrigat�rio.")])    
    descricao = TextAreaField(u"Descri��o", [validators.Required(u"Este campo � obrigat�rio."), validators.Length(max=4096, message=u'Favor insira uma descri��o de no m�ximo 4096 caracteres.')])
    observacao = TextAreaField(u"Observa��o", [validators.Length(max=8192, message=u'Favor insira uma observa��o de no m�ximo 8192 caracteres.')])    
    tipofonte_id = SelectField(u"Tipo de fontes", [validators.Required(u"Este campo � obrigat�rio.")], choices=[])
    fonte = TextField(u"Fonte",  description=u"Ex: Globo.com; (link da mat�ria); Jornal o Estado de S�o Paulo, etc.;")
    protocolo = TextField(u"Protocolo")
    
    endereco = NonLazyFormField(EnderecoSomenteForm, u"Endere�o", default=lambda: AttrDict(files='', tags=''))
    
class RelacionarForm(Form):
    denuncia_id = HiddenField("Denuncia")   
    macrocategoria = SelectField(u"Macro-categoria", [validators.Required(u"Este campo � obrigat�rio.")], choices=[])
    microcategoria = SelectMultipleField(u"Micro-categoria", [validators.Required(u"Este campo � obrigat�rio.")], choices=[])    
    suspeitos = SelectMultipleField(u"Suspeitos", choices=[])    
    vitimas = SelectMultipleField(u"Vitimas", choices=[])    
    
class FinalizarForm(Form):
    denuncia_id = HiddenField("Denuncia")
    descricaoanexo= TextField(u"Descri��o do anexo",validators=[RequiredIf('arquivo')])
    arquivo = FileField(u"Arquivo")       

class PesquisarForm(Form):
    numerodenuncia= TextField(u"N�mero da den�ncia")
    dtcriacaoinicio= DateField(u"Data de registro",[validators.Optional()], format="%d/%m/%Y")
    dtcriacaofim= DateField(u"Data da cria��o'fim", [validators.Optional()], format="%d/%m/%Y")
    dtocorinicio= DateField(u"Data da ocorr�ncia da den�ncia", [validators.Optional()], format="%d/%m/%Y")
    dtocorfim= DateField(u"Data da ocorr�ncia fim", [validators.Optional()], format="%d/%m/%Y")
    estado = SelectField(u"Estado", choices=estados_choices) 
    cidade = SelectField(u"Cidade", choices=[], default="")   
    palavrachave= TextField(u"Palavra chave")
    status = SelectMultipleField(u"Status", choices=[])  
   
class GraficoViolacaoForm(Form):
    macrocategoria = SelectField(u"Macro-categoria", [validators.Required(u"Este campo � obrigat�rio.")], choices=[])
    microcategoria = SelectField(u"Micro-categoria", [validators.Required(u"Este campo � obrigat�rio.")], choices=[])  
    dtocorinicio= DateField(u"Data da ocorr�ncia da den�ncia", [validators.Optional()], format="%d/%m/%Y")
    dtocorfim= DateField(u"Data da ocorr�ncia fim", [validators.Optional()], format="%d/%m/%Y")

class GraficoViolSuspForm(Form):
    macrocategoria = SelectField(u"Macro-categoria", [validators.Required(u"Este campo � obrigat�rio.")], choices=[])
    microcategoria = SelectField(u"Micro-categoria", [validators.Required(u"Este campo � obrigat�rio.")], choices=[])  
    tiposuspeito = SelectField(u"Tipo", [validators.Required("Escolha o tipo do suspeito")], choices=[])   
    
class TelephoneForm(Form):
    ddd = TextField('DDD', [validators.required(u"Este campo � obrigat�rio."),validators.Length(min=2, max=2, message=u"Informe o ddd com apenas 2 d�gitos.")])
    numero = TextField('Telefone',[validators.required(u"Este campo � obrigat�rio."),validators.Length(min=8, max=10, message=u"Informe o telefone com no m�ximo 10 d�gitos.")])    
    
class UsuarioForm(Form):
    login = TextField(u"Nome do usu�rio", [validators.Required(u"Este campo � obrigat�rio."),validators.Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,u'Nome de usu�rio deve contar somente letras, n�meros, pontos ou underscores'), validators.Length(min=3, max=16, message=u"Digite no m�nimo 5 caracteres e no m�ximo 16 caracteres.")])  
    nome = TextField(u"Nome", [validators.Required(u"Este campo � obrigat�rio."),validators.Length(min=5, max=80, message=u"Digite no m�nimo 5 caracteres e no m�ximo 80 caracteres.")])     
    email = TextField(u"Email", [validators.Required(u"Este campo � obrigat�rio."),validators.Email(message=u"Digite um email inv�lido"), validators.Length(min=5, max=200, message=u"Digite no m�nimo 5 caracteres e no m�ximo 200 caracteres.")])  
    telefone = FormField(TelephoneForm)
    senhaatual = PasswordField(u"Senha atual")
    senha = PasswordField(u"Senha",  [validators.Required(u"Este campo � obrigat�rio."),validators.Regexp('^(?=.*[A-Z])(?=.*[!@#$&*])(?=.*[0-9])(?=.*[a-z]).{8,16}$', 0,u'Uma senha segura deve contar pelo menos um caracter maisc�lo, 1 caracter especial (!@#$&*), algum d�gito n�merico, algum caracter minisc�lo e ser no m�nimo com 8 caracteres.')])
    confirmasenha = PasswordField(u"Confirma Senha", [validators.Required(u"Este campo � obrigat�rio."), validators.EqualTo('senha', message='Senhas devem ser iguais.')])

class LoginForm(Form):
    login = TextField(u"Usu�rio", [validators.Required()])
    senha = PasswordField(u"Senha", [validators.Required()])
    
class PermissaoForm(Form):
    nome = TextField(u"Nome", [validators.Required(u"Este campo � obrigat�rio")])
    descricao = TextField(u"Descri��o", [validators.Required(u"Este campo � obrigat�rio")])    
    
class PesquisaUsuarioForm(Form):
    login = TextField(u"Login", [validators.Optional()])
    nome  = TextField(u"Nome",  [validators.Optional()])
    #email = TextField(u"Email", [validators.Optional()])

class WorkflowForm(Form):
    numerodenuncia= TextField(u"N�mero da den�ncia")
    dtcriacaoinicio= DateField(u"Data de registro",[validators.Optional()], format="%d/%m/%Y")
    dtcriacaofim= DateField(u"Data da cria��o'fim", [validators.Optional()], format="%d/%m/%Y")
    dtocorinicio= DateField(u"Data da ocorr�ncia da den�ncia", [validators.Optional()], format="%d/%m/%Y")
    dtocorfim= DateField(u"Data da ocorr�ncia fim", [validators.Optional()], format="%d/%m/%Y")
    dtlimiteinicio= DateField(u"Data limite de retorno", [validators.Optional()], format="%d/%m/%Y")
    dtlimitefim= DateField(u"Data limite de retorno fim", [validators.Optional()], format="%d/%m/%Y")
    estado = SelectField(u"Estado", choices=estados_choices) 
    cidade = SelectField(u"Cidade", choices=[], default="")   
    palavrachave= TextField(u"Palavra chave")
    status = SelectMultipleField(u"Status", choices=[])  
    

class EncaminhamentoForm(Form):
    orgao = SelectField(u"Org�o de destino", choices=[])   
    tipo= SelectField(u"Tipo de encaminhamento", choices=[])          
    dtenvio= DateField(u"Data de envio", [validators.Required(u"Este campo � obrigat�rio."), DateRange(min=date(2010, 1, 1),max=date(2020, 12, 31), message=u"A data deve ser entre 01/01/2010 e 31/12/2020")], format="%d/%m/%Y")
    dtlimite= DateField(u"Data limite do retorno", [validators.Required(u"Este campo � obrigat�rio."), DateRange(min=date(2010, 1, 1),max=date(2020, 12, 31), message=u"A data deve ser maior que a data atual."), DateShouldGreatherThan('dtenvio')], format="%d/%m/%Y")        
    dtretorno= DateField(u"Data do retorno", [validators.Optional()], format="%d/%m/%Y")         

class RetornoForm(Form):
    resultado = TextAreaField(u"Resultado", [validators.Required(u"Este campo � obrigat�rio."), validators.Length(max=4096, message=u'Favor insira um resultado de no m�ximo 4096 caracteres.')])        
    obs = TextAreaField(u"Observa��o", [validators.Required(u"Este campo � obrigat�rio."), validators.Length(max=4096, message=u'Favor insira uma observa��o de no m�ximo 4096 caracteres.')])        
    arquivo = FileField(u"Arquivo")   

class OficioForm(Form):
    orgao = SelectField(u"Org�o de destino", choices=[])   
    dtenvio= DateField(u"Data de envio", [validators.Required(u"Este campo � obrigat�rio."), DateRange(min=date(2010, 1, 1),max=date(2020, 12, 31), message=u"A data deve ser entre 01/01/2010 e 31/12/2020")], format="%d/%m/%Y")
    dtlimite= DateField(u"Data limite do retorno", [validators.Required(u"Este campo � obrigat�rio."), DateRange(min=date(2010, 1, 1),max=date(2020, 12, 31), message=u"A data deve ser maior que a data atual."), DateShouldGreatherThan('dtenvio')], format="%d/%m/%Y")            
    numero = TextField(u"N�mero", [validators.Required(u"Este campo � obrigat�rio.")])    
    assunto = TextField(u"Resumo", [validators.Required(u"Este campo � obrigat�rio.")])        
    obs = TextAreaField(u"Observa��o", [validators.Required(u"Este campo � obrigat�rio."), validators.Length(max=4096, message=u'Favor insira uma observa��o de no m�ximo 4096 caracteres.')])        
    arquivo = FileField(u"Arquivo")       
    
class TelefonemaForm(Form):
    orgao = SelectField(u"Org�o de destino", choices=[])   
    dtenvio= DateField(u"Data de envio", [validators.Required(u"Este campo � obrigat�rio."), DateRange(min=date(2010, 1, 1),max=date(2020, 12, 31), message=u"A data deve ser entre 01/01/2010 e 31/12/2020")], format="%d/%m/%Y")
    dtlimite= DateField(u"Data limite do retorno", [validators.Required(u"Este campo � obrigat�rio."), DateRange(min=date(2010, 1, 1),max=date(2020, 12, 31), message=u"A data deve ser maior que a data atual."), DateShouldGreatherThan('dtenvio')], format="%d/%m/%Y")            
    numero = TextField(u"N�mero de telefone", [validators.Required(u"Este campo � obrigat�rio.")])    
    destinatario = TextField(u"Destinat�rio", [validators.Required(u"Este campo � obrigat�rio.")])        
    obs = TextAreaField(u"Observa��o", [validators.Required(u"Este campo � obrigat�rio."), validators.Length(max=4096, message=u'Favor insira uma observa��o de no m�ximo 4096 caracteres.')])        

class ReuniaoForm(Form):
    orgao = SelectField(u"Org�o de destino", choices=[])   
    dtenvio= DateField(u"Data de envio", [validators.Required(u"Este campo � obrigat�rio."), DateRange(min=date(2010, 1, 1),max=date(2020, 12, 31), message=u"A data deve ser entre 01/01/2010 e 31/12/2020")], format="%d/%m/%Y")
    dtlimite= DateField(u"Data limite do retorno", [validators.Required(u"Este campo � obrigat�rio."), DateRange(min=date(2010, 1, 1),max=date(2020, 12, 31), message=u"A data deve ser maior que a data atual."), DateShouldGreatherThan('dtenvio')], format="%d/%m/%Y")            
    pauta = TextField(u"Pauta", [validators.Required(u"Este campo � obrigat�rio.")])        
    participantes = TextField(u"Participantes", [validators.Required(u"Este campo � obrigat�rio.")])        
    obs = TextAreaField(u"Observa��o", [validators.Required(u"Este campo � obrigat�rio."), validators.Length(max=4096, message=u'Favor insira uma observa��o de no m�ximo 4096 caracteres.')])        
    arquivo = FileField(u"Arquivo")       
    
class EmailForm(Form):
    orgao = SelectField(u"Org�o de destino", choices=[])   
    dtenvio= DateField(u"Data de envio", [validators.Required(u"Este campo � obrigat�rio."), DateRange(min=date(2010, 1, 1),max=date(2020, 12, 31), message=u"A data deve ser entre 01/01/2010 e 31/12/2020")], format="%d/%m/%Y")
    dtlimite= DateField(u"Data limite do retorno", [validators.Required(u"Este campo � obrigat�rio."), DateRange(min=date(2010, 1, 1),max=date(2020, 12, 31), message=u"A data deve ser maior que a data atual."), DateShouldGreatherThan('dtenvio')], format="%d/%m/%Y")            
    para = TextField(u"Para", [validators.Required(u"Este campo � obrigat�rio.")])        
    de = TextField(u"De", [validators.Required(u"Este campo � obrigat�rio.")])        
    assunto = TextField(u"Assunto", [validators.Required(u"Este campo � obrigat�rio.")])        
    texto = TextAreaField(u"Texto", [validators.Required(u"Este campo � obrigat�rio."), validators.Length(max=4096, message=u'Favor insira uma observa��o de no m�ximo 4096 caracteres.')])        
    arquivo = FileField(u"Arquivo")   
    
class GenericoForm(Form):
    orgao = SelectField(u"Org�o de destino", choices=[])   
    dtenvio= DateField(u"Data de envio", [validators.Required(u"Este campo � obrigat�rio."), DateRange(min=date(2010, 1, 1),max=date(2020, 12, 31), message=u"A data deve ser entre 01/01/2010 e 31/12/2020")], format="%d/%m/%Y")
    dtlimite= DateField(u"Data limite do retorno", [validators.Required(u"Este campo � obrigat�rio."), DateRange(min=date(2010, 1, 1),max=date(2020, 12, 31), message=u"A data deve ser maior que a data atual."), DateShouldGreatherThan('dtenvio')], format="%d/%m/%Y")            
    obs = TextAreaField(u"Observa��o", [validators.Required(u"Este campo � obrigat�rio."), validators.Length(max=4096, message=u'Favor insira uma observa��o de no m�ximo 4096 caracteres.')])        
    arquivo = FileField(u"Arquivo")   
        
class RetornoForm(Form):    
    descricao = TextAreaField(u"Descri��o do retorno", [validators.Required(u"Este campo � obrigat�rio."), validators.Length(max=4096, message=u'Favor insira uma descri��o sobre o retorno de no m�ximo 4096 caracteres.')])        
    retorno = SelectField(u"Tipo do retorno", choices=[])  
    dtretorno= DateField(u"Data do retorno", [validators.Required(u"Este campo � obrigat�rio.")], format="%d/%m/%Y")
    observacao = TextAreaField(u"Observa��o", [validators.Length(max=4096, message=u'Favor insira uma observa��o de no m�ximo 4096 caracteres.')])  
    tipoassistencia = SelectMultipleField(u"Tipo de assist�ncia", choices=tipoassistencia_choices)   
    ip = TextField(u"N�mero do Inqu�rito Policial", [validators.Length(max=100, message=u'Favor insira n�mero de no m�ximo 100 posi��es.')])
    situacaoip = SelectField(u"Situa��o do Inquerito Policial", choices=situacao_choices)
    motivo = TextAreaField(u"Motivo", [validators.Length(max=4096, message=u'Favor insira uma observa��o de no m�ximo 4096 caracteres.')]) 
    np = TextField(u"N�mero do Processo", [validators.Length(max=100, message=u'Favor insira n�mero de no m�ximo 100 posi��es.')])  
    situacaop = SelectField(u"Situa��o do Processo", choices=situacao_choices)
    bo = TextField(u"Boletim de ocorr�ncia(BO)", [validators.Length(max=100, message=u'Favor insira n�mero de no m�ximo 100 posi��es.')])   
    rco = TextField(u"Relat�rio Circunstanciado de Ocorr�ncia (RCO)", [validators.Length(max=100, message=u'Favor insira n�mero de no m�ximo 100 posi��es.')])
    reds = TextField(u"Registro de Eventos de Defesa Social(REDS)", [validators.Length(max=100, message=u'Favor insira n�mero de no m�ximo 100 posi��es.')])
    tipopolitica = SelectMultipleField(u"Tipo de politica PSR", choices=politicas_choices)    
    arquivo = FileField(u"Arquivo")  
    
class HomicidioForm(Form):    
    rco = TextField(u"Relat�rio Circunstanciado de Ocorr�ncia (RCO)", [validators.Length(max=100, message=u'Favor insira n�mero de no m�ximo 100 posi��es.')])        
    bo = TextField(u"Boletim de ocorr�ncia(BO)", [validators.Length(max=100, message=u'Favor insira n�mero de no m�ximo 100 posi��es.')])
    ip = TextField(u"N�mero do Inqu�rito Policial", [validators.Length(max=100, message=u'Favor insira n�mero de no m�ximo 100 posi��es.')])
    situacao = SelectField(u"Situa��o do Inquerito Policial", choices=situacao_choices)
    reds = TextField(u"Registro de Eventos de Defesa Social(REDS)", [validators.Length(max=100, message=u'Favor insira n�mero de no m�ximo 100 posi��es.')])
    meioutilizado = SelectMultipleField(u"Meio utilizado", choices=[])
    prfato = SelectField(u"Per�odo do fato", choices=periodo_choices)
    obs = TextAreaField(u"Observa��o", [validators.Length(max=4096, message=u'Favor insira uma observa��o de no m�ximo 4096 caracteres.')])
    arquivo = FileField(u"Arquivo complementar da den�ncia")
    
class MotivoForm(Form):    
    motivo = TextAreaField(u"Observa��o", [validators.Required(u"Este campo � obrigat�rio."), validators.Length(max=1024, message=u'Favor insira uma observa��o de no m�ximo 1024 caracteres.')])            