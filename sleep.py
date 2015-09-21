#!/usr/bin/env python

from datetime import datetime, timedelta

DAYS_OF_WEEK = {
    0: 'Monday',
    1: 'Tuesday',
    2: 'Wednesday',
    3: 'Thursday',
    4: 'Friday',
    5: 'Saturday',
    6: 'Sunday'
    }
SPEEDS = {
    1: 'slow',
    3: 'fast'
    }


def transform(raw_sessions, user):

    sessions = []
    events = []

    print '[Info] Transforming {0} sessions...'.format(len(raw_sessions))
    for session in raw_sessions:
        
        s = {}
        s['user'] = user
        s['id'] = user + session['start']
        s['start_time'] = session['start']
        s['stop_time'] = session['stop']
        start_time = datetime.strptime(session['start'], '%Y-%m-%dT%H:%M:%S')
        stop_time = datetime.strptime(session['stop'], '%Y-%m-%dT%H:%M:%S')
        s['total_time'] = str(stop_time - start_time)
        s['num_events'] = len(session['events'])
        s['quality'] = 1 # algorithm
        s['day_of_week'] = {}
        s['day_of_week']['name'] = DAYS_OF_WEEK[start_time.weekday()]
        s['day_of_week']['value'] = start_time.weekday()
        s['keen'] = {}
        s['keen']['timestamp'] = session['start']
        sessions.append(s)

        for event in session['events']:
            e = {}
            e['user'] = user
            e['timestamp'] = (start_time + timedelta(seconds=event[0])).isoformat()
            e['id'] = user + e['timestamp']
            e['session_id'] = s['id']
            e['speed'] = {}
            e['speed']['name'] = SPEEDS[event[1]]
            e['speed']['value'] = event[1]
            e['intensity'] = event[2]
            e['keen'] = {}
            e['keen']['timestamp'] = e['timestamp']
            events.append(e)

    return sessions, events


if __name__ == '__main__':
    main()
