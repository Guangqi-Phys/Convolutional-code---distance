#!/usr/bin/python3

import networkx as nx
import matplotlib.pyplot as plt

memory = 9;
n_memory = 2**memory;
list1 = [];
list2 = [];
g_list = [];
g_bin_list = [];
data_file = 'data/data_k=' + str(memory) + '_no.dat';



for i in range(2,n_memory):
	list1.append(i);

for i in range(1,memory):
	list2.append(2**i);

g_list = list(set(list1) - set(list2));

for i in range(len(g_list)):
	g_bin_list.append((bin(g_list[i]).replace('0b','')).zfill(memory));

DG = nx.DiGraph();

v_list = []
for i in range(n_memory):
	v_list.append(i);

v_bin_list = [];
for i in range(len(v_list)):
	v_bin_list.append((bin(v_list[i]).replace('0b','')).zfill(memory-1));


v_slice0 = [];
v_slice1 = [];
for i in range(len(v_bin_list)):
	v_slice0.append(v_bin_list[i] + '0');
	v_slice1.append(v_bin_list[i] + '1');

nn = 0;
f = open(data_file, "w");
max_distance = 0;
for ind in range(len(g_bin_list)-100, len(g_bin_list)):
	for jnd in range(ind+1,int(len(g_bin_list))):
		distance = 0;
		for j in range(len(v_slice0)):
			path1 = 0;
			path2 = 0;
			for i in range(len(g_bin_list[0])):
				path1 += int(v_slice0[j][i])*int(g_bin_list[ind][i]);
				path2 += int(v_slice0[j][i])*int(g_bin_list[jnd][i]);
			path1 = path1 % 2;
			path2 = path2 % 2;
			weight = path1 + path2;
			DG.add_weighted_edges_from([(v_bin_list[j], v_slice0[j][1:], weight)]);

		for j in range(len(v_slice1)):
			path1 = 0;
			path2 = 0;
			for i in range(len(g_bin_list[0])):
				path1 += int(v_slice1[j][i])*int(g_bin_list[ind][i]);
				path2 += int(v_slice1[j][i])*int(g_bin_list[jnd][i]);
			path1 = path1 % 2;
			path2 = path2 % 2;
			weight = path1 + path2;
			DG.add_weighted_edges_from([(v_bin_list[j], v_slice1[j][1:], weight)]);
        
		start_point = '';
		end_point = '';
		for iind in range(memory-1):
			start_point += '0';
			end_point += '0';
		start_point = start_point[1:] + '1';

		first_point = '';
		for iind in range(memory):
			first_point += '0';
		first_point = first_point[1:] + '1';

		path1 = 0;
		path2 = 0;
		for i in range(len(g_bin_list[0])):
			path1 += int(first_point[i])*int(g_bin_list[ind][i]);
			path2 += int(first_point[i])*int(g_bin_list[jnd][i]);
		weight1 = (path1 % 2) + (path2 % 2);

		distance = weight1 + nx.shortest_path_length(DG, source=start_point, target = end_point, weight='weight');

		if distance > max_distance:
			max_distance = distance;

		nn += 1;

		# f.write("Constraint length (K): {}. Generator polynomials: {}, {}. Distance: {}  ".format(memory, g_bin_list[ind],g_bin_list[jnd], distance));
		f.write("{} {}".format(nn, distance));
		f.write('\n');
# f.write("Maximum distance is: {}".format(max_distance))
f.close()









