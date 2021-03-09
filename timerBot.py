#!/usr/bin/env python

from discord import Webhook, RequestsWebhookAdapter
import datetime as dt
import sys
import time
import argparse

import credentials

# copied from the internet, generates "nd rd th... based on n"
ordinal = lambda n: "%d%s" % (n,"tsnrhtdd"[(n//10%10!=1)*(n%10<4)*n%10::4])

# generates a string of the form '**__THE FOLLOWING POSTS ARE FOR THE DATE OF:__** day, month DAYth, YEAR (Time posted in EST)'
def genDateString():
    now = dt.datetime.now()
    day = ordinal(int(dt.datetime.now().strftime('%-d')))
    d1 = now.strftime('%A, %B')
    d2 = now.strftime('%Y')
    date = f'{d1} {day}, {d2} (Time posted in EST)' 
    out = '**__THE FOLLOWING POSTS ARE FOR THE DATE OF:__** ' + date
    return out

def genWeekendString():
    now = dt.datetime.now()
    mon = now + dt.timedelta(days=2)
    monStr = mon.strftime('%A, %B')
    fri = now + dt.timedelta(days=6)
    friStr = fri.strftime('%A, %B')
    mondayDay = ordinal(int(mon.strftime('%-d')))
    fridayDay = ordinal(int(fri.strftime('%-d')))
    d2 = now.strftime('%Y')
    date = f' {monStr} {mondayDay}, {d2} to {friStr} {fridayDay}, {d2}' 
    #**__THE FOLLOWING POSTS ARE FOR THE WEEKEND PRECEDING:__** Monday, March 8th, 2021 to Friday, March 12th, 2021
    out = '**__THE FOLLOWING POSTS ARE FOR THE WEEKEND PRECEDING THE TRADING WEEK OF:__** ' + date
    return out

# sends message to channel if not using the '-test' arg. test arg sends to a private discord server channel with test webhook link.
def sendMessage(message, is_test=False, print_only=False):
    if print_only:
            print(message)
    if is_test:
        testwebhookURL = credentials.testwebhookURL
        testhook = Webhook.from_url(testwebhookURL, adapter=RequestsWebhookAdapter())
        testhook.send(message)
    elif not print_only:
        webhooktimerUrl = credentials.timerbot
        timerhook = Webhook.from_url(webhooktimerUrl, adapter=RequestsWebhookAdapter())
        timerhook.send(message)

def main():
    parser = argparse.ArgumentParser(description='Sends a messge to a discord chat at 12:01AM with the days date.')
    parser.add_argument('-p', '--print_only', action='store_true', help='Only print output, do not send to Discord')
    parser.add_argument('-t', '--test_server', action='store_true', help='Send to test channel/server, not production.')
    args = parser.parse_args()
    weekday = False
    weekday = dt.datetime.now().weekday() in range(0, 5)
    if weekday:
        message = genDateString()
        sendMessage(message, is_test=args.test_server, print_only=args.print_only)
    else:
        message = genWeekendString()
        sendMessage(message, is_test=args.test_server, print_only=args.print_only)

# sends messge when ran
if __name__ == "__main__":
    sys.exit(main())