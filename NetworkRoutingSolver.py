#!/usr/bin/python3


from CS312Graph import *
from PriorityQueue import *
import time


class NetworkRoutingSolver:
    def __init__( self):
        pass

    def initializeNetwork( self, network ):
        assert( type(network) == CS312Graph )
        self.network = network

    def getShortestPath( self, destIndex ):
        self.dest = destIndex
        current_point = self.dest
        path_edges = []
        total_length = 0
        #loops through the shortest path pointers until we get to the source vertex (backwards is faster)
        while not (self.shortestPaths[current_point] is None):
            #find the edge that connects to the previous vertex in the path
            previous = self.shortestPaths[current_point]
            edge = None
            for potentialEdge in self.network.nodes[previous].neighbors:
                if potentialEdge.dest.node_id == current_point:
                    edge = potentialEdge

            #add edge to the list of edge objects (used for display)
            path_edges.append( (edge.src.loc, edge.dest.loc, '{:.0f}'.format(edge.length)) )
            #add to the total path length
            total_length += edge.length
            #move to the previous point in the path for the next iteration
            current_point = previous
        return {'cost':total_length, 'path':path_edges}

    def computeShortestPaths( self, srcIndex, use_heap=False ):
        self.source = srcIndex
        #creating a class variable to hold the pointers in the shortest paths
        self.shortestPaths = [None]*len(self.network.nodes)
        t1 = time.time()
        if use_heap:
            distPQueue = PQueueHeap()
        else:
            distPQueue = PQueueArray()
        #initialize priority queue and set the source vertex's distance to 0
        distPQueue.make_queue(self.network.nodes)
        distPQueue.decrease_key(srcIndex, 0)
        #repeat this n times since that's the max amount it can happen
        for i in range(len(self.network.nodes)):
            #take the closest vertex
            closestNode,cnDist = distPQueue.delete_min()
            #for edge leaving the vertex
            for edge in self.network.nodes[closestNode].neighbors:
                destination = edge.dest.node_id
                edgeDistance = edge.length
                #if the edge points to a vertex we haven't already resolved
                if (not (distPQueue.get_key(destination) is None)):
                    #if the edge creates a shorter path than the current path
                    if(distPQueue.get_key(destination) > cnDist+edgeDistance):
                        #shorten the distance value in the priority queue
                        distPQueue.decrease_key(destination, cnDist+edgeDistance)
                        #update the path pointer value (used to store shortest paths)
                        self.shortestPaths[destination] = closestNode

        t2 = time.time()
        return (t2-t1)


