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
                        # reply_with_generic_template(sender_id, [element])

                        do_rules(sender_id, message_text)

    return "ok", 200


def get_url(url):
    result = request.get(url)
    return json.loads(result.content)


def do_rules(recipient_id, message_text):
    rules = {
        "Hello": {"main": "Hi! I am your historic fashion look-book. Write me a year to look up haute couture from past centuries.", "image": "http://i2.cdn.turner.com/cnnnext/dam/assets/160122154934-serkan-cura-aw14-haute-couture-large-169.jpg", "subtitle": "Get inspired and mix it with today's styles."},
        "1900": {"main": "1900", "image": "http://image.glamourdaze.com/2013/09/dress-timeline-1900-to-1909.jpg", "subtitle": "This is a description apparently"},
        "1910": {"main": "Year: 1910", "image": "http://image.glamourdaze.com/2013/09/dress-timeline-1900-to-1909.jpg", "subtitle": "This is a description apparently"},
        "1920": {"main": "Year: 1920", "image": "http://image.glamourdaze.com/2014/04/1920s-DRESS-TIMELINE-eveningwear.jpg", "subtitle": "This is a description apparently"},
        "1930": {"main": "Year: 1930", "image": "http://www.marquise.de/en/themes/timeline/timeline6.jpg", "subtitle": "This is a description apparently"},
        "1940": {"main": "Year: 1940", "image": "http://cdn.vintagedancer.com/wp-content/uploads/1941-day-dresses-house-crop-petite1.jpg", "subtitle": "This is a description apparently"},
        "1950": {"main": "Year: 1950", "image": "http://fashion.lilithezine.com/images/1950s-Fashion-10.jpg", "subtitle": "This is a description apparently"},
        "1960": {"main": "Year: 1960", "image": "http://blogretro.vanityfair.it/files/2014/02/Moda-anni-Sessanta.jpg", "subtitle": "This is a description apparently"},
        "1970": {"main": "Year: 1970", "image": "https://s-media-cache-ak0.pinimg.com/564x/8f/72/a6/8f72a6458d0c961fe95f479ef8720a3f.jpg", "subtitle": "This is a description apparently"},
        "1980": {"main": "Year: 1980", "image": "https://blushingbtique.files.wordpress.com/2014/10/1980s-fashion.png", "subtitle": "This is a description apparently"},
        "1990": {"main": "Year: 1990", "image": "https://blushingbtique.files.wordpress.com/2014/10/1990s-fashion.png", "subtitle": "This is a description apparently"},
        "2000": {"main": "Year: 2000", "image": "http://www.ixdaily.com/storage/styles/article-large/public/article/3335519-e806d251.jpg?itok=SI-NKCHm", "subtitle": "This is a description apparently"},
        "2010": {"main": "Year: 2010", "image": "http://www.thechicfashionista.com/images/xfw201011.jpg.pagespeed.ic.ZVOF6fh_C3.jpg", "subtitle": "This is a description apparently"},
        "2011": {"main": "Year: 2011", "image": "http://3.bp.blogspot.com/-xJ-F4WvvTBM/TaDwodSsLvI/AAAAAAAACTk/9ovfmjdlmrI/s1600/Fall+2011+Fashion+Trends+-+The+Sweater+Set.jpg", "subtitle": "This is a description apparently"},
        "2012": {"main": "Year: 2012", "image": "http://xposuremodeling.com/wp-content/uploads/2012/09/fall-2012-fashion-trends-1.jpg", "subtitle": "This is a description apparently"},
        "2013": {"main": "Year: 2013", "image": "http://www.glamour.com/images/fashion/2013/03/spring-trends-river-promo-w724.jpg", "subtitle": "This is a description apparently"},
        "2014": {"main": "Year: 2014", "image": "http://www.eonline.com/eol_images/Entire_Site/2013810/rs_1024x759-130910092814-1024.croptops.cm.91013.jpg", "subtitle": "This is a description apparently"},
        "2015": {"main": "Year: 2015", "image": "http://1-moda.com/wp-content/uploads/2014/04/0222.jpg", "subtitle": "This is a description apparently"},
        "2016": {"main": "Year: 2016", "image": "http://ell.h-cdn.co/assets/16/10/1457396249-elle-fall-2016-trends-index.jpg", "subtitle": "This is a description apparently"},
        "2370": {"main": "Year: 2370", "image": "http://3.bp.blogspot.com/-55uX2TiFbJc/UY88OpJ_53I/AAAAAAAAOAg/85JWBgV8vUc/s1600/Dr_Beverly_Crusher03.jpg", "subtitle": "This is Doctor Beverly Crusher showing off some very classy starfleet attire. Quite common for humans in the year 2370."},
        "2020": {"main": "Year: 2020", "image": "https://s-media-cache-ak0.pinimg.com/236x/03/99/e6/0399e66e75115a5fbd3e6beb45465368.jpg", "subtitle": "This is a description apparently"},
        "2030": {"main": "Year: 2030", "image": "https://s-media-cache-ak0.pinimg.com/236x/ac/19/28/ac1928f6f20d9ab28ab6050b9bbb1158.jpg", "subtitle": "This is a description apparently"},
        "2040": {"main": "Year: 2040", "image": "https://s-media-cache-ak0.pinimg.com/564x/8e/19/d4/8e19d4faf7531c12b9e6bef8f2b7cb5e.jpg", "subtitle": "This is a description apparently"},
        "A long time ago in a galaxy far, far away": {"main": "A long time ago in a galaxy far, far away", "image": "https://s-media-cache-ak0.pinimg.com/564x/61/18/df/6118df6b6313409b149a860a12a4fa64.jpg", "subtitle": "This is Princess Leia showing off some on point space fashion."},

        #Replies to normal text
        "4000": {"main": "Sorry, I can’t predict the future, but join me bye travelling back in time!", "image": "https://nostalgicwardrobe.files.wordpress.com/2010/01/carl-bengtsson-photo7.jpg?w=600", "subtitle": "Send me the year you are nostalgic about."},
        "1850": {"main": "Sorry, fashionable fashion is not that old!", "image": "https://s-media-cache-ak0.pinimg.com/564x/fd/28/35/fd28353650c19fd224f0c70bc95cc28e.jpg", "subtitle": "Start with 1900!"},
        "car": {"main": "I am sorry, I did not understand you.", "image": "http://www.krass42.com/wp-content/uploads/2015/03/Katze-im-Kleiderschrank-533x400.jpg", "subtitle": "Please try again!"}

    }

    if message_text in rules:
        # reply_with_text(recipient_id, rules[message_text])
        hash = rules[message_text]
        element = create_generic_template_element(hash["main"], hash["image"], hash["subtitle"])
        reply_with_generic_template(recipient_id, [element])


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
