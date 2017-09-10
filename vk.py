# coding:utf8


SCRIPT_NAME = 'vk'
SCRIPT_AUTHOR = 'fogapod'
SCRIPT_VERSION = '0.0.1dev'
SCRIPT_LICENSE = 'MIT'
SCRIPT_DESC = 'vk.com messaging script'

try:
    import weechat
except ImportError:
    print('\nThis file should be run under WeeChat')

    import sys

    sys.exit(2)

import re

DEFAULT_SETTINGS = {
    'debug_logging': True,
    'token': ''
}

INSERT_TOKEN_COMMAND = 'insert-token'

BUFFER = ''


# TODO: use classes instead
# UTIL
def log_info(text, buffer=None,  note=0, error=0):
    if buffer is None:
        buffer = BUFFER

    message = '{0}: {1}'.format(SCRIPT_NAME, text)

    if get_setting('debug_logging'):
        # not very useful yet
        pass

    if note:
        message = NOTE_PREFIX + message
    elif error:
        message = ERROR_PREFIX + message

    weechat.prnt(buffer, message)


def log_debug(text, *args, **kwargs):
    if get_setting('debug_logging'):
        log_info('[DEBUG] ' + text, *args, **kwargs)


def set_default_settings():
    for setting, default_value in DEFAULT_SETTINGS.items():
        if not weechat.config_is_set_plugin(setting):
            log_debug('Creating: {0}:{1}'.format(setting, default_value))
            set_setting(setting, default_value)


def get_setting(key):
    if not weechat.config_is_set_plugin(key):
        return DEFAULT_SETTINGS[key]

    setting = weechat.config_get_plugin(key)
    setting_type = type(DEFAULT_SETTINGS[key])

    if setting_type is bool:
        return setting == 'True'
    else:
        return setting_type(setting)


def set_setting(key, value):
    log_debug('Saving: {0}:"{1}"'.format(key, value))
    weechat.config_set_plugin(key, str(value))


# BUFFER
def buffer_input_cb(data, buffer, input_data):
    # TODO: use '/vk command' instead or both methods
    lower_input_data = input_data.lower()
    args = lower_input_data.strip().split()[1:]

    if lower_input_data.startswith(INSERT_TOKEN_COMMAND):
        if not args:
            log_info('This command should be run with argument!', error=1)
        else:
            token = re.search('access_token=(.+?)&expires_in', args[0])
            if token:
                set_setting(TOKEN_SETTING_NAME, token.group(1))
                log_debug(token.group(1))
            else:
                log_info(
                    'Could not find token in url! Please, try again', error=1
                )

    return weechat.WEECHAT_RC_OK


def buffer_close_cb(data, buffer):
    log_info(
        'WARNING: This buffer should not be closed while script running. Use '
        '/python unload {0} if you want to exit'.format(SCRIPT_NAME), error=1
    )  # TODO: prevent closing buffer or open new after x seconds

    global BUFFER
    BUFFER = ''

    return weechat.WEECHAT_RC_OK


def create_buffer():
    global BUFFER

    if not BUFFER:
        BUFFER = weechat.buffer_new(
            SCRIPT_NAME, 'buffer_input_cb',
            'Main working window for ' + SCRIPT_NAME,
            'buffer_close_cb', ''
        )
        log_debug('Buffer created')


# BOT
class LongPollSession:

    def __init__(self):
        self.mlpd = None


def show_auth_hint():
    log_info(
        'Please, open this url, confirm access rights of the app and copy url'
        ' from address bar. Then use command {0} <copyed_url>'.format(
            INSERT_TOKEN_COMMAND)
    )
    log_info(
        'https://oauth.vk.com/authorize?client_id=6178678&scope=69636&v=5.68&'
        'response_type=token',
        note=1
    )


def main():
    if not weechat.register(
            SCRIPT_NAME, SCRIPT_AUTHOR, SCRIPT_VERSION,
            SCRIPT_LICENSE, SCRIPT_DESC, 'exit_cb', ''):
        return weechat.WEECHAT_RC_ERROR

    # registration required for accessing config
    global NOTE_PREFIX
    global ERROR_PREFIX

    NOTE_PREFIX = weechat.color(weechat.config_color(
        weechat.config_get('weechat.color.chat_prefix_join')
    )) + weechat.config_string(
        weechat.config_get('weechat.look.prefix_join')) + '\t'

    ERROR_PREFIX = weechat.color(weechat.config_color(
        weechat.config_get('weechat.color.chat_prefix_error')
    )) + weechat.config_string(
        weechat.config_get('weechat.look.prefix_error')) + '\t'

    create_buffer()
    set_default_settings()

    log_debug('Test note', note=1)
    log_debug('Test error', error=1)

    if not get_setting('token'):
        show_auth_hint()


def exit_cb():
    log_debug('Exiting')
    weechat.buffer_close(BUFFER)

    return weechat.WEECHAT_RC_OK


if __name__ == '__main__':
    main()
