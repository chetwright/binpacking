'''
Bin Packing
Branch and Bound Binpacking and First Fit Decreasing
Implemented in Python
'''
import random
import csv
import time
import numpy
import sys

sys.setrecursionlimit(100000)
random.seed(567)

class Bin:    
    def __init__(self, capacity):
          self.capacity = capacity
          self.items = [] #int array of items added back in

    def remaining_space(self):
        return (self.capacity - sum(self.items))

    def does_item_fit(self, item):  #This might be redundant
        if ((self.remaining_space() - item) >= 0):
            #bug found: >= not >, causes extra bin on exact
            return True
        return False
    def add_item(self, item):
        self.items.append(item)  #check the syntax on this and next

    def remove_item(self, item):
        self.items.remove(item) 

    
def rand_distributed_set(capacity, items_count):
    items = []
    index = 0
    while items_count > 0:
        items_count = items_count - 1
        item = random.randint(1, capacity)  # Set the items to work within the capacity
        items.append(item)

    return items

def light_set(capacity, items_count):
    items = []
    while items_count > 0:
        items_count = items_count - 1
        item = random.randint(1,int(capacity*(0.5)))
        items.append(item)
    return items

def very_light_set(capacity, items_count):
    items = []
    while items_count > 0:
        items_count = items_count - 1
        item = random.randint(1,int (capacity*(0.25)))
        items.append(item)
    return items
        
def heavy_set(capacity, items_count):
    items = []
    while items_count > 0:
        items_count = items_count - 1
        item = random.randint(int (capacity*(0.5)), capacity) # Set the items list to be heavy
        items.append(item)
    return items

def very_heavy_set(capacity, items_count):
    items = []
    while items_count > 0:
        items_count = items_count - 1
        item = random.randint(int (capacity*(0.8)), capacity)  
        items.append(item)
    return items

def medium_set(capacity, items_count):
    items = []
    while items_count > 0:
        items_count = items_count - 1
        item = random.randint(int (capacity*(0.33)),int (capacity*(0.66))) # Set the items list to be medium
        #check if this is right numbers wise
        items.append(item)
    return items

def polar_set(capacity, items_count):
    items = []
    while items_count > 0:
        items_count = items_count - 1
        if random.randint(1,2) == 1:
            item = random.randint(1, int(capacity * 0.2))
            
        else: #50/50 chance for a big or small polar item
            item = random.randint(int(capacity*(0.8)), capacity) 
        items.append(item)
    return items
    
def save_raw_csv(results, filename): #include filename
    with open(filename, "w", newline="") as file:
        writer = csv.writer(file)

        # 第一行是表头
        writer.writerow(["capacity", "items_count", "distribution", "trial #", "bins_used", "run_time"])

        # 后面一行一行写结果
        for row in results:
            writer.writerow(row)
    
def save_summary_csv(summary_results, filename): #include filename
    
    with open(filename, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["n", "capacity", "tests", "average_bins_used", "average_running_time_seconds"])
    
        for row in summary_results:
            writer.writerow(row)
    #file.close()

def branch_and_bound(capacity, items):

    start = time.perf_counter()
    sorted_items = sorted(items, reverse=True)  #reverse the sort such that large items are first
     #either rewrite with my own sort or decide if sort is better than my sort

    nodes_visited = 0  
    
    bins = []
    items_total_weight = sum(items)
    upper_bound = len(items) #absolute worst case
    remainder = items_total_weight % capacity
    #final_bins = None
    #removing final_bins for performance since Don't need
    lower_bound = items_total_weight // capacity  #lower bound on the 
    if (remainder != 0):
        
        lower_bound = lower_bound + 1
    if (len(items) == 0):
        return 0,0  #no bins needed
    if (len(items) == 1):
         
        return 1,0 #not fractional so this will only need one bin
    most_efficient = upper_bound
     
      

    def bnb_search(item_index, bins):
        
        
        
          #for some reason an inner function made more sense than an outer one for the recursive thinking
          #on this but I don't really know why, might change later
        nonlocal most_efficient
        #upper bound does not change
          #i think this is correct because the items are sorted
        #nodes_visited = nodes_visited + 1
        if (item_index == len(items)):
            if (len(bins) < most_efficient):
                most_efficient = len(bins)
                #final_bins = []
                #for bin in bins:
                    #final_bins.append(list(bin.items))
            return #if second case not true than not good solution
          
         #Pruning method
        remaining_items = sorted_items[item_index:]  #all the items which haven't been placed yet
        remaining_items_weight = sum(remaining_items)
        remainder = remaining_items_weight % capacity # see if remaining weight will fit in the bins
          #lower bound will be set to num of bins opened + remain
        lower_bound = len(bins) + (remaining_items_weight // capacity)
        if (remainder != 0):
            
            lower_bound = lower_bound + 1
                
        if (lower_bound > most_efficient): # another bug fixed here, switched to >, pruning too early with >=
            return #not a good solution

          # Branc 1: we are going to try and fit an item into an existing bin  
        item = sorted_items[item_index]
        seen_weights = set()  #faster search in a set I think?  At least removes the
                                #duplicate values
        for bin in bins:
            if bin.does_item_fit(item):
                if (bin.remaining_space() in seen_weights) == True:
                        continue  #Back to the top of for loop
                seen_weights.add(bin.remaining_space())

                bin.add_item(item)
                bnb_search(item_index + 1, bins)  # go to the next item
                bin.remove_item(item)  # otherwise the bins will fill up as I found out lol
                    
          #This is the second branching operation in which
          #we will open a new bin
          
        if len(bins) + 1 <= most_efficient: # Third bug here I believe
            new_bin = Bin(capacity)
            new_bin.add_item(item)
            bins.append(new_bin)
            bnb_search(item_index + 1, bins)
            bins.pop() #Remove last bin from list
    #final_bins = []
   # final_bins = bnb_search(0,[]) #search starts at index of 0 and goes
                       #starts with empty list of bins
    bnb_search(0,[])
    end = time.perf_counter()
    #print(nodes_visited)
    return most_efficient, (end-start)
        # maybe later I will return the actual bin packing
        # for now I am not too worried about it



def branch_and_bound_ffd(capacity, items):
    #ffd called first, this should greatly decrease the number of nodes visited

    start = time.perf_counter()

    if (len(items) == 0):
        return 0,0  #no bins needed
    if (len(items) == 1):
        return 1,0 #not fractional so this will only need one bin

    sorted_items = sorted(items, reverse=True)  #reverse the sort such that large items are first
     #either rewrite with my own sort or decide if sort is better than my sort
   # nodes_visited = 0
    
    bins = []
    items_total_weight = sum(items)
    junk_ffd_packing =[] #bins from ffd, don't want to fill just get upper bound



    upper_bound, ffd_time = first_fit_decreasing(capacity, sorted_items)
    #upper_bound = len(items) #absolute worst case
    remainder = items_total_weight % capacity
    #final_bins = None
    lower_bound = items_total_weight // capacity  #lower bound on the 
    if (remainder != 0):
        
        lower_bound = lower_bound + 1
    most_efficient = upper_bound
     
      

    def bnb_search(item_index, bins):
        
        
        
          #for some reason an inner function made more sense than an outer one for the recursive thinking
          #on this but I don't really know why, might change later
        nonlocal most_efficient #final_bins, nodes_visited
    #    nodes_visited = nodes_visited + 1
        #upper bound does not change
          #i think this is correct because the items are sorted
    
        if (item_index == len(items)):
            if (len(bins) < most_efficient):
                most_efficient = len(bins)
                final_bins = []
                #for bin in bins:
                   # final_bins.append(list(bin.items))
            return #if second case not true than not good solution
          
         #dfffPruning method
        remaining_items = sorted_items[item_index:]  #all the items which haven't been placed yet
        remaining_items_weight = sum(remaining_items)
        remainder = remaining_items_weight % capacity # see if remaining weight will fit in the bins
          #lower bound will be set to num of bins opened + remain
        lower_bound = len(bins) + (remaining_items_weight // capacity)
        if (remainder != 0):
            
            lower_bound = lower_bound + 1
                
        if (lower_bound > most_efficient): # another bug fixed here, switched to >, pruning too early with >=
            return #not a good solution

          # Branc 1: we are going to try and fit an item into an existing bin  
        item = sorted_items[item_index]
        seen_weights = set()  #faster search in a set I think?  At least removes the
                                #duplicate values
        for bin in bins:
            if bin.does_item_fit(item):
                if (bin.remaining_space() in seen_weights) == True:
                        continue  #Back to the top of for loop
                seen_weights.add(bin.remaining_space())

                bin.add_item(item)
                bnb_search(item_index + 1, bins)  # go to the next item
                bin.remove_item(item)  # otherwise the bins will fill up as I found out lol
                    
          #This is the second branching operation in which
          #we will open a new bin
          
        if len(bins) + 1 <= most_efficient: # Third bug here I believe
            new_bin = Bin(capacity)
            new_bin.add_item(item)
            bins.append(new_bin)
            bnb_search(item_index + 1, bins)
            bins.pop() #Remove last bin from list
    #final_bins = []
   # final_bins = bnb_search(0,[]) #search starts at index of 0 and goes
                       #starts with empty list of bins
    bnb_search(0,[])
    end = time.perf_counter()
    #print(nodes_visited)

    return most_efficient, (end-start)
    
   # return most_efficient, final_bins,
        # maybe later I will return the actual bin packing
        # for now I am not too worried about it

# FFD 算法
def first_fit_decreasing(capacity, items):
    # items 从大到小排序
    start = time.perf_counter()
    
    sorted_items = sorted(items, reverse=True)

    # 用来装每个箱子里有哪些物品
    bins = []

    # 用来记录每个箱子现在总重量是多少
    bin_totals = []

    # 一个一个处理排好序的 item
    for item in sorted_items:
        
        put_in_bin = False   # 先假设这个 item 还没有放进去

        # 看看能不能放进已经存在的某个 bin
        for j in range(len(bins)):
            # 如果这个箱子当前总重量 + item <= capacity，就说明放得下
            if bin_totals[j] + item <= capacity:
                bins[j].append(item)          # 把 item 放进这个箱子
                bin_totals[j] = bin_totals[j] + item   # 更新这个箱子的总重量
                put_in_bin = True
                break   # First fit：找到第一个能放的就停

        # 如果前面的旧箱子都放不下，就新开一个箱子
        if put_in_bin == False:
            bins.append([item])   # 新箱子里先放这个 item
            bin_totals.append(item)
    end = time.perf_counter()
   # time = end-start  # Not sure on the output of this
    return len(bins), (end-start)

def test_runner_ffd():
    capacities = [10,100]
    item_counts = [10, 100]
    num_trials = 10

    generators = {  # this makes it immensely easier than what I was trying to do before
                    # never have used this technique before
        "rand": rand_distributed_set,
        "heavy": heavy_set,
        "very_heavy": very_heavy_set,
        "medium": medium_set,
        "light": light_set,
        "very_light": very_light_set,
        "polar": polar_set,
        }

    results = []

    for capacity in capacities:
        for items_count in item_counts:
            for dist_name, generator_func in generators.items():
                for trial in range(num_trials):
                    items = generator_func(capacity, items_count)
                    bins_used, run_time = first_fit_decreasing(capacity, items)
                    results.append([capacity, items_count, dist_name, trial, bins_used, run_time])
    return results
def test_runner_bnb_ffd():
    capacities = [10,100]
    item_counts = [10, 100]
    num_trials = 100

    generators = {  # this makes it immensely easier
                    # than what I was trying to do before
                           
        "rand": rand_distributed_set,
        "heavy": heavy_set,
        "very_heavy": very_heavy_set,
        "medium": medium_set,
        "light": light_set,
        "very_light": very_light_set,
        "polar": polar_set,
        }

    results = []

    for capacity in capacities:
        for items_count in item_counts:
            for dist_name, generator_func in generators.items():
                for trial in range(num_trials):
                    items = generator_func(capacity, items_count)
                    bins_used, run_time = branch_and_bound_ffd(capacity, items)
                    results.append([capacity, items_count, dist_name, trial, bins_used, run_time])
    return results
            
def test_runner_bnb_simple():
    capacities = [10,100]
    item_counts = [10, 100]
    num_trials = 100

    generators = {
        "rand": rand_distributed_set,
        "heavy": heavy_set,
        "very_heavy": very_heavy_set,
        "medium": medium_set,
        "light": light_set,
        "very_light": very_light_set,
        "polar": polar_set,
        }

    results = []

    for capacity in capacities:
        for items_count in item_counts:
            for dist_name, generator_func in generators.items():
                for trial in range(num_trials):
                    items = generator_func(capacity, items_count)
                    bins_used, run_time = branch_and_bound(capacity, items)
                    results.append([capacity, items_count, dist_name, trial, bins_used, run_time])
    return results



def summarizer(results):
    summary = []
    configs = set((row[0], row[1], row[2]) for row in results)

    for (capacity, items_count, dist_name) in configs:

        matching = [row for row in results if row[0] == capacity and row[1] == items_count and row[2] == dist_name]
        
        avg_bins = sum(row[4] for row in matching) / len(matching)
        avg_time = sum(row[5] for row in matching) / len(matching)

        summary.append([capacity,items_count,dist_name,len(matching),avg_bins,avg_time])
    return summary
def run_from1(algorithm):
    #added this because find_15_minutes doesn't work as hoped
    #finds the number of bins and the max number of items(starting at 1 item)
    #which can be packed in 15 minutes, number of items, increases by 1 everytime
    #perhaps this test along with find_15_minutes can tell something about complexity
    items = []
    results = []
    time_elapsed = 0
    capacity = 10
    items_count = 1
    total_bins_packed = 0
    total_items_packed = 1
    algotime = 0
    algo_time_growth = []
    while (time_elapsed < 900):
        items = rand_distributed_set(capacity, items_count)
        
        time_elapsed = time_elapsed + algotime
        bins_packed, algotime = algorithm(capacity, items)
        total_items_packed = total_items_packed + items_count
        total_bins_packed = total_bins_packed + bins_packed
        algo_time_growth.append(algotime)
        items_count +=1
    
    return total_bins_packed, items_count, total_items_packed, algo_time_growth
def find_15_minutes(algorithm):
    #finds the largest number of items which can be handled in 15 minutes
    time = 0
    longest_time = 0
    items = []
    capacity = 10
    items_count = 10 #start with 10 items to make this take a bit less time
    
    while longest_time < 900: #900/60 = 15
        #testing only on rand_dist set
        items = rand_distributed_set(capacity, items_count)
        bins_packed, time = algorithm(capacity, items)
        if (time > longest_time):
            longest_time = time
        items_count = items_count+1
        
    return bins_packed, items_count, time
def write_csv_15mins(results, filename):
    total_bins_packed, items_count, total_items_packed, algo_time_growth = results
    with open(filename, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["item_count", "algo_time"])
        for i, t in enumerate(algo_time_growth):
            writer.writerow([i + 1, t])

def main():
    print("Welcome to the bin-packing test suite: ")
    print("1: FFD")
    print("2: Branch-and-Bound")
    print("3: Branch-and-Bound-FFD-upper-bound")
    print("4: Pack for 15 minutes")
    print("15: Find 15 minutes for all")
    user_in = input("Enter choice of test(1-3,15): ")
    
    if (user_in == "1"):
        results = test_runner_ffd()
        save_raw_csv(results, "ffd_results.csv")
        save_summary_csv(summarizer(results), "ffd_summary.csv")
    elif (user_in == "2"):
        results = test_runner_bnb_simple()
        save_raw_csv(results, "bnb_simple_results.csv")
        save_summary_csv(summarizer(results), "bnb_simple_summary.csv")
    elif (user_in == "3"):
        results = test_runner_bnb_ffd()
        save_raw_csv(results, "bnb_ffd_csv_results.csv")
        save_summary_csv(summarizer(results), "bnb_ffd_summary.csv")
    elif (user_in == "4"):
        results = run_from1(branch_and_bound)
        print("BNB:")
        write_csv_15mins(results,"bnb_15_minute_run.csv")
        print(results)
        results = run_from1(branch_and_bound_ffd)
        print("BNBFFD:")
        write_csv_15mins(results,"bnbffd_15_minute_run.csv")
        print(results)
        results = run_from1(first_fit_decreasing)
        print("FFD:")
        write_csv_15mins(results,"ffd_15_minute_run.csv")
        print(results)
    elif (user_in == "15"):
        results = find_15_minutes(branch_and_bound)
        print("BNB:")
        print(results)
        results = find_15_minutes(branch_and_bound_ffd)
        print("BNBFFD:")
        print(results)
        results = find_15_minutes(first_fit_decreasing)
        print("FFD:")
        print(results)
    #more later for personal fortran function testing

if __name__ == "__main__":
    main()
'''
some suspicions that I have right now.  The heavy and very heavy sets will have some effect on the time
Try different capacities and different items counts
larger capacities etc
'''
