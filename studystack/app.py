
import os
from flask import Flask, render_template, request, redirect, url_for, flash
from dotenv import load_dotenv
from sqlalchemy import func, or_
import bleach

from models import db, Subject, Tag, Summary, summary_tags

load_dotenv()

def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'uma-chave-padrão-de-desenvolvimento')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    @app.route('/')
    def index():
        """Página principal que exibe os resumos com filtros e busca."""

        search_query = request.args.get('q', '')
        filtro_subject_id = request.args.get('subject_id', '')
        filtro_tag_id = request.args.get('tag_id', '')

        subjects = Subject.query.order_by(Subject.name).all()
        tags = Tag.query.order_by(Tag.name).all()

        query = Summary.query

        if search_query:
            search_term = f"%{search_query}%"
            query = query.filter(
                or_(
                    Summary.title.ilike(search_term),
                    Summary.content.ilike(search_term)
                )
            )
        
        if filtro_subject_id:
            query = query.filter(Summary.subject_id == filtro_subject_id)
        
        if filtro_tag_id:
            query = query.join(Summary.tags).filter(Tag.id == filtro_tag_id)

        summaries = query.order_by(Summary.created_at.desc()).all()

        return render_template('index.html', 
                               summaries=summaries, 
                               subjects=subjects, 
                               tags=tags,
                               filtro_subject_id_ativo=filtro_subject_id,
                               filtro_tag_id_ativo=filtro_tag_id,
                               search_query=search_query)

    @app.route('/create', methods=['GET', 'POST'])
    def create_summary():
        if request.method == 'POST':
            title = request.form['title']
            content = request.form['content']
            subject_name = request.form['subject'].strip()
            tags_string = request.form['tags']

            if not all([title, content, subject_name]):
                flash('Título, Conteúdo e Matéria são campos obrigatórios!', 'erro')
                return render_template('create.html')

            subject = Subject.query.filter_by(name=subject_name).first()
            if not subject:
                subject = Subject(name=subject_name)
                db.session.add(subject)

            tags_objects = []
            if tags_string:
                tag_names = [name.strip() for name in tags_string.split(',') if name.strip()]
                for tag_name in tag_names:
                    tag = Tag.query.filter_by(name=tag_name).first()
                    if not tag:
                        tag = Tag(name=tag_name)
                        db.session.add(tag)
                    tags_objects.append(tag)
            
            new_summary = Summary(title=title, content=content, subject=subject)
            new_summary.tags.extend(tags_objects)
            
            db.session.add(new_summary)
            db.session.commit()

            flash('Resumo criado com sucesso!', 'sucesso')
            return redirect(url_for('view_summary', summary_id=new_summary.id))
        return render_template('create.html')

    @app.route('/summary/<int:summary_id>')
    def view_summary(summary_id):
        summary = Summary.query.get_or_404(summary_id)

        allowed_tags = {
            'p', 'br', 'strong', 'b', 'em', 'i', 'u', 'ul', 'ol', 'li', 
            'h1', 'h2', 'h3', 'a', 'img', 'blockquote'
        }
        allowed_attrs = {
            '*': ['class'],
            'a': ['href', 'title'],
            'img': ['src', 'alt', 'width', 'height']
        }
        
        sanitized_content = bleach.clean(
            summary.content, 
            tags=allowed_tags, 
            attributes=allowed_attrs
        )

        return render_template('view.html', summary=summary, content=sanitized_content)

    @app.route('/edit/<int:summary_id>', methods=['GET', 'POST'])
    def edit_summary(summary_id):
        summary = Summary.query.get_or_404(summary_id)
        
        if request.method == 'POST':
            summary.title = request.form['title']
            summary.content = request.form['content']
            subject_name = request.form['subject'].strip()
            tags_string = request.form['tags']

            subject = Subject.query.filter_by(name=subject_name).first()
            if not subject:
                subject = Subject(name=subject_name)
                db.session.add(subject)
            summary.subject = subject

            summary.tags.clear()
            if tags_string:
                tag_names = [name.strip() for name in tags_string.split(',') if name.strip()]
                for tag_name in tag_names:
                    tag = Tag.query.filter_by(name=tag_name).first()
                    if not tag:
                        tag = Tag(name=tag_name)
                        db.session.add(tag)
                    summary.tags.append(tag)
            
            db.session.commit()
            flash('Resumo atualizado com sucesso!', 'sucesso')
            return redirect(url_for('view_summary', summary_id=summary.id))
        return render_template('edit.html', summary=summary)

    @app.route('/delete/<int:summary_id>', methods=['POST'])
    def delete_summary(summary_id):
        summary = Summary.query.get_or_404(summary_id)
        db.session.delete(summary)
        db.session.commit()
        flash('Resumo excluído com sucesso!', 'sucesso')
        return redirect(url_for('index'))

    @app.route('/estatisticas')
    def estatisticas():
        total_obras = Summary.query.count()
        nota_media_raw = db.session.query(func.avg(Summary.id)).scalar() 
        nota_media = round(nota_media_raw, 2) if nota_media_raw else 0

        contagem_por_categoria = db.session.query(Subject.name, func.count(Summary.id)).join(Summary).group_by(Subject.name).order_by(Subject.name).all()
        contagem_por_tipo = [] 

        return render_template('estatisticas.html', 
                               total_obras=total_obras,
                               nota_media=nota_media, 
                               contagem_por_categoria=contagem_por_categoria,
                               contagem_por_tipo=contagem_por_tipo) 

    return app

if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        db.create_all()
    app.run(debug=True)