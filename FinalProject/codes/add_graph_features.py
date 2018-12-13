"""
Features:
  # text features
  0: food,
  1: specialNeed,
  2: alcohol,
  3: amount,
  4: service,
  5: efficiency,
  6: return
  7: recommend,
  8: overall,
  9: location,
  10: place,
  11: price,
  12: sanitation,
  # review features
  14: kolreview,
  15: social1rating,
  16: social2rating,
  # user features
  17: community,
  18: elite,
  19: closeness,
  20: betweenness,
  21: pagerank,
  22: avgstar,
  # business features
  23: zip_code,
  23: stars,
  24: c0fav,
  25: c3fav,
  26: c2fav,
  27: c9fav,
  28: c13fav,
  29: c42fav,
  30: c5fav,
  31: c19fav,
  32: c21fav,
  33: c54fav,
  34: c27fav,
  35: c34fav,
  36: c70fav,
  37: c10fav,
  38: c12fav,
  39: c33fav,
  40: c167fav
"""

import sys


def build_feature_dicts(review_file, user_file, business_file):
  feat_r, feat_u, feat_b = dict(), dict(), dict()

  for line in open(review_file, 'r').readlines()[1:]:
    if line.strip() != '':
      line = line.strip().split(',')
      feat_r[line[0]] = ','.join(line[2:])

  for line in open(user_file, 'r').readlines()[1:]:
    if line.strip() != '':
      line = line.strip().split(',')
      feat_u[line[0]] = ','.join(line[1:])

  for line in open(business_file, 'r').readlines()[1:]:
    if line.strip() != '':
      line = line.strip().split(',')
      feat_b[line[0]] = ','.join(line[1:])

  return feat_r, feat_u, feat_b


def add_features(in_file, out_file, feat_r, feat_u, feat_b):
  fin = open(in_file, 'r')
  fout = open(out_file, 'w')

  r404, u404, b404 = 0, 0, 0
  for line in fin:
    if line.strip() != '':
      line = line.strip().split(',')
      if line[0] not in feat_r:
        r404 += 1
      if line[1] not in feat_u:
        u404 += 1
      if line[2] not in feat_b:
        b404 += 1
      if line[0] in feat_r:
        r = feat_r[line[0]]
      else:
        continue
      if line[1] in feat_u:
        u = feat_u[line[1]]
      else:
        continue
      if line[2] in feat_b:
        b = feat_b[line[2]]
      else:
        continue
      line = ','.join(line + [r, u, b])
      fout.write(line + '\n')
  print('Missing r={}, u={}, b={}'.format(r404, u404, b404))


def main():
  review_file, user_file, business_file, in_file, out_file = sys.argv[1:6]
  feat_r, feat_u, feat_b = build_feature_dicts(
      review_file, user_file, business_file)
  add_features(in_file, out_file, feat_r, feat_u, feat_b)


if __name__ == '__main__':
  main()