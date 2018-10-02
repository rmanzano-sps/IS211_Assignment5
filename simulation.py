import csv
import urllib2

class Server:

    def __init__(self, ppm):
        self.page_rate = ppm
        self.current_task = None
        self.time_remaining = 0

    def tick(self):
        if self.current_task != None:
            self.time_remaining = self.time_remaining - 1
        if self.time_remaining <= 0:
            self.current_task = None

    def busy(self):
        if self.current_task != None:
            return True
        else:
            return False

    def start_next(self,new_task):
        self.current_task = new_task
        self.time_remaining = new_task.get_pages() * 60/self.page_rate


class Request:

    def __init__(self, timestamp, pages):
        self.timestamp = timestamp
        self.pages = pages

    def get_stamp(self):
        return self.timestamp

    def get_pages(self):
        return self.pages

    def wait_time(self, current_time):
        return current_time - self.timestamp



class Queue:

   def __init__(self):
      self.items = []

   def is_empty(self):
      return self.items == []

   def enqueue(self, item):
      self.items.insert(0,item)

   def dequeue(self):
      return self.items.pop()

   def size(self):
      return len(self.items)




def simulateOneServer(data):

    for row in data:
        seconds_of_simulation = int(row[0])
        file_name = row[1]
        seconds_to_process = int(row[2])
        print_queue = Queue()
        lab_printer = Server(seconds_to_process)
        waiting_times = []
        task = Request(timestamp=seconds_of_simulation, pages=seconds_to_process)
        print_queue.enqueue(task)

        if (not lab_printer.busy()) and (not print_queue.is_empty()):
            next_task = print_queue.dequeue()
            waiting_times.append(next_task.wait_time(seconds_of_simulation))
            lab_printer.start_next(next_task)
            lab_printer.tick()

        average_wait = sum(waiting_times) / len(waiting_times)
        print("Average Wait %6.2f secs %3d tasks remaining."% (average_wait, print_queue.size()))


# def simulateManyServers(name_list, num):
#     sim_queue = Queue()
#
#     for name in name_list:
#         sim_queue.enqueue(name)
#         while sim_queue.size() > 1:
#             for i in range(num):
#                 sim_queue.enqueue(sim_queue.dequeue())
#             sim_queue.dequeue()
#
#         return sim_queue.dequeue()
#     print(hot_potato(["Bill", "David", "Susan", "Jane", "Kent","Brad"], 7))

def main():
    url = 'http://s3.amazonaws.com/cuny-is211-spring2015/requests.csv'
    response = urllib2.urlopen(url)
    data = csv.reader(response)
    simulateOneServer(data)
    # simulateManyServers(data, servers)


if __name__ == "__main__":
    main()


# 7, /images/test.gif, 1
#  7th second of the simulation, filename, 1 second to process
