'''Intelligent Log "Anomalizer" 
Instead of just searching for "Error," this script reads a log file and uses a dictionary to count 
occurrences of every unique word. It then flags lines that contain words that appear in less than 
1% of the total log (finding the "needle in the haystack").
Key Libraries: collections.Counter, re.'''

from collections import Counter
import re

with open('demo.log','r') as f:
  content = f.read() 
  lines = []
  for line in content.splitlines(): 
    lines.append(re.sub(r'^\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}:\d{2}(?:,\d+)?\s*', '', line))
  updated_content = ' '.join(lines)
  words = updated_content.split(' ')
  c = Counter(words)
  threshold = 1/100*len(words)

  target_words = []
  for k,v in c.items():
    if v<threshold:
      target_words.append(k)

  updated_log=[]
  for line in content.splitlines():
    for target_word in target_words:
      if target_word in line:
        updated_log.append(line+' $')
        break
    else:
      updated_log.append(line)

with open('demo_anomaly.log','w') as f:
  for line in updated_log:
    f.write(line+'\n')