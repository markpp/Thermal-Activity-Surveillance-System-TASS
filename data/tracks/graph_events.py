import glob
import os
import argparse
import numpy as np
from numpy import genfromtxt, savetxt
import csv
import cv2
import warnings
# https://networkx.readthedocs.io/en/stable/examples/
import networkx as nx
import matplotlib.pyplot as plt

TIME_DIFFERENCE_THRESHOLD = 5

def find_preceeding_nodes(graph, leave_node):
    # Extract leave node and every predecessor
    sub_nodes = []
    sub_nodes.append(leave_node)
    while graph.predecessors(leave_node):
        #print G.predecessors(n)[0]
        sub_nodes.append(graph.predecessors(leave_node)[0])
        leave_node = leave_node-1

    # return the relevant nodes
    return sub_nodes

def populate_graph(dets_list):
    # Populate graph with detections
    G = nx.DiGraph(name='my graph')

    det_types = ['b', 'r']
    node_pos = {}
    node_color = []
    # Set to values appropriate for first node
    match = False
    match_idx = 0
    for idx, det in enumerate(dets_list):
        det_frame_nr, det_type, det_prob, _, det_x, det_y = det[0].split(";")

        # check for match between detection and nodes in graph
        if len(G.node) > 0:
            # find best match(insert hungarian algorithm)
            abs_diff_list = []
            for n_idx in range(0, len(G.node)):
                abs_diff_list.append(abs(G.node[n_idx]['time'] - int(det_frame_nr)))
            np_list = np.array(abs_diff_list)
            best_idx = np.argmin(np_list)

            # match if time difference is small
            if np_list[best_idx] < TIME_DIFFERENCE_THRESHOLD:
                match = True
                match_idx = n_idx
            else:
                match = False

        #color = ""
        #if det_type == 'b':
        #    color = "b"

        #elif det_type == 'p':
        #    color = "p"
        # If match node with edge to match
        if match:
            G.add_node(idx, time=int(det_frame_nr), pos_x=det_x, score=det_prob, node_type=det_type)
            G.add_edge(match_idx, idx)

        # if first or no match add new node to graph
        else:
            G.add_node(idx, time=int(det_frame_nr), pos_x=det_x, score=det_prob, node_type=det_type)

        node_pos[idx] = [int(det_frame_nr), int(det_x)]
        #node_color.append(det_type)


    # Finding root nodes in graph
    root_nodes = [x for x in G.nodes_iter() if G.out_degree(x) == 1 and G.in_degree(x) == 0]
    print("roots {}".format(root_nodes))

    # Finding leave nodes in graph
    leave_nodes = [x for x in G.nodes_iter() if G.out_degree(x) == 0 and G.in_degree(x) == 1]
    print("Leaves {}".format(leave_nodes))
    #print("Leaves {}".format([n for n, d in G.out_degree().items() if d == 0]))

    #print("INFO")
    #print nx.info(G, n=None)
    #print("degree histogram: {}".format(nx.degree_histogram(G)))

    return G, node_pos, root_nodes, leave_nodes

def plot_graph(G, node_pos, root_nodes, leave_nodes):
    plt.figure(1, figsize=(18, 6))

    #print(node_pos)
    #print(node_color)
    #nx.draw_networkx(G, pos=node_pos, arrows=True, with_labels=True, node_size=200, node_color=node_color, font_size=8)

    #Get all distinct node classes according to the node shape attribute
    #node_shapes = set((shape[1]["s"] for shape in G.nodes(data = True)))

    bike_nodes = [sNode[0] for sNode in filter(lambda x: x[1]["node_type"] == 'b', G.nodes(data=True))]
    ped_nodes = [sNode[0] for sNode in filter(lambda x: x[1]["node_type"] == 'p', G.nodes(data=True))]

    nx.draw_networkx_nodes(G, node_pos, node_shape="v", nodelist=set(root_nodes) & set(bike_nodes), with_labels=True, node_size=200, node_color='b')
    nx.draw_networkx_nodes(G, node_pos, node_shape="^", nodelist=set(leave_nodes) & set(bike_nodes), with_labels=True, node_size=200, node_color='b')

    nx.draw_networkx_nodes(G, node_pos, node_shape="^", nodelist=set(leave_nodes) & set(ped_nodes), with_labels=True, node_size=200, node_color='r')
    nx.draw_networkx_nodes(G, node_pos, node_shape="v", nodelist=set(root_nodes) & set(ped_nodes), with_labels=True, node_size=200, node_color='r')


    #For each node class...
    #for det_type in det_types:

        #...filter and draw the subset of nodes with the same symbol in the positions that are now known through the use of the layout.

        #nx.draw_networkx_nodes(G, node_pos, node_shape=det_type, nodelist=[sNode[0] for sNode in filter(lambda x: x[1]["node_color"] == det_type, G.nodes(data=True))])

    #Finally, draw the edges between the nodes
    nx.draw_networkx_edges(G, node_pos, arrows=False)

    plt.xlabel('Frame number')
    plt.ylabel('Position in image(y-axis)')
    plt.savefig("simple_path.png") # save as png
    plt.show() # display


def frame_nr_to_time(track_list):

    for track in track_list[:4]:
        # Convert time
        frame_nr = int(track[0].split(';')[0])
        time_ms = int(frame_nr/0.009) # convert to ms using fps, should be 7 but louise set it to 9

        real_time = time_ms + (11*60*60*1000)
        print(time_ms)
        s, ms = divmod(real_time, 1000)
        m, s = divmod(real_time, 60)
        h, m = divmod(m, 60)
        print "%d:%02d:%02d.%02d" % (h, m, s, ms)
        #end_time_mtb = int(time_m_sec + float(int(data_frames_mtb.iloc[-1]['Frame']) / 9)))

        #sort based on type

def split_tracks(tracks):
    ped_list = []
    mtb_list = []
    track_list = []
    for track in tracks[:]:
        # Convert time
        frame_nr = int(track[0].split(';')[0])
        if(track[0].split(';')[1] is 'P'):
            ped_list.append(frame_nr)
        elif(track[0].split(';')[1] is 'B'):
            mtb_list.append(frame_nr)

        track_list.append(frame_nr)

    return track_list, mtb_list, ped_list

def time_to_frame_nr(time):
    fps = 30
    #if(time[3]>0):
    #    ms_frames = 1000/time[3]
    #else:
    #    ms_frames = 0
    s_frames = time[2]*fps
    m_frames = time[1]*60*fps
    h_frames = (time[0]-11)*360*fps

    #ms_frames
    return s_frames + m_frames + h_frames

def split_time_stamp(time_stamp):
    h = int(time_stamp.split(':')[0])
    m = int(time_stamp.split(':')[1])
    s = int(time_stamp.split(':')[2].split('.')[0])
    ms = int(time_stamp.split(':')[2].split('.')[1])
    return [h, m, s, ms]

def convert_events(events):
    event_list = []
    mtb_events = []
    ped_events = []

    for line in events[1:]:
        # Split line
        mtb = line[0].split(';')[0]
        ped = line[0].split(';')[1]
        if(mtb):
            #print("mtb: {}".format(mtb))
            frame_nr = time_to_frame_nr(split_time_stamp(mtb))
            event_list.append([frame_nr, 'B'])
            mtb_events.append(frame_nr)

        if(ped):
            #print("ped: {}".format(ped))
            frame_nr = time_to_frame_nr(split_time_stamp(ped))
            event_list.append([frame_nr, 'P'])
            ped_events.append(frame_nr)

    return sorted(event_list,key=lambda l:l[0]), sorted(mtb_events), sorted(ped_events)


def plot_hist(mtb_events, mtb_tracks, ped_events, ped_tracks, name):

    #'''
    m_max = 0
    if(np.max(mtb_events) > np.max(mtb_tracks)):
        m_max = np.max(mtb_events)
    else:
        m_max = np.max(mtb_tracks)

    print m_max
    bs = [0, 0.1*m_max, 0.2*m_max, 0.3*m_max, 0.4*m_max, 0.5*m_max, 0.6*m_max, 0.7*m_max, 0.8*m_max, 0.9*m_max, 1*m_max]
    #'''

    mtb_event_hist = np.histogram(mtb_events, bs)
    mtb_event_cumsum = np.cumsum(mtb_event_hist[0])

    mtb_track_hist = np.histogram(mtb_tracks, bs)
    mtb_track_cumsum = np.cumsum(mtb_track_hist[0])

    ped_event_hist = np.histogram(ped_events, bs)
    ped_event_cumsum = np.cumsum(ped_event_hist[0])

    ped_track_hist = np.histogram(ped_tracks, bs)
    ped_track_cumsum = np.cumsum(ped_track_hist[0])

    fig = plt.figure()


    #'''
    mtb_gt_hist = np.minimum(mtb_event_hist[0], mtb_track_hist[0])

    print('MTB')
    print('TPs : {}'.format(np.sum(mtb_gt_hist)))
    print('FNs : {}'.format(np.sum(mtb_event_hist[0] - mtb_gt_hist)))
    print('FPs : {}'.format(np.sum(mtb_track_hist[0] - mtb_gt_hist)))


    ped_gt_hist = np.minimum(ped_event_hist[0], ped_track_hist[0])
    print('PED')
    print('TPs : {}'.format(np.sum(ped_gt_hist)))
    print('FNs : {}'.format(np.sum(ped_event_hist[0] - ped_gt_hist)))
    print('FPs : {}'.format(np.sum(ped_track_hist[0] - ped_gt_hist)))

    #bins = 20
    #plt.hist(event_hist[0], bs, alpha=0.8, label='FN')
    #plt.hist(mtb_tracks[0], bs, alpha=0.8, label='FP')
    #plt.plot(bs[1:], gt_hist, 'r--', linewidth=1)

    #plt.hist(gt_hist, bs, alpha=0.8, label='TP')
    #plt.bar(event_hist[0], event_hist[1], width=1, label='TP', color='b')
    #'''


    plt.plot(mtb_event_hist[1][1:], mtb_event_cumsum, 'b-', label='MTB GT')
    plt.plot(mtb_track_hist[1][1:], mtb_track_cumsum, 'c--', label='MTB System')

    plt.plot(ped_event_hist[1][1:], ped_event_cumsum, 'r-', label='PED GT')
    plt.plot(ped_track_hist[1][1:], ped_track_cumsum, 'm--', label='PED System')

    plt.legend(loc='upper left')
    fig.suptitle('MTB counting', fontsize=20)
    plt.xlabel('Frame #', fontsize=16)
    plt.ylabel('Frequency', fontsize=16)
    #plt.show()
    fig_name = 'Graphs/{}_distribution.png'.format(name)
    plt.savefig(fig_name)

def plot_events(mtb_events, mtb_tracks, ped_events, ped_tracks):

    plot_hist(mtb_events, mtb_tracks, ped_events, ped_tracks, 'GT vs. tracks')


if __name__ == "__main__":
    """
    Main function for executing the .py script.
    Command:
        -p path/to/detection/file.csv
    Color for type and shape for roots and leaves no shape for the rest

    Inseart GT events as nodes of cirtain color
    """
    # construct the argument parser and parse the arguments
    ap = argparse.ArgumentParser()
    ap.add_argument("-e", "--events", type=str,
                    help="Path to event file")
    ap.add_argument("-t", "--tracks", type=str,
                    help="Path to track file")
    args = vars(ap.parse_args())

    event_list = []
    with open(args["events"], 'rb') as f:
        reader = csv.reader(f)
        event_list = list(reader)

    events, mtb_events, ped_events = split_tracks(event_list)

    '''
    with open(args["events"], 'rb') as f:
        reader = csv.reader(f)
        event_list = list(reader)

    events, mtb_events, ped_events = convert_events(event_list)

    with open(args["events"][:-4]+"_tracks.csv", 'wb') as csvfile:
        event_tracks = csv.writer(csvfile, delimiter=';')
        for event in events:
            event_tracks.writerow(event)
    '''

    track_list = []
    with open(args["tracks"], 'rb') as f:
        reader = csv.reader(f)
        track_list = list(reader)

    tracks, mtb_tracks, ped_tracks = split_tracks(track_list)
    #frame_nr_to_time(track_list)
    plot_events(mtb_events, mtb_tracks, ped_events, ped_tracks)

    '''
    #
    with open('event_frame_nrs.csv', 'wb') as csvfile:
        csv_writer = csv.writer(csvfile, delimiter=';')
        for event in events:
            csv_writer.writerow(event)

    '''


    #warnings.simplefilter("ignore")

    #Graph, node_pos, root_nodes, leave_nodes = populate_graph(dets_list[160:200])

    #plot_graph(Graph, node_pos, root_nodes, leave_nodes)

    #for leave in leave_nodes:
        #sub_nodes = find_preceeding_nodes(G, leave)
        # create subgraph from the predecessors
        #G.subgraph(sub_nodes)

    #pos = {7: [1, 1], 8: [2, 2], 9: [3, 3], 10: [4, 4], 11: [5, 5], 12: [6, 6], 13: [7, 7], 14: [8, 8]}





    """
        #nx.draw(H)

        #nx.draw_networkx_nodes(G, pos, node_size=2000, nodelist=[4])
        #nx.draw_networkx_nodes(G, pos, node_size=3000, nodelist=[0, 1, 2, 3], node_color='b')
        #nx.draw_networkx_edges(G, pos, alpha=0.5, width=6)

        #pos = nx.spring_layout(H, iterations=200)
        #nx.draw(G, nx.spring_layout(G), node_size=800)

        # position on "timeline"
        # color acording to type node_color=['r','r','r','r','b','b'] same length as nodelist



    G = nx.Graph()
    G.add_node("spam")
    G.add_edge('A', 'B')
    G.add_edge('B', 'D')
    G.add_edge('1', '2')
    G.add_edge('2', '3')

    nx.draw(G)
    plt.savefig("simple_path.png") # save as png
    plt.show() # display
    """
