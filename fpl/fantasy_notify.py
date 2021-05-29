"""
Send automated emails about fantasy deadline
"""

import ultimate_fantasy as f
import email_notifs as e

deadline = f.fpl_players()._get_deadline()
format_deadline = str(deadline.hour) + ':' + str(deadline.minute) + ' ' + str(deadline.day) + '-' + str(deadline.month) + '-' + str(deadline.year)
message = 'The next deadline to make changes to you team for Fantasy Football is:<br><br>{}<br><br>https://fantasy.premierleague.com/'.format(format_deadline)
send_mail = e.notif(msg=message, subject='Next Fantasy Football Deadline')
