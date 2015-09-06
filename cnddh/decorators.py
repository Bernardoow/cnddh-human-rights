# coding=latin-1
from flask import request, g
from flask import abort, flash

from functools import wraps

def checa_permissao(permissao):
    def decorator(f):
        @wraps(f)
        def inner(*args, **kwargs):
            if g.user and g.user.checa_permissao(permissao):
                return f(*args, **kwargs)
            else:
                flash(u'Aten��o voc� n�o possui a permiss�o: %s. Se isto n�o estiver correto, entre em contato solicitando esta permiss�o.' % permissao.upper(),u'notice')
                abort(401)
        return inner
    return decorator
