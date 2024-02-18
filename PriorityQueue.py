#!/usr/bin/python3
class PQueueArray:
    def __init__(self):
        #one array for holding distances for each index
        self.keys = []

    def insert(self, key):
        #adds the value to the end of the array, since it is not sorted
        self.keys.append(key)

    def decrease_key(self, point, newKey):
        #simply changes the value at an index, since the array is not sorted
        self.keys[point] = newKey

    def delete_min(self):
        #loops through all values in the array to find the minimum, and the index of the minimum element
        minVertex = 0
        for i in range(len(self.keys)):
            if (not(self.keys[i] is None)):
                if (self.keys[minVertex] is None):
                    minVertex = i
                elif (self.keys[minVertex] > self.keys[i]):
                    minVertex = i

        minDistance = self.keys[minVertex]
        #sets the previous minimum distance to None so it isn't visited again
        self.keys[minVertex] = None

        #return both the point and distance
        return minVertex,minDistance

    def make_queue(self, points):
        #for each point, insert that point
        self.keys = []
        for i in points:
            self.insert(float('inf'))

    def get_key(self, point):
        return self.keys[point]

class PQueueHeap:
    def __init__(self):
        #one array of distances
        self.keys = []
        #one binary heap array that sorts the point indices by distance (points[0] is the closest point)
        self.points = []
        #one array of pointers that tells where to find a given point on the binary tree
        self.treePositions = []

    def insert(self, key):
        #add distance to the distance array
        self.keys.append(key)
        #add the point id to the bottom of points heap
        self.points.append(len(self.points))
        #add the position of the point id to the pointer array
        self.treePositions.append(len(self.treePositions))
        #bubble up the inserted point using a recursive helper function
        self.percolate_up(len(self.points)-1)

    def decrease_key(self, point, key):
        #change the distance in the distance array
        self.keys[point] = key
        #bubble up the point using the recursive helper function and the position of the point from the pointer array
        self.percolate_up(self.treePositions[point])


    def delete_min(self):
        minVals = self.points[0],self.keys[self.points[0]]
        #update the pointers in the pointer array
        self.treePositions[self.points[-1]] = 0
        self.treePositions[self.points[0]] = None
        #replace the top element with the last element
        self.points[0] = self.points[-1]
        self.points.pop()
        #use recursive helper function to let the top node trickle down
        self.percolate_down(0)
        #return the closest point and its distance
        return minVals

    def make_queue(self, points):
        #For each point, add that point
        for i in range(len(points)):
            self.insert(float('inf'))

    def get_key(self, point):
        return self.keys[point]

    def percolate_up(self, pointIndex):
        #if we are at the top, return
        if pointIndex == 0:
            return
        #otherwise, check to see if the current position has a value less than its parent
        parentIndex = ((pointIndex+1)//2)-1
        if self.keys[self.points[pointIndex]] < self.keys[self.points[parentIndex]]:
            #if so, switch the two values
            self.points[pointIndex],self.points[parentIndex] = self.points[parentIndex],self.points[pointIndex]
            #switch the values' pointers
            self.treePositions[self.points[pointIndex]] = pointIndex
            self.treePositions[self.points[parentIndex]] = parentIndex
            #call recursively on the same value in its new position
            self.percolate_up(parentIndex)


    def percolate_down(self, pointIndex):
        childIndex = ((pointIndex+1)*2)-1
        #if both child points are occupied:
        if ((childIndex+1) < len(self.points)):
            #find the lower value child:
            if self.keys[self.points[childIndex]] > self.keys[self.points[childIndex+1]]:
                minChildIndex = childIndex+1
            else:
                minChildIndex = childIndex
            #if the lower child is lower than the current value
            if (self.keys[self.points[pointIndex]] > self.keys[self.points[minChildIndex]]):
                #switch child and parent
                self.points[pointIndex],self.points[minChildIndex] = self.points[minChildIndex],self.points[pointIndex]
                #update pointers
                self.treePositions[self.points[pointIndex]] = pointIndex
                self.treePositions[self.points[minChildIndex]] = minChildIndex
                #call recursively on the same value in the child's position
                self.percolate_down(minChildIndex)
        #if only the left child is occupied
        elif (childIndex < len(self.points)):
            #if that child is a lower value than the current value
            if (self.keys[self.points[pointIndex]] > self.keys[self.points[childIndex]]):
                #switch child and parent
                self.points[pointIndex],self.points[childIndex] = self.points[childIndex],self.points[pointIndex]
                #update pointers
                self.treePositions[self.points[pointIndex]] = pointIndex
                self.treePositions[self.points[childIndex]] = childIndex
                #call recusively on the same value in the child's position
                self.percolate_down(childIndex)
