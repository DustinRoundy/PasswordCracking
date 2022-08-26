import time
import sys
from data import map
rank = 0
cluster_size = 26

start_number = rank
end_number = 0

password = sys.argv[1]

start = time.time()

attempts = 0
# Set current password attempt to an empty array with the same length as password
current_attempt = []
for length in range(len(password)):
    current_attempt.append(0)


# for password_attempt in range(start, password.len(), cluster_size * 2):

f = open('report.txt', 'w')
f.write("Cluster size: " + str(cluster_size) +'\n')
f.write("Start: " + str(start_number) + '\n')
cluster_data = []
for password_attempt in range(start_number, len(map), cluster_size):
    cluster_data.append(password_attempt)
print(cluster_data)
# password_found = False
# while password_found != True:
#     for i in range(len(current_attempt)):
#         print(cluster_data[i])
for item in range(len(cluster_data)):
    # print(item)
    current_attempt[0] = map[cluster_data[item]]
    for length in range(len(password) - 1):
        if length != 0:
            print(length, "is not zero")
            for length2 in range(len(password) - 1):
                for i in range(len(map)):
                    current_attempt[length + 1] = map[i]
                    for i in range(len(map)):
                        current_attempt[length2 + 1] = map[i]
                        f.write(str(current_attempt) + '\n')
                    # print(current_attempt)
            # for len2 in range(0, length):
            #     print('test', len2)
            #     for i in range(len(map)):
            #         current_attempt[length + 1] = map[i]
            # print("Test")
        else:
            for i in range(len(map)):
                current_attempt[length + 1] = map[i]
                f.write(str(current_attempt) + '\n')


        
