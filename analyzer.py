import json
import sys

with open("timeline.json", "r") as read_file:
    data = json.load(read_file)

events = data['traceEvents']


max_ts = 0
min_ts = sys.maxint
total_dur_per_op = dict()
total_invocations = dict()
for e in events:
  if e['ph'] != 'X':
    continue

  ts = e['ts']
  args = e['args']
  dur = e['dur']
  op_name = args['name']
  op_type = args['op']

  max_ts = max(ts, max_ts)
  min_ts = min(ts, min_ts)

  if op_type in total_dur_per_op:
    total_dur_per_op[op_type] += dur
    total_invocations[op_type] += 1
  else:
    total_dur_per_op[op_type] = dur
    total_invocations[op_type] = 1

elapsed_time = max_ts - min_ts
print(elapsed_time/1000.0)

printed_item = 0
for key, val in sorted(total_dur_per_op.iteritems(), key=lambda (k,v):(v,k), reverse=True):
  percentage = val/float(elapsed_time)*100.0
  if percentage < 0.1:
    break;
  print '{:20} : {:5.3}%, {}, {:5.3}us'.format(
      key, percentage,
      total_invocations[key],
      float(val)/total_invocations[key])


