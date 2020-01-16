from flask import Blueprint, jsonify, request, render_template
from decouple import config
from slack_user_client import SlackClient

import requests


test_api = Blueprint('test_api', __name__)


@test_api.route('/sc_test', methods=['GET', 'POST'])
def sc_test():

    channel_id = request.form.get('channel_id')

    slack = SlackClient(
        config('SLACK_EMAIL'),
        config('SLACK_PASSWORD'),
        'https://lambdaschoolstudents.slack.com/'
    )

    slack.login()

    messages_data = slack.get_all_messages_from_channel(channel_id)

    return render_template('dashboard.html', messages_data=messages_data)
