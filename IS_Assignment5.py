from Request import Request
from Server import Server
from Queue import Queue
import sys
import argparse

def main() :
    parser = argparse.ArgumentParser(description='Optional app description')
    # Required positional argument
    parser.add_argument('-file', type=str, required=True ,  help='path to the input csv file name')
    parser.add_argument('-server', type=int, default=0, help='number of servers to use')

    args = parser.parse_args()
    if args.file is None :
        print ('Please provide the path and name of the input csv file , -- help for more info')
        sys.exit()

    if args.server is None :
        print ('Please provide the path and name of the output file to use , -- help for more info')


    in_file = args.file
    num_server = args.server
    if num_server >1 :
        simulateManyServer(15,5,in_file,num_server)
    else:
        simulateOneServer(24, 5,in_file)

def simulateOneServer(num_seconds, file_per_minute,in_file):
    server = Server(file_per_minute)
    print_queue = Queue()
    waiting_times = []

    with open(in_file) as lines:
        for line in lines:
            data = line.split(',')
            request = Request(int(data[0].strip()), data[1],int(data[2].strip()))
            print_queue.enqueue(request)
            #print(str(request.wait_time()))
    #print (data)
    for current_second in range(num_seconds):

        if (not server.busy()) and (not print_queue.is_empty()):
            next_task = print_queue.dequeue()
            waiting_times.append(next_task.wait_time())
            server.start_next(next_task)

        server.tick()
    average_wait = sum(waiting_times) / len(waiting_times)
    print("Average Wait %6.2f secs %3d tasks remaining." %(average_wait, print_queue.size()))

def simulateManyServer(num_secs, file_per_min,in_file,num_servers):
    request_list = [Server(file_per_min) for i in range(num_servers)]
    print_queue = Queue()
    waiting_times = []

    with open(in_file) as lines:
        for line in lines:
            data = line.split(',')
            request = Request(int(data[0].strip()), data[1],int(data[2].strip()))
            print_queue.enqueue(request)

    current_server = 0
    for current_second in range(num_secs):

        if (not request_list[current_server].busy()) and (not print_queue.is_empty()):
            next_task = print_queue.dequeue()
            waiting_times.append(next_task.wait_time())
            request_list[current_server].start_next(next_task)
            current_server = (current_server + 1) % len(request_list)

        for server in request_list :
            if server.busy :
                server.tick()
    average_wait = sum(waiting_times) / len(waiting_times)
    print("Average Wait %6.2f secs %3d tasks remaining." %(average_wait, print_queue.size()))


if __name__ == "__main__": main()

