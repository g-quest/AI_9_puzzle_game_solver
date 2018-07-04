'''
9 Puzzle Solver
Author: Gregory V. Cuesta
Date: July 3, 2018

Written in Python 3
'''
from collections import deque
import heapq
import resource
import sys
import time

# take in command-line input
method = sys.argv[1]
board = [int(number) for number in (sys.argv[2]).split(',')]

# 0 represents the blank tile
goalState = [0, 1, 2, 3, 4, 5, 6, 7, 8]

# use to time functions
start_time = time.time()

def main():

	print("\nStarting Board:\n")
	print(" {0} {1} {2} \n".format(board[0], board[1], board[2]))
	print(" {0} {1} {2} \n".format(board[3], board[4], board[5]))
	print(" {0} {1} {2} \n".format(board[6], board[7], board[8]))

	print("Goal:\n")
	print(" {0} {1} {2} \n".format(goalState[0], goalState[1], goalState[2]))
	print(" {0} {1} {2} \n".format(goalState[3], goalState[4], goalState[5]))
	print(" {0} {1} {2} \n".format(goalState[6], goalState[7], goalState[8]))

	if method == 'bfs':
		
		Methods.bfs(board, goalState)

	elif method == 'dfs':
		
		Methods.dfs(board, goalState)

	elif method == 'ast':
		
		Methods.ast(board, goalState)

	elif method == 'ida':
		
		Methods.ida(board, goalState)

	else:
		
		print('\nInvalid method type.')
		print('\nEnter only one of the following: bfs, dfs, ast, ida\n')
		sys.exit()

def output(path_to_goal, cost_of_path, nodes_expanded, fringe_size, max_fringe_size, 
	search_depth, running_time, max_ram_usage):


	print('--------  output.txt file created with the following:  --------\n')
	print('path_to_goal: {0}\n'.format(path_to_goal))
	print('cost_of_path: {0}\n'.format(cost_of_path))
	print('nodes_expanded: {0}\n'.format(nodes_expanded))
	print('fringe_size: {0}\n'.format(fringe_size))
	print('max_fringe_size: {0}\n'.format(max_fringe_size))
	print('search_depth: {0}\n'.format(search_depth))
	print('running_time: {:.8f}\n'.format(running_time)) 
	print('max_ram_usage: {:.8f}\n'.format(max_ram_usage))

	# create and write results to output.txt for grading
	file = open('output.txt','w') 
 
	file.write('path_to_goal: {0}\n'.format(path_to_goal))
	file.write('cost_of_path: {0}\n'.format(cost_of_path))
	file.write('nodes_expanded: {0}\n'.format(nodes_expanded))
	file.write('fringe_size: {0}\n'.format(fringe_size))
	file.write('max_fringe_size: {0}\n'.format(max_fringe_size))
	file.write('search_depth: {0}\n'.format(search_depth))
	file.write('running_time: {:.8f}\n'.format(running_time)) 
	file.write('max_ram_usage: {:.8f}\n'.format(max_ram_usage))

	file.close()

class Moves:

	def up(state):

		zeroPosition = state.index(0)
		newStateUp = state[:]

		if (zeroPosition != 0) & (zeroPosition != 1) & (zeroPosition != 2):
			
			newPosition = zeroPosition - 3
			tempHold = newStateUp[newPosition]
			newStateUp[newPosition] = 0 # moves 0 to new position
			newStateUp[zeroPosition] = tempHold # moves tile being swapped

			return ("Up", newStateUp)

		else:

			return None # can't move up if in top row

	def down(state):

		zeroPosition = state.index(0)
		newStateDown = state[:]

		if (zeroPosition != 6) & (zeroPosition != 7) & (zeroPosition != 8):
			
			newPosition = zeroPosition + 3
			tempHold = newStateDown[newPosition]
			newStateDown[newPosition] = 0 
			newStateDown[zeroPosition] = tempHold 

			return ("Down", newStateDown)

		else:

			return None # can't move down if in bottom row

	def left(state):

		zeroPosition = state.index(0)
		newStateLeft = state[:]

		if (zeroPosition != 0) & (zeroPosition != 3) & (zeroPosition != 6):
			
			newPosition = zeroPosition - 1
			tempHold = newStateLeft[newPosition]
			newStateLeft[newPosition] = 0 
			newStateLeft[zeroPosition] = tempHold 

			return ("Left", newStateLeft)

		else:

			return None # can't move left if in left column		

	def right(state):

		zeroPosition = state.index(0)
		newStateRight = state[:]

		if (zeroPosition != 2) & (zeroPosition != 5) & (zeroPosition != 8):
			
			newPosition = zeroPosition + 1
			tempHold = newStateRight[newPosition]
			newStateRight[newPosition] = 0 
			newStateRight[zeroPosition] = tempHold 

			return ("Right", newStateRight)

		else:

			return None # can't move right if in right column		

class Nodes:
	
	def neighbors(state):

		expandedNode = []

		expandedNode.append(Moves.up(state))
		expandedNode.append(Moves.down(state))		
		expandedNode.append(Moves.left(state))
		expandedNode.append(Moves.right(state))

		# remove any nodes with None value
		expandedNode = [node for node in expandedNode if node != None]
		
		return expandedNode

	def heuristic(initialState, goalState):

		mhd = []
		for each in initialState:
			
			if initialState.index(0) == 0:

				pass

			else:
				
				mhd.append(Nodes.manhattan(initialState.index(goalState[each]), goalState[each])) 

		return sum(mhd) 
            
	def manhattan(initialState, goalState):

		# find Manhattan Distance of individual tiles to GoalState tiles
		mhd = abs(initialState // 3 - goalState // 3) + abs(initialState % 3 - goalState % 3)

		return mhd

	def findPath(parents, goalState, initialState):
		
		path = [tuple(goalState)]
		parentState = tuple()
		state = tuple(goalState)

		while state != tuple(initialState):
			
			parentState = (tuple(list(parents.values())[list(parents.keys()).index(state)]))
			
			path.append(parentState)
			
			state = parentState

		path.reverse()

		return path

class Methods:

	# Breadth-First Search
	def bfs(initialState, goalState):

		frontierQueue = deque([initialState])
		exploredSet = set()
		fringeCountTracker = [1]
		parents = {tuple(initialState): None}
		movesTracker = []
		depthMarkers = {tuple(initialState): 0}

		while (len(frontierQueue) != 0):

			state = frontierQueue.popleft() # deque method that ensures FIFO
			
			if state == goalState:

				path = Nodes.findPath(parents, goalState, initialState)			
				path_to_goal = []
				for move in movesTracker:
			
					if (tuple(move[1]) in path):
			
						path_to_goal.append(move[0])
				
				cost_of_path = len(path_to_goal) 
				nodes_expanded = len(exploredSet) # goal state excluded
				fringe_size = len(frontierQueue) 
				max_fringe_size = max(fringeCountTracker) 
				search_depth = len(path) - 1 # root node depth = 0
				running_time = time.time() - start_time
				max_ram_usage = (resource.getrusage(resource.RUSAGE_SELF).ru_maxrss) / 1000000

				output(path_to_goal, cost_of_path, nodes_expanded, fringe_size, max_fringe_size, 
					search_depth, running_time, max_ram_usage)

				break
			
			exploredSet.add(tuple(state))

			# expand node
			for neighbor in Nodes.neighbors(state):

				if (neighbor[1] not in frontierQueue) & (tuple(neighbor[1]) not in exploredSet):
		
					frontierQueue.append(neighbor[1])
					parents.update({tuple(neighbor[1]):state})				
					movesTracker.append(neighbor)

			fringeCountTracker.append(len(frontierQueue))


	# Depth-First Search
	def dfs(initialState, goalState):
		
		frontierStack = [initialState]
		frontierSet = set(tuple(initialState))
		exploredSet = set()
		fringeCountTracker = [1]
		parents = {tuple(initialState): None}
		movesTracker = []
		depthMarkers = {tuple(initialState): 0}

		while (len(frontierStack) != 0):

			state = frontierStack.pop() # list method that ensures LIFO

			if state == goalState:
			
				path = Nodes.findPath(parents, goalState, initialState)	
				path_to_goal = []
				for move in movesTracker:			
			
					if (tuple(move[1]) in path):			
			
						path_to_goal.append(move[0])

				cost_of_path = len(path_to_goal) 
				nodes_expanded = len(exploredSet)
				fringe_size = len(frontierStack) 
				max_fringe_size = max(fringeCountTracker)
				search_depth = len(path) - 1
				running_time = time.time() - start_time
				max_ram_usage = (resource.getrusage(resource.RUSAGE_SELF).ru_maxrss) / 1000000

				output(path_to_goal, cost_of_path, nodes_expanded, fringe_size, max_fringe_size, 
					search_depth, running_time, max_ram_usage)

				break

			exploredSet.add(tuple(state))

			for neighbor in reversed(Nodes.neighbors(state)):
				
				if (tuple(neighbor[1]) not in frontierSet) & (tuple(neighbor[1]) not in exploredSet):
				
					frontierStack.append(neighbor[1])				
					frontierSet.add(tuple(neighbor[1]))				
					parents.update({tuple(neighbor[1]):state})				
					movesTracker.append(neighbor)

			fringeCountTracker.append(len(frontierStack))

	# A-Star Search
	def ast(initialState, goalState):

		frontierPQ = [(((Nodes.heuristic(initialState, goalState)), initialState))]
		exploredSet = set()
		fringeCountTracker = [1]
		parents = {tuple(initialState): None}
		movesTracker = []

		while (len(frontierPQ) != 0):

			state = heapq.heappop(frontierPQ)

			if list(state[1]) == goalState:

				path = Nodes.findPath(parents, goalState, initialState)
				path_to_goal = []
				for move in movesTracker:
					
					if (tuple(move[1]) in path):
				
						path_to_goal.append(move[0])

				cost_of_path = len(path_to_goal) 
				nodes_expanded = len(exploredSet)
				fringe_size = len(frontierPQ) 
				max_fringe_size = max(fringeCountTracker)
				search_depth = len(path) - 1
				running_time = time.time() - start_time
				max_ram_usage = (resource.getrusage(resource.RUSAGE_SELF).ru_maxrss) / 1000000

				output(path_to_goal, cost_of_path, nodes_expanded, fringe_size, max_fringe_size, 
					search_depth, running_time, max_ram_usage)

				break

			exploredSet.add(tuple(state[1]))

			for neighbor in Nodes.neighbors(list(state[1])):
				
				if (((Nodes.heuristic(neighbor[1], goalState)) not in frontierPQ) & (tuple(((Nodes.heuristic(neighbor[1], goalState)), neighbor[1])[1]) not in exploredSet)):
					
					heapq.heappush(frontierPQ, (Nodes.heuristic(neighbor[1], goalState), neighbor[1]))					
					parents.update({tuple(neighbor[1]):state[1]})				
					movesTracker.append(neighbor)

			fringeCountTracker.append(len(frontierPQ))

	# IDA-Star Search
	def ida(initialState, goalState):

		frontierStack = [(((Nodes.heuristic(initialState, goalState)), initialState))]
		exploredSet = set()
		fringeCountTracker = [1]
		parents = {tuple(initialState): None}
		movesTracker = []

		# heuristic for the initial state
		limit = frontierStack[0][0]

		while True:

			state = frontierStack.pop()

			if state[1] == goalState:

				path = Nodes.findPath(parents, goalState, initialState)
				path_to_goal = []
				for move in movesTracker:
					
					if (tuple(move[1]) in path):
						
						path_to_goal.append(move[0])

				cost_of_path = len(path_to_goal) 
				nodes_expanded = len(exploredSet)
				fringe_size = len(frontierStack) 
				max_fringe_size = max(fringeCountTracker)
				search_depth = len(path) - 1
				running_time = time.time() - start_time
				max_ram_usage = (resource.getrusage(resource.RUSAGE_SELF).ru_maxrss) / 1000000

				output(path_to_goal, cost_of_path, nodes_expanded, fringe_size, max_fringe_size, 
					search_depth, running_time, max_ram_usage)

				break

			exploredSet.add(tuple(state[1]))

			for neighbor in Nodes.neighbors(list(state[1])):

				if (Nodes.heuristic(neighbor[1], goalState)) < limit:
					
					frontierStack.append(neighbor)					
					parents.update({tuple(neighbor[1]):state[1]})					
					movesTracker.append(neighbor)

					# change limit to lowest heuristic value of nieghbors
					limit = Nodes.heuristic(neighbor[1], goalState)								

				else:

					pass

			fringeCountTracker.append(len(frontierStack))

main()


