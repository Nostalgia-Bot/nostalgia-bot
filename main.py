# -*- coding: utf-8 -*-
import json, urllib
from flask import Flask, request, abort
import requests
import csv
import sqlite3

app = Flask(__name__)

access_token = 'EAARZC2QRJKt4BAOM1vWblZBT9Dmre9kaQkRrn8oRyakSL2s3RoaLVU9TGIeVndA6ch2fJJTmW0eAx7lzQWTBR2Iv9tKtvZBU7GCz1awDqqg0wObeF7sEyc9ZCF3nqpSJIg8R8YZAm5UuTGp5vxDZBLVlYZCGZCsnmWRpxikMzBTXBwZDZD'


@app.route("/", methods=["GET"])
def root():
    return "Hello World!"


# webhook for facebook to initialize the bot
@app.route('/webhook', methods=['GET'])
def get_webhook():

    if not 'hub.verify_token' in request.args or not 'hub.challenge' in request.args:
        abort(400)

    return request.args.get('hub.challenge')


@app.route('/webhook', methods=['POST'])
def post_webhook():
    data = request.json

    if data["object"] == "page":
        for entry in data['entry']:
            for messaging_event in entry['messaging']:

                if "message" in messaging_event:

                    sender_id = messaging_event['sender']['id']

                    if 'text' in messaging_event['message']:
                        message_text = messaging_event['message']['text']
                        image = "http://cdn.shopify.com/s/files/1/0080/8372/products/tattly_jen_mussari_hello_script_web_design_01_grande.jpg"
                        element = create_generic_template_element("Hello", image, message_text)
                        reply_with_generic_template(sender_id, [element])

                        # do_rules(sender_id, message_text)

    return "ok", 200


def get_url(url):
    result = request.get(url)
    return json.loads(result.content)


def do_rules(recipient_id, message_text):
    rules = {
        "Hello": create_generic_template_element("Hi, what year would you like to be inspired by?", "",""),
        "1900": create_generic_template_element("1900",	"http://image.glamourdaze.com/2013/09/dress-timeline-1900-to-1909.jpg", "This is a description apparently")

        # "1910": create_generic_template_element("1900",	"http://image.glamourdaze.com/2013/09/dress-timeline-1900-to-1909.jpg")
        #
        # "1920": create_generic_template_element("1900",	"http://image.glamourdaze.com/2014/04/1920s-DRESS-TIMELINE-eveningwear.jpg")
        #
        # "1930": create_generic_template_element("1900",	"http://www.marquise.de/en/themes/timeline/timeline6.jpg")
        #
        # "1940": create_generic_template_element("1900",	"http://cdn.vintagedancer.com/wp-content/uploads/1941-day-dresses-house-crop-petite1.jpg")
        #
        # "1950": create_generic_template_element("1900",	"http://fashion.lilithezine.com/images/1950s-Fashion-10.jpg")
        #
        # "1960": create_generic_template_element("1900",	"http://blogretro.vanityfair.it/files/2014/02/Moda-anni-Sessanta.jpg")
        #
        # "1970": create_generic_template_element("1900",	"https://s-media-cache-ak0.pinimg.com/564x/8f/72/a6/8f72a6458d0c961fe95f479ef8720a3f.jpg")
        #
        # "1980": create_generic_template_element("1900",	"https://blushingbtique.files.wordpress.com/2014/10/1980s-fashion.png")
        #
        # "1990": create_generic_template_element("1900",	"https://blushingbtique.files.wordpress.com/2014/10/1990s-fashion.png")
        #
        # "2000": create_generic_template_element("1900",	"http://www.ixdaily.com/storage/styles/article-large/public/article/3335519-e806d251.jpg?itok=SI-NKCHm")
        #
        # "2010": create_generic_template_element("1900",	"http://www.thechicfashionista.com/images/xfw201011.jpg.pagespeed.ic.ZVOF6fh_C3.jpg")
        #
        # "2011": create_generic_template_element("1900", "http://3.bp.blogspot.com/-xJ-F4WvvTBM/TaDwodSsLvI/AAAAAAAACTk/9ovfmjdlmrI/s1600/Fall+2011+Fashion+Trends+-+The+Sweater+Set.jpg")
        #
        # "2012": create_generic_template_element("1900",	"http://xposuremodeling.com/wp-content/uploads/2012/09/fall-2012-fashion-trends-1.jpg")
        #
        # "2013": create_generic_template_element("1900",	"http://www.glamour.com/images/fashion/2013/03/spring-trends-river-promo-w724.jpg")
        #
        # "2014": create_generic_template_element("1900",	"http://www.eonline.com/eol_images/Entire_Site/2013810/rs_1024x759-130910092814-1024.croptops.cm.91013.jpg")
        # "2015": create_generic_template_element("1900",	"http://1-moda.com/wp-content/uploads/2014/04/0222.jpg")
        #
        # "2016": create_generic_template_element("1900",	"http://ell.h-cdn.co/assets/16/10/1457396249-elle-fall-2016-trends-index.jpg")
        # "2370": create_generic_template_element("1900",	"http://3.bp.blogspot.com/-55uX2TiFbJc/UY88OpJ_53I/AAAAAAAAOAg/85JWBgV8vUc/s1600/Dr_Beverly_Crusher03.jpg")
        # "2350": create_generic_template_element("2350", "http://67.media.tumblr.com/ed79bc3e8dea303291861b4a27f5d2a7/tumblr_nur5eapJvA1qzx9wpo1_1280.jpg")
    }

    if message_text in rules:
        reply_with_text(recipient_id, rules[message_text])
        reply_with_generic_template(recipient_id, rules[message_text])


    else:
        reply_with_text(recipient_id, "You have to write something I understand ;)")


def reply_with_text(recipient_id, message_text):
    message = {
        "text": message_text
    }
    reply_to_facebook(recipient_id, message)


def reply_with_generic_template(recipient_id, elements):
    message = {
        "attachment": {
            "type": "template",
            "payload": {
                "template_type": "generic",
                "elements": elements
            }
        }
    }
    reply_to_facebook(recipient_id, message)


def reply_to_facebook(recipient_id, message):
    params = {
        "access_token": access_token
    }

    headers = {
        "Content-Type": "application/json"
    }

    data = json.dumps({
        "recipient": {
            "id": recipient_id
        },
        "message": message
    })

    url = "https://graph.facebook.com/v2.6/me/messages?" + urllib.urlencode(params)
    r = requests.post(url=url, headers=headers, data=data)


def create_generic_template_element(title, image_url, subtitle):
    return {
        "title": title,
        "image_url": image_url,
        "subtitle": subtitle
    }


if __name__ == '__main__':
    app.run(debug=True)
