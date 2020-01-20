from flask import Blueprint, jsonify, request, render_template, flash
from flask import current_app as app
from .forms import Channel

dashboard = Blueprint('dashboard', __name__)


@dashboard.route('/messages', methods=['GET', 'POST'])
def messages():
    form = Channel()
    payload = []

    if form.validate_on_submit():

        channel_id = request.form.get('channel_id')

        payload = app.config['slack'].get_all_messages_from_channel(channel_id)

        flash(f'{channel_id} has been scrapped', 'success')
        return render_template('dashboard/pages/sccs_payload.html', form=form, payload=payload)

    return render_template('dashboard/content.html', form=form)
