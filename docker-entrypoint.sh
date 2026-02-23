#!/bin/sh

CRON_TIME="${CRON_TIME:-0 12 * * *}"

echo "$CRON_TIME cd /app/scraper/app && /usr/local/bin/python main.py >> /var/log/scraper.log 2>&1" > /etc/cron.d/scraper-cron

chmod 0644 /etc/cron.d/scraper-cron
crontab /etc/cron.d/scraper-cron

touch /var/log/scraper.log

echo "Cron job:"
crontab -l

exec cron -f