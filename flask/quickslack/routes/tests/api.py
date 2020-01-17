from flask import Blueprint, jsonify, request, render_template
from flask import current_app as app


test_api = Blueprint('test_api', __name__)


@test_api.route('/sc_test', methods=['GET', 'POST'])
def sc_test():

    channel_id = request.form.get('channel_id')

    messages_data = app.config['slack'].get_all_messages_from_channel(channel_id)

    return render_template('tests/dashboard.html', messages_data=messages_data)
