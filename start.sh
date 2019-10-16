#!/bin/bash
#Starts the bot, alongside memory and CPU limits.
while :
do
	ulimit -m 24000000
	python3 bot.py & ./limit.sh
done
