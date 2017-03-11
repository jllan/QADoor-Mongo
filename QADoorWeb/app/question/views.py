from flask import Blueprint, render_template, url_for, request, flash, redirect, session, jsonify, current_app
from flask_login import current_user, login_required
from .models import Questions
from flask_mongoengine import Pagination

PER_PAGE = 20
question = Blueprint('question', __name__, url_prefix='')

@question.route('/', methods=['GET'])
@question.route('/<int:page>', methods=['GET'])
def question_index(page=1):
    # paginate = Questions.query.filter(Questions.id).paginate(page, PER_PAGE)
    pagination = Questions.objects.paginate(page=page, per_page=PER_PAGE)
    # return render_template('index.html', pagination=pagination)
    return render_template('index.html', questions=pagination.items, pagination=pagination)

@question.route('/search/', methods=['GET', 'POST'])
@question.route('/search/<string:keyword>/', methods=['GET', 'POST'])
@question.route('/search/<string:keyword>/<int:page>', methods=['GET', 'POST'])
def question_search(keyword='', page=1):
    # keyword = request.form['key']
    # keyword = request.form['key']
    print(keyword)
    questions = Questions.objects(title__icontains=keyword)
    pagination = Pagination(questions, page=page, per_page=PER_PAGE)
    return render_template('index.html', questions=pagination.items, pagination=pagination)

@question.route('/tag/<string:tag>/', methods=['GET'])
@question.route('/tag/<string:tag>/<int:page>', methods=['GET'])
def question_tag(tag, page=1):
    # paginate = Questions.query.filter(Questions.tags.like('%'+tag+'%')).paginate(page, PER_PAGE)
    questions = Questions.objects(tags=tag)
    pagination = Pagination(questions, page=page, per_page=PER_PAGE)
    return render_template('index.html', questions=pagination.items, pagination=pagination)

@question.route('/detail/<question_id>', methods=['GET'])
def question_detail(question_id):
    question = Questions.objects.get_or_404(_id=question_id)
    return render_template('question_detail.html', question=question)

@question.errorhandler(404)
def not_found(error):
    return render_template('404.html')
