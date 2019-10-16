#!/bin/bash
#Limits CPU usage for the bot
sleep 8
cpulimit -l 50 -p `pgrep -f bot.py`;
