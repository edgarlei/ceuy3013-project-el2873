oct20 = csv_redux('202010-citibike-tripdata.csv')
nov20 = csv_redux('202011-citibike-tripdata.csv')
comb = pd.concat([oct20, nov20])

oct20_run = oct20.head(n=15)

def add_col(data):
  for i in str(len(data)):
    data['year'] = data.starttime[int(i)][0:4]
    data['month'] = data.starttime[int(i)][5:7]
  return data

add_col(oct20_run)

def check_sample(data):
  lower_bound = data.tripduration.mean() - 0.25 * data.tripduration.std()
  upper_bound = data.tripduration.mean() + 0.25 * data.tripduration.std()
  def gen_sample():
    piece = data.sample(frac=0.25, axis=0)
    return piece
  sample = gen_sample()
  sam_td_mn = sample.tripduration.mean()
  while sam_td_mn > 0:
    if (sam_td_mn > lower_bound) & (sam_td_mn < upper_bound):
      break
    else:
      sample = gen_sample()
  return sample

check_sample(oct20)
