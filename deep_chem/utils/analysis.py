"""
Utility functions to compare datasets to one another.
"""
__author__ = "Bharath Ramsundar"
__copyright__ = "Copyright 2015, Stanford University"
__license__ = "LGPL"

import numpy as np

def results_to_csv(results_dict):
  """Pretty prints results as CSV line."""
  targets = sorted(results_dict.keys())
  print ",".join(targets)
  print ",".join([str(results_dict[target]) for target in targets])

def summarize_distribution(y):
  """Analyzes regression dataset.

  Parameters
  ----------
  y: np.ndarray 
    A 1D numpy array containing distribution.
  """
  mean = np.mean(y)
  std = np.std(y)
  minval = np.amin(y)
  maxval = np.amax(y)
  hist = np.histogram(y)
  print "Mean: %f" % mean
  print "Std: %f" % std
  print "Min: %f" % minval
  print "Max: %f" % maxval
  print "Histogram: "
  print hist

def analyze_data(dataset, splittype="random"):
  """Analyzes regression dataset.

  Parameters
  ----------
  dataset: dict
    A dictionary of type produced by load_datasets.
  splittype: string
    Type of split for train/test. Either random or scaffold.
  """
  singletask = multitask_to_singletask(dataset)
  for target in singletask:
    data = singletask[target]
    if len(data.keys()) == 0:
      continue
    if splittype == "random":
      train, test = train_test_random_split(data, seed=0)
    elif splittype == "scaffold":
      train, test = train_test_scaffold_split(data)
    else:
      raise ValueError("Improper splittype. Must be random/scaffold.")
    _, Xtrain, ytrain, _ = dataset_to_numpy(train)
    # TODO(rbharath): Take this out once debugging is completed
    ytrain = np.log(ytrain)
    mean = np.mean(ytrain)
    std = np.std(ytrain)
    minval = np.amin(ytrain)
    maxval = np.amax(ytrain)
    hist = np.histogram(ytrain)
    print target
    print "Mean: %f" % mean
    print "Std: %f" % std
    print "Min: %f" % minval
    print "Max: %f" % maxval
    print "Histogram: "
    print hist


def compare_all_datasets():
  """Compare all datasets in our collection.

  TODO(rbharath): Make this actually robust.
  """
  muv_path = "/home/rbharath/vs-datasets/muv"
  pcba_path = "/home/rbharath/vs-datasets/pcba"
  dude_path = "/home/rbharath/vs-datasets/dude"
  pfizer_path = "/home/rbharath/private-datasets/pfizer"
  muv_data = load_datasets([muv_path])
  pcba_data = load_datasets([pcba_path])
  dude_data = load_datasets([dude_path])
  pfizer_data = load_datasets([pfizer_path])
  print "----------------------"
  compare_datasets("muv", muv_data, "pcba", pcba_data)
  print "----------------------"
  compare_datasets("pfizer", pfizer_data, "muv", muv_data)
  print "----------------------"
  compare_datasets("pfizer", pfizer_data, "pcba", pcba_data)
  print "----------------------"
  compare_datasets("muv", muv_data, "dude", dude_data)
  print "----------------------"
  compare_datasets("pcba", pcba_data, "dude", dude_data)
  print "----------------------"
  compare_datasets("pfizer", pfizer_data, "dude", dude_data)

def compare_datasets(first_name, first, second_name, second):
  """Counts the overlap between two provided datasets.

  Parameters
  ----------
  first_name: string
    Name of first dataset
  first: dict
    Data dictionary generated by load_datasets.
  second_name: string
    Name of second dataset
  second: dict
    Data dictionary generated by load_datasets.
  """
  first_scaffolds = set()
  for key in first:
    _, scaffold, _ = first[key]
    first_scaffolds.add(scaffold)
  print "%d molecules in %s dataset" % (len(first), first_name)
  print "%d scaffolds in %s dataset" % (len(first_scaffolds), first_name)
  second_scaffolds = set()
  for key in second:
    _, scaffold, _ = second[key]
    second_scaffolds.add(scaffold)
  print "%d molecules in %s dataset" % (len(second), second_name)
  print "%d scaffolds in %s dataset" % (len(second_scaffolds), second_name)
  common_scaffolds = first_scaffolds.intersection(second_scaffolds)
  print "%d scaffolds in both" % len(common_scaffolds)

