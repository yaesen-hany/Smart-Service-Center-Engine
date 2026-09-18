from tabulate import tabulate
import json
CURRENT_ID=1
class Stack:
    def __init__(self):
        self.stack=[]
    def is_empty(self):
        return len(self.stack) == 0
    def push(self,stack):
        self.stack.append(stack)
    def pop(self):
        if self.is_empty():
            return None
        return self.stack.pop()
    def peek(self):
        if self.is_empty():
            return None
        return self.stack[-1]
class Queue:
    def __init__(self):
        self.queue = []
    def is_empty(self):
        return len(self.queue) == 0
    def enqueue(self, item):
        self.queue.append(item)
    def dequeue(self):
        if self.is_empty():
            return None
        return self.queue.pop(0)
    def front(self):
        if self.is_empty():
            return None
        return self.queue[0]
class HashTable:
    def __init__(self,size=10):
        self.size=size
        self.table = [[] for _ in range(size)]
    def hash(self,key):
        return key % self.size
    def get(self,key):
        bucket= self.table[self.hash(key)]
        for k, v in bucket:
             if k == key:
                 return v
        return None
    def put (self,key,value):
        bucket=self.table[self.hash(key)]
        for i in range(len(bucket)):
            if bucket[i][0] == key:
               bucket[i] = (key, value)
               return
        bucket.append((key,value))
def load_json (queue, hash_table, filename="requests.json"):
    global CURRENT_ID
    try:
        with open(filename, "r") as f:
            requests = json.load(f)   
        max_id = 0
        for req in requests:
            hash_table.put(req["id"], req)
            if req["id"] > max_id:
                max_id = req["id"]
        sorted_requests, _, _, _ = sort_requset(requests, hash_table, type_sort="insert_sort", key="id")
        for req in sorted_requests:
            queue.enqueue(req)
        CURRENT_ID = max_id + 1
        return True
    except FileNotFoundError:
        return False
def save_to_json(queue, filename="requests.json"):
    try:
        with open(filename, "w") as f:
            json.dump(queue.queue, f, indent=4)
        return True
    except Exception:
        return False
def bubble_sort(s):
    count=0
    swap=0
    for i in range(len(s)):
        for j in range(len(s)-1-i):
            count+=1

            if s[j]>s[j+1]:
                
                swap+=1
                s[j],s[j+1]=s[j+1],s[j] 
    return s,count,swap
def select_sort(s):
    count=0
    swap=0
    for i in range(len(s)):
         small=i
         for j in range(i+1,len(s)):
            count+=1
            if s[j]<s[small]:
                small=j
                if small!=i:
                    s[i],s[small]=s[small],s[i]
                    swap+=1
    return s,count,swap
def insert_sort(s):
    count=0
    swap=0
    for i in range(1,len(s)):
        
        small=s[i]
        j=i-1
        while j>=0 :
            count+=1
            if small<s[j]:
                swap+=1
                s[j+1]=s[j]
                j-=1
            else:
                break
        s[j+1]=small
    return s,count,swap
def sort_requset(requset,hash_table,type_sort,key="priority"):
    s = []
    for req in requset:
          s.append([req[key], req["id"]])
    if type_sort=="bubble_sort":
        sorted_requset, count, swaps = bubble_sort(s)
    elif type_sort=="select_sort":
        sorted_requset, count, swaps = select_sort(s)
    elif type_sort=="insert_sort":
         sorted_requset, count, swaps = insert_sort(s)
    sorted_data = []
    for item in sorted_requset:
         req_id = item[1]
         sorted_data.append(hash_table.get(req_id))
    return sorted_data, count, swaps ,key
def search_requests(
    requests, hash_table, target, search_type="sequential_search"):
    id_req = [req["id"] for req in requests]
    if search_type == "sequential_search":
        position, count = sequential_search(id_req, target)
        if position != -1:
            found_req = hash_table.get(target)
            return True, position, count, found_req
        return False, position, count, None
    elif search_type == "binary_search":
        postion,count=binary_search(id_req,target)
        if postion < len(id_req) and id_req[postion]==target:
            found_req = hash_table.get(target)
            return True,postion,count,found_req
        else:
            return False,postion,count,None
def sequential_search(data, target):
  count = 0
  for i in range(len(data)):
    count += 1
    if data[i] == target:
        return i,count    
  return -1,count
def binary_search(data,target):
    left=0
    right=len(data)-1
    count=0
    while left<=right:
        mid=(left+right)//2
        count+=1
        if data[mid]==target:
            return mid,count
            
        elif data[mid]<target:
            left=mid+1
        else:
            right=mid-1
    return left,count #just with sort list
def add_requset(queue,hash_table):
    global CURRENT_ID
    try:
        name=input("Enter name: ")
        prio=int(input("Enter priority(1:5): "))
        priority=(prio) if prio in list(range(1,6)) else 5
        time=input("Enter Estimated Service Time(option): ")
        est_time=int(time) if time.strip() else 15
        
        id=CURRENT_ID
        CURRENT_ID+=1
        requset={
            "id":id,
            "name":name,
            "priority":priority,
            "est_time":est_time,
            "status":"Pending"
            }
        queue.enqueue(requset)
        hash_table.put(id, requset)
        return True
    except ValueError:
           return False
def process_request(queue,processed,hash_table):
    request=queue.dequeue()
    if request is None:
        return False
    request["status"] = "Processed"
    processed.append(request)
    hash_table.put(request["id"], request)
    return request
def display_queue(queue):
    if queue.is_empty():
        return print("Queue is empty.")
    table = [
        [
            req["id"],
            req["name"],
            req["priority"],
            req["est_time"],
            req["status"],
        ]
        for req in queue.queue
    ]
    header=["ID", "Name", "Priority", "Est Time", "Status"]
    print(tabulate(table, headers=header, tablefmt="rounded_grid"))
def display_processed(processed):
  if not processed:
    print("No processed requests yet.")
    return
  table = [
      [req["id"], req["name"], req["priority"], req["est_time"], req["status"]]
      for req in processed
  ]
  header = ["ID", "Name", "Priority", "Est Time", "Status"]
  print(tabulate(table, headers=header, tablefmt="rounded_grid"))
def add_search_history(stack, target_id, method, found, postion, count):
  record = {
      "target_id": target_id,
      "method": method,
      "result": "Found" if found else "Not Found",
      "position": postion,
      "comparisons": count,
  }
  stack.push(record)
def show_algorithm_statistics(queue, hash_table,key="priority"):
  if queue.is_empty():
    print("No data available to generate statistics.")
    return

  print("\n--- Sorting Algorithms Benchmark on Current Data ---")
  results = []
  for algo in ["bubble_sort", "select_sort", "insert_sort"]:
    _, count, swaps, _ = sort_requset(queue.queue.copy(), hash_table, algo, key)
    results.append([algo.replace("_", " ").title(), count, swaps])

  print( tabulate(results,headers=["Algorithm", "Comparisons", "Swaps / Shifts"],tablefmt="rounded_grid"))
def view_last_search(stack):
  if stack.is_empty():
    print("No search history available.")
    return None
  last = stack.peek()
  print("--- Last Search Record ---")
  print(f"Target ID: {last['target_id']}")
  print(f"Method: {last['method']}")
  print(f"Result: {last['result']}")
  print(f"Position: {last['position']}")
  print(f"Comparisons: {last['comparisons']}")
  return last
def pop_last_search(stack):
  if stack.is_empty():
    print("History is already empty.")
    return None
  removed = stack.pop()
  print(
      f"Removed search record for ID {removed['target_id']} from history."
  )
  return removed
def print_menu():
  print("\n" + "=" * 45)
  print("      REQUEST MANAGEMENT SYSTEM      ")
  print("=" * 45)
  print("1.  Add New Request")
  print("2.  Process Next Request")
  print("3.  View Next Request in Queue ")
  print("4.  Display Pending Queue")
  print("5.  Lookup Request via HashTable")
  print("6.  Sort Requests")
  print("7.  Search Request (Sequential) in process requests")
  print("8.  Search Request (Binary) in queue")
  print("9.  View Most Recent Search ")
  print("10. Undo/Remove Last Search ")
  print("11. Show algorithm statistics")
  print("12. Show Processed Requests")
  print("13. Exit")
  print("=" * 45)
def main():
    q = Queue()
    st = Stack()
    ht = HashTable()
    load_json(q,ht)
    processed=[]
    while True:
        print_menu()
        choise=input("Enter your choice: ")
        if choise=="1":
            if add_requset(q,ht):
                print("Request added successfully.")
                save_to_json(q)
            else:
                print("Failed to add request. Please check your input.")#add requset
        elif choise=="2":
            request = process_request(q, processed, ht)
            if request:
                print(f"Processed Request ID: {request['id']}")
                save_to_json(q)
            else:
                print("No requests to process.")#Process Next Request
        elif choise=="3":
            next_request = q.front()
            if next_request:
                print(f"Next Request ID: {next_request['id']}, Name: {next_request['name']}")
            else:
                print("No requests in the queue.")#View Next Request in Queue
        elif choise=="4":
            display_queue(q)#Display Pending Queue
        elif choise=="5":
            try:
                target_id = int(input("Enter Request ID to lookup: "))
                found_request = ht.get(target_id)
                found = found_request is not None
                add_search_history(st, target_id, "HashTable", found, postion="N/A", count=1)
                if found_request:
                    print(f"Found Request: {found_request}")
                else:
                    print("Request not found in HashTable.")
            except ValueError:
                print("Invalid ID. Please enter a numeric value.")#Lookup Request via HashTable
        elif choise=="6":
            if q.is_empty():
                print("Queue is empty, no requests to sort.")
                continue
            sort_type = input("Enter sorting method (bubble_sort/select_sort/insert_sort): ")
            key = input("Enter key to sort by (priority/est_time): ")
            sorted_requests, count, swaps, sort_key = sort_requset(q.queue.copy(), ht, sort_type, key)
            print(f"Sorted by {sort_key} using {sort_type}. Comparisons: {count}, Swaps: {swaps}")
            table = [ [req["id"], req["name"], req["priority"], req["est_time"], req["status"]]for req in sorted_requests]
            header = ["ID", "Name", "Priority", "Est Time", "Status"]
            print(tabulate(table, headers=header, tablefmt="rounded_grid"))#Sort Requests
        elif choise=="7":
            if not processed:
                 print("No processed requests available to search.")
                 continue
            try:
                target_id = int(input("Enter Request ID to search (Sequential): "))
                found, position, count, found_request = search_requests(processed, ht, target_id, "sequential_search")
                add_search_history(st, target_id, "Sequential", found, position, count)
                if found:
                    print(f"Result: Found at index {position} | Comparisons: {count} | Method: Sequential Search")
                    print(f"Request Details: {found_request}")
                else:
                    print(f"Result: Not Found | Comparisons: {count} | Method: Sequential Search")
            except ValueError:
                print("Invalid ID. Please enter a numeric value.")#Search Request (Sequential)
        elif choise=="8":
            if q.is_empty():
                print("Queue is empty.")
                continue
            try:
                target_id= int(input("Enter Request ID to search (binary): "))
                found, position, count, found_request = search_requests(q.queue, ht, target_id, "binary_search")
                add_search_history(st, target_id, "binary", found, position, count)
                if found:
                   print(f"Result: Found at index {position} | Comparisons: {count} | Method: Binary Search")
                   print(f"Request Details: {found_request}")
                else:
                    print(f"Result: Not Found (Suggested insert position: index {position}) | Comparisons: {count} | Method: Binary Search")
            except ValueError:
                print("Invalid ID. Please enter a numeric value.")#Search Request (Binary)
        elif choise=="9":
            view_last_search(st)#View Most Recent Search
        elif choise=="10":
            pop_last_search(st)#Undo/Remove Last Search
        elif choise=="11":
            key = input("Enter key to sort by (priority/est_time): ").strip()
            if key not in ["priority", "est_time", "id"]:
               key = "priority"
            show_algorithm_statistics(q,ht,key)# Show algorithm statistics
        elif choise=="12":
            display_processed(processed)#Show Processed Requests
        elif choise=="13":
            print("Goodbye!")
            save_to_json(q)
            break#exist
        else:
            print("Invalid option, please choose from 1 to 13.")


    
if __name__ == "__main__":
  main()