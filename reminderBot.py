#!/usr/bin/env python
from discord import Webhook, RequestsWebhookAdapter
import sys
import argparse
import credentials

# sends message to channel if not using the '-test' arg. test arg sends to a private discord server channel with test webhook link.
def sendMessage(message, is_test=False, print_only=False):
    if print_only:
            print(message)
    if is_test:
        testwebhookURL = credentials.testwebhookURL
        testhook = Webhook.from_url(testwebhookURL, adapter=RequestsWebhookAdapter())
        testhook.send(message)
    elif not print_only:
        cryptohookURL = credentials.cryptohookURL
        cryptohook = Webhook.from_url(cryptohookURL, adapter=RequestsWebhookAdapter())
        cryptohook.send(message)

def main():
    parser = argparse.ArgumentParser(description='Sends a messge to a discord chat at 12:01AM with the days date.')
    parser.add_argument('-p', '--print_only', action='store_true', help='Only print output, do not send to Discord')
    parser.add_argument('-t', '--test_server', action='store_true', help='Send to test channel/server, not production.')
    args = parser.parse_args()
    message = "<@834577975369269248> This is your 10 minute warning for the Daily Candle Reset."
    sendMessage(message, is_test=args.test_server, print_only=args.print_only)

# sends messge when ran
if __name__ == "__main__":
    sys.exit(main())