# Demo of Django Telegram Auth

First, open the app in a browser. Also open your Telegram client application.

<div align="center"><img src="img02.png"></div>


Now, you can log in using your Telegram account.

## Auth via Telegram Bot

Click the "Sign in with Telegram bot" button.

<div align="center"><img src="img13.png"></div>

You will be redirected to the Telegram bot. Click "Start".

<div align="center"><img src="img03.png"></div>

Bot send you message with an authorization link. Click "Continue here" button.

<div align="center"><img src="img14.png"></div>

After authorization, you will be redirected to your profile page in the app. The user's first and last name and username will be taken from your Telegram account. An additional photo will also be displayed if you also authorize in an alternative way (via a widget, for example).


<div align="center"><img src="img04.png"></div>

To exit the profile, press the button "Logout".

<div align="center"><img src="img15.png"></div>

## Auth via Telegram OAuth

Click the "Sign in with Telegram OAuth" button.

<div align="center"><img src="img16.png"></div>

You will be redirected to the page for entering your Telagram phone number.

<div align="center"><img src="img05.png"></div>

After entering the number, you will be sent a confirmation code from the official Telegram [notification account](https://t.me/TelegramSupport).

<div align="center"><img src="img06.png"></div>

Click “Confirm” to allow authorization. You will be redirected to your profile page in the app. Name, username and photo will be taken from your Telegram account

<div align="center"><img src="img07.png"></div>

To exit the profile, press the button "Logout".

<div align="center"><img src="img15.png"></div>

## Auth via Telegram Widget

Click the "Войти через Telegram" button.

<div align="center"><img src="img12.png"></div>

You will see a pop-up window confirming your Telegram phone number

<div align="center"><img src="img08.png"></div>

After entering the number, you will be sent a confirmation code from the official Telegram [notification account](https://t.me/TelegramSupport).

<div align="center"><img src="img09.png"></div>

Click “Confirm” to allow authorization. You will be redirected to your profile page in the app. Name, username and photo will be taken from your Telegram account

<div align="center"><img src="img10.png"></div>

Until the browser session is completed, you can log in without Telegram confirmation. In this case, you will see your avatar on the widget.

<div align="center"><img src="img11.png"></div>

To exit the profile, press the button "Logout".

<div align="center"><img src="img15.png"></div>

You can also read the complete installation and configuration guide in the [README](../README.md).