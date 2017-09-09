# coding:utf8


SCRIPT_NAME = 'vk'
SCRIPT_AUTHOR = 'fogapod'
SCRIPT_VERSION = '0.0.1dev'
SCRIPT_LICENSE = 'MIT'
SCRIPT_DESC = 'vk.com messaging plugin'

try:
    import weechat
except ImportError:
    print('\nThis file should be run under Weechat')

    import sys

    sys.exit(2)


def main():
    if weechat.register(
            SCRIPT_NAME, SCRIPT_AUTHOR, SCRIPT_VERSION,
            SCRIPT_LICENSE, SCRIPT_DESC, '', ''):
        # TODO: create plugin # easy
        pass


if __name__ == '__main__':
    main()
