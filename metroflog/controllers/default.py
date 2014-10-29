# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## This is a sample controller
## - index is the default action of any application
## - user is required for authentication and authorization
## - download is for downloading files uploaded in the db (does streaming)
## - api is an example of Hypermedia API support and access control
#########################################################################

def index():
    if auth.user:
        if not session.saludo_inicial:
            session.saludo_inicial = True
            response.flash = 'Bienvenido: %s' % auth.user.first_name
            
    query = Publicacion.id > 0
    publicaciones = db(query).select(orderby=~Publicacion.fecha)
            
    return dict(publicaciones=publicaciones)


def crear_publicacion():
    form = FORM('Título: ',
                INPUT(_name='titulo', requires=IS_NOT_EMPTY()),
                INPUT(_type='submit'))
    
    if form.process(formname='publicacion').accepted:
        response.flash = 'Su título fue enviado correctamente'
        
    elif form.errors:
        response.flash = 'Controle el formulario'
    
    return dict()

def publicacion():
    
    Publicacion.titulo.requires = [IS_NOT_EMPTY(), IS_LENGTH(6)]
    
    form = SQLFORM(Publicacion)
    if form.accepts(request.vars, session):
        response.flash = 'Se ingresó un nueva publicación'
        
    elif form.errors:
        response.flash = 'Controle el formulario'
    
    return dict(form=form)


def publicacion_factory():
    form = SQLFORM.factory(Field('imagen', 'upload'),
                           Field('fecha', 'date'),
                           Field('usuario', 'reference auth_user'))
    form.fecha['_placeholder'] = 'yyyy/mm/dd'
    return dict(form=form)


def consulta():
    return dict()

def mostrar_resultado():
    query = Publicacion.titulo.lower().contains(request.vars.secondname)
    if not db(query).isempty():
        return db(query).select()
    return ''

def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/manage_users (requires membership in
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    """
    return dict(form=auth())


@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)


def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    return service()


@auth.requires_login() 
def api():
    """
    this is example of API with access control
    WEB2PY provides Hypermedia API (Collection+JSON) Experimental
    """
    from gluon.contrib.hypermedia import Collection
    rules = {
        '<tablename>': {'GET':{},'POST':{},'PUT':{},'DELETE':{}},
        }
    return Collection(db).process(request,response,rules)
