#!/usr/bin/env python

from subprocess import call
import json
from datetime import datetime, timedelta
from keen.client import KeenClient
from sleep import transform
from params import keen

KEEN_PROJECT_ID = keen['project_id']
KEEN_WRITE_KEY = keen['write_key']
KEEN_READ_KEY = keen['read_key']

TIME_DELTA = 5
TIME_FRAME = 'this_5_days'


def main():

    call(['./get_sleep.sh'])

    with open('data_json.txt') as raw:
        print '[Info] Loading raw sleep data...'
        raw_sessions = json.load(raw)
        timestamp = (datetime.today() - timedelta(days=TIME_DELTA)).isoformat()
        chk_sessions = [s for s in raw_sessions if s['start'] > timestamp]
        
        if len(chk_sessions) > 0:
            print '[Info] Found {0} sleep sessions to check...'.format(len(chk_sessions))

            client = KeenClient(
                project_id = KEEN_PROJECT_ID,
                write_key = KEEN_WRITE_KEY,
                read_key = KEEN_READ_KEY
                )
            old_sessions = client.extraction('sessions', timeframe=TIME_FRAME)
            new_sessions = [s for s in chk_sessions if 'tyin' + s['start'] not in [s2['id'] for s2 in old_sessions]]

            if len(new_sessions) > 0:
                print '[Info] Found {0} sleep sessions to add...'.format(len(new_sessions))
                sessions = []
                events = []
                sessions, events = transform(new_sessions, 'tyin')

                client.add_events({'sessions': sessions, 'events': events})
                print '[Info] Added {0} sleep sessions.'.format(len(new_sessions))

    print '[Info] Done.'


if __name__ == '__main__':
    main()
