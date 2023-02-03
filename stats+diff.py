SCORE_LOG = 'GVvFUHS.txt'

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
    if quarter <= 4:
        return (QUARTER_TIME * quarter) - t
    else:
        return (QUARTER_TIME * 4 + (QUARTER_TIME / 2 * (quarter - 4))) - t

HOME_DATA = [(0, 0)]
AWAY_DATA = [(0, 0)]
DIFF_DATA = [(0, 0)]

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
fig, ax = plt.subplots(2, 1)
# fig, ax = plt.subplots(1, 1)
fig.set_facecolor('black')
fig.set_figheight(12.5)
fig.set_figwidth(10)

reg = [QUARTER_TIME * q for q in range(0, 5)]
labels = ['Q1', 'Q2', 'Q3', 'Q4']
ots = int(LOG[-1]['period'][:-2]) - 4
for i in range(0, ots):
    reg.append(reg[-1] + QUARTER_TIME / 2)
    labels.append(f'OT{i + 1}')
labels.append('F')

# ax[0].set_xticks([QUARTER_TIME * q for q in range(0, 5)], ['Q1', 'Q2', 'Q3', 'Q4', 'F'], color='white')
ax[0].set_xticks(reg, labels, color='white')
# ax[0].set_xticks([QUARTER_TIME * q / 2 for q in range(0, 11)], [' ', 'Q1', ' ', 'Q2', ' ', 'Q3', ' ', 'Q4', 'OT1', 'OT2', 'F'], color='white')
ax[0].set_xlabel('Time', color='white')
ax[0].set_yticks([q * 5 for q in range(0, 100)], [str(q * 5) for q in range(0, 100)], color='white')
ax[0].set_ylabel('Score', color='white')
ax[0].tick_params(color='white')
ax[0].set_facecolor('black')
ax[0].grid(True, color='white')
ax[0].step([d[0] for d in AWAY_DATA], [d[1] for d in AWAY_DATA], color='white', linewidth=2, where='post', label='Troy')
ax[0].step([d[0] for d in HOME_DATA], [d[1] for d in HOME_DATA], color='red', linewidth=2, where='post', label='Fullerton')
ax[0].legend(loc='upper left', facecolor='black', framealpha=1, labelcolor='white')

# ax[1].set_xticks([QUARTER_TIME * q for q in range(0, 5)], ['Q1', 'Q2', 'Q3', 'Q4', 'F'], color='white')
ax[1].set_xticks(reg, labels, color='white')
ax[1].set_xlabel('Time', color='white')
ax[1].set_yticks([q * 5 for q in range(-100, 100)], [str(q * 5) for q in range(-100, 100)], color='white')
ax[1].set_ylabel('Score Differential', color='white')
ax[1].tick_params(color='white')
ax[1].set_facecolor('black')
ax[1].grid(True, color='white')

ax[1].step([d[0] for d in DIFF_DATA], [d[1] for d in DIFF_DATA], color='white', linewidth=2, where='post')
ax[1].step((0, final), (0, 0), color='red', linewidth=2)
diffs = []
for d in DIFF_DATA:
    diffs.append(d[1])
big = max(diffs)
small = -1 * min(diffs)
lim = max(big, small) + 5
ax[1].set_ylim([-1 * lim, lim])
fig.savefig(SCORE_LOG.replace('.txt', '.png'))