import numpy as np

class Dataset(object):
  """Dataset.
  Format:
  user_id, business_id, stars, feature_1, [feature_2, ...]
  """
  def __init__(self, datafile):
    fdata = open(datafile, 'r')
    self.features = []
    self.labels = []

    for line in fdata:
      if line.strip() == '':
        continue

      else:
        line = line.strip().split(',')
        try:
          stars = float(line[3])
          if stars > 3:
            stars = 1.
          else:
            stars = 0.
          self.labels.append(stars)
          # self.features.append(map(float, line[4:26] + line[27:]))
          self.features.append(map(float, line[4:]))
        except:
          print(line)

    self.features = np.array(self.features, dtype=np.float32)
    self.labels = np.array(self.labels, dtype=np.float32)
