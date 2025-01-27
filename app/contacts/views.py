from flask import render_template, request, redirect, url_for
from . import contacts_bp
from .models import Contact, Group
from app import db


# Список контактів
@contacts_bp.route('/')
def contact_list():
    contacts = Contact.query.all()
    return render_template('contacts/contact_list.html', contacts=contacts)


# Деталі контакту
@contacts_bp.route('/<int:contact_id>')
def contact_detail(contact_id):
    contact = Contact.query.get_or_404(contact_id)
    return render_template('contacts/contact_detail.html', contact=contact)


# Додавання нового контакту
@contacts_bp.route('/add', methods=['GET', 'POST'])
def add_contact():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form.get('phone')
        group_id = request.form.get('group_id')

        new_contact = Contact(name=name, email=email, phone=phone, group_id=group_id)
        db.session.add(new_contact)
        db.session.commit()
        return redirect(url_for('contacts.contact_list'))

    groups = Group.query.all()
    return render_template('contacts/add_contact.html', groups=groups)
