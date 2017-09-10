# VK on WeeChat
This script will allow you to chat on [VKontakte](https://vk.com) using [WeeChat](https://www.weechat.org/).

## Usage
Drop `vk.py` into `~.weechat/python/`  
To enable autorun for script, run `ln -s ~/.weechat/python/vk.py ~/.weechat/python/autoload/vk.py`

Open Weechat and type `/python load vk.py` (if not added to autoload or weechat was already running)  
Go to the vk buffer (upper left corner)

You will need special token for accessing VKontakte [API](https://vk.com/dev/manuals)
To get this token, open [this url](https://oauth.vk.com/authorize?client_id=6178678&scope=69636&v=5.68&response_type=token) in you webbrowser, confirm access rights for the app and copy url you was redirected to.
Type `insert-token <copyed_url>` inside of `vk` buffer to save your token.

`# TODO: auth without external browser`
