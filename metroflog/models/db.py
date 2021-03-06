# -*- coding: utf-8 -*-

connectsqlite = 'sqlite://storage.db'
connectpostgres = 'postgres://postgres:parapente@localhost/cursoweb2py'


db = DAL(connectsqlite, pool_size=1, check_reserved=['all'])

response.generic_patterns = ['*'] if request.is_local else []


from gluon.tools import Auth, Service, PluginManager

auth = Auth(db)
service = Service()
plugins = PluginManager()

## create all tables needed by auth if not custom tables
auth.settings.extra_fields['auth_user']= [
  Field('direccion', requires=IS_NOT_EMPTY()),
  Field('ciudad'),
  Field('codigo_postal'),
  Field('telefono')]

auth.define_tables(username=False, signature=False)

## configure email
mail = auth.settings.mailer
mail.settings.server = 'smtp.gmail.com:587'
mail.settings.sender = 'debianitram@gmail.com'
mail.settings.login = 'debianitram:micontraseña'

## configure auth policy
# Esto es un comentario
auth.settings.registration_requires_verification = True
auth.settings.registration_requires_approval = False
auth.settings.reset_password_requires_verification = True

#db.define_table(name_table, *Fields, **attrb)

def calculo(registro):
    return registro['titulo'] + str(registro['fecha'])
    

Publicacion = db.define_table('publicacion',
                Field('titulo',
                      'string',
                      label='Nombre de la imagen',
                      length=30),
                Field('imagen', 'upload'),
                Field('descripcion', 'text'),
                Field('fecha',
                      'datetime',
                      default=request.now),
                Field('busqueda',
                      compute=calculo),
                Field('autor',
                      'reference auth_user',
                      default=auth.user_id),
                format='ID: %(id)s, %(titulo)s'                
                )

Saludo = db.define_table('saludo',
                Field('publicacion_id',
                      Publicacion),
                Field('mensaje', 'text'),
                Field('fecha',
                      'datetime',
                      default=request.now),
                Field('autor',
                      'reference auth_user',
                      default=auth.user_id),
                )
