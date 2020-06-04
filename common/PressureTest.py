#!/usr/bin/python2
# -*- coding: utf-8 -*-
import requests
import json
import sys
import os
from loguru import logger
headers = {'Content-Type': 'application/json;charset=utf-8'}
api_url = "https://oapi.dingtalk.com/robot/send?access_token=36464a265945b1bae3d5fc414272958b2e0ea69caf1ab55ad9f5b2e26d031f87"

def msg():
    json_text= {
        "actionCard": {
            "title": 'subject',
            "text": 'text',
            "hideAvatar": "0",
            "btnOrientation": "0",
            "btns": [
                {
                    "title":'testing',
                    "actionURL": ""
                }
            ]
        },
        "msgtype": "actionCard"
    }

    logger.info(requests.post(api_url,json.dumps(json_text),headers=headers).content)

msg()