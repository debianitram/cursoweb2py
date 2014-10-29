def pub():
    publicacion = Publicacion(request.vars.id_publicacion) or redirect(URL(c='default', f='index'))
    query_saludo = Saludo.publicacion_id == publicacion.id
    rows_saludo = db(query_saludo).select(orderby=~Saludo.fecha)

    print request.vars 
    
    Saludo.mensaje.requires = IS_NOT_EMPTY()
    Saludo.publicacion_id.default = publicacion.id
    form = SQLFORM(Saludo, fields=['mensaje'])

    if form.accepts(request.vars, session):
        response.flash = 'Su publicación fue enviada con éxito'
    elif form.errors:
        response.flash = 'Controle el formulario'


    return dict(post=publicacion, comments=rows_saludo, form=form)


@auth.requires_membership('acceso_panel')
def panel():
    if auth.has_membership('secreto'):
        response.flash = 'Ud. es muy picante'
        return dict(grid=SPAN('Realmente es muy picante'))

    query = Publicacion.autor == auth.user.id
    grid = SQLFORM.grid(query,
                        links=[lambda r: A("Private", _href=URL('privacidad', args=r.id, user_signature=True))],
                        editable=auth.has_membership('edicion_publicacion'))
    return dict(grid=grid)


@auth.requires_signature()
def privacidad():
    # response.flash = request.args
    saludos = db(Saludo.publicacion_id == request.args(0)).select()
    
    return dict(saludos=saludos)

@auth.requires(auth.has_membership('acceso_panel') and request.now.weekday() == 1)
def verificacion_multiple():
    return dict()