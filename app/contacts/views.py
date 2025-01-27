from flask import render_template, request, redirect, url_for, flash
from sqlalchemy import or_
from sqlalchemy.orm import joinedload

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
    query = Contact.query.options(joinedload(Contact.group))  # Завантажуємо групи для оптимізації

    # Пошук за кількома полями
    if search_query:
        query = query.filter(
            or_(
                Contact.name.ilike(f"%{search_query}%"),
                Contact.email.ilike(f"%{search_query}%"),
                Contact.phone.ilike(f"%{search_query}%"),
                Group.name.ilike(f"%{search_query}%")  # Пошук за назвою групи
            )
        )

    # Сортування
    if sort_field in ['name', 'email', 'phone']:  # Безпечна перевірка на допустимі поля
        query = query.order_by(getattr(Contact, sort_field))
    elif sort_field == 'group':  # Сортування за назвою групи
        query = query.join(Group).order_by(Group.name)

    contacts = query.all()

    return render_template(
        'contact_list.html',
        contacts=contacts,
        sort_field=sort_field,
        search_query=search_query
    )

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

# Редагування контакту
@contacts_bp.route('/edit/<int:contact_id>', methods=['GET', 'POST'])
def edit_contact(contact_id):
    contact = Contact.query.get_or_404(contact_id)
    form = ContactForm(obj=contact)
    form.group_id.choices = [(g.id, g.name) for g in Group.query.all()]

    if form.validate_on_submit():
        contact.name = form.name.data
        contact.email = form.email.data
        contact.phone = form.phone.data
        contact.group_id = form.group_id.data

        db.session.commit()
        flash("Контакт успішно оновлено!", "success")
        return redirect(url_for('contacts.contact_list'))

    return render_template('edit_contact.html', form=form, contact=contact)


# Видалення контакту
@contacts_bp.route('/delete/<int:contact_id>', methods=['POST'])
def delete_contact(contact_id):
    contact = Contact.query.get_or_404(contact_id)
    db.session.delete(contact)
    db.session.commit()
    flash("Контакт успішно видалено!", "success")
    return redirect(url_for('contacts.contact_list'))
