from flask import render_template, request, redirect, url_for, flash
from . import contacts_bp
from .forms import ContactForm
from .models import Contact, Group
from app import db


# Список контактів
# Список контактів із сортуванням і пошуком
@contacts_bp.route('/')
def contact_list():
    # Параметри сортування та пошуку
    sort_field = request.args.get('sort', 'name')  # Поле для сортування, за замовчуванням 'name'
    search_query = request.args.get('search', '').strip()  # Пошуковий запит

    # Базовий запит до бази даних
    query = Contact.query

    if search_query:
        query = query.filter(Contact.name.ilike(f"%{search_query}%"))

    contacts = query.order_by(sort_field).all()

    return render_template('contact_list.html', contacts=contacts, sort_field=sort_field, search_query=search_query)


# Деталі контакту
@contacts_bp.route('/<int:contact_id>')
def contact_detail(contact_id):
    contact = Contact.query.get_or_404(contact_id)
    return render_template('contact_detail.html', contact=contact)


# Додавання нового контакту
@contacts_bp.route('/add_contact', methods=['GET', 'POST'])
def add_contact():
    form = ContactForm()
    form.group_id.choices = [(g.id, g.name) for g in Group.query.all()]
    if form.validate_on_submit():
        existing_contact = Contact.query.filter_by(email=form.email.data).first()
        if existing_contact:
            flash("Контакт з такою email адресою вже існує!", "danger")
            return redirect(url_for('contacts.add_contact'))
        contact = Contact(
            name=form.name.data,
            email=form.email.data,
            phone=form.phone.data,
            group_id=form.group_id.data
        )
        db.session.add(contact)
        db.session.commit()
        flash("Контакт успішно додано!", "success")
        return redirect(url_for('contacts.add_contact'))
    return render_template('add_contact.html', form=form)
