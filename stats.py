SCORE_LOG = 'BVvBP.txt'

import json

LOG = []
with open (SCORE_LOG, 'r') as f:
    for l in f:
        _, _, payload = l.split(' | ')
        LOG.append(json.loads(payload))

QUARTER_TIME = 8 * 60

def _normalize_clock(clock: str, period: str) -> float:
    if ':' in clock:
        minutes, seconds = clock.split(':')
        t = int(minutes) * 60 + float(seconds)
    else:
        t = float(clock)
    quarter = int(period[:-2])

    return (QUARTER_TIME * quarter) - t

HOME_DATA = []
AWAY_DATA = []
DIFF_DATA = []

for i in range(1, len(LOG)):
    x = _normalize_clock(LOG[i]['clock'], LOG[i]['period'])
    if LOG[i]['home_score'] != LOG[i-1]['home_score']:
        HOME_DATA.append((x, LOG[i]['home_score']))
        DIFF_DATA.append((x, LOG[i]['home_score'] - LOG[i]['visitor_score']))
    if LOG[i]['visitor_score'] != LOG[i-1]['visitor_score']:
        AWAY_DATA.append((x, LOG[i]['visitor_score']))
        DIFF_DATA.append((x, LOG[i]['home_score'] - LOG[i]['visitor_score']))

final = _normalize_clock(LOG[-1]['clock'], LOG[-1]['period'])
HOME_DATA.append((final, LOG[-1]['home_score']))
AWAY_DATA.append((final, LOG[-1]['visitor_score']))
DIFF_DATA.append((final, LOG[-1]['home_score'] - LOG[-1]['visitor_score']))

import matplotlib as mpl
import matplotlib.pyplot as plt

# plt.xticks([QUARTER_TIME * q for q in range(0, 4)], ['1st', '2nd', '3rd', '4th'])
# fig, ax = plt.subplots(2, 1)
fig, ax = plt.subplots(1, 1)
fig.set_facecolor('black')

ax.set_xticks([QUARTER_TIME * q for q in range(0, 5)], ['Q1', 'Q2', 'Q3', 'Q4', 'F'], color='white')
ax.set_xlabel('Time', color='white')
ax.set_yticks([q * 5 for q in range(0, 100)], [str(q * 5) for q in range(0, 100)], color='white')
ax.set_ylabel('Score', color='white')
ax.tick_params(color='white')
ax.set_facecolor('black')
ax.grid(True, color='white')
ax.step([d[0] for d in HOME_DATA], [d[1] for d in HOME_DATA], color='red', linewidth=2)
ax.step([d[0] for d in AWAY_DATA], [d[1] for d in AWAY_DATA], color='green', linewidth=2)

# ax[1].set_xticks([QUARTER_TIME * q for q in range(0, 4)], ['Q1', 'Q2', 'Q3', 'Q4'])
# ax[1].grid(True)
# ax[1].step([d[0] for d in DIFF_DATA], [d[1] for d in DIFF_DATA])
fig.savefig('bv-bp.png')