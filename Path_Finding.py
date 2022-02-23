import matplotlib.pyplot as plt 
import pickle

# initialize goal and starting position
start = (0, 0)
goal = (49, 49)


# superimposes path onto the maze image
def draw_path(final_path_points, other_path_points):
	im = plt.imread('172maze2021.png')
	x_interval = (686-133)/49
	y_interval = (671-122)/49
	plt.imshow(im)
	fig = plt.gcf()
	ax = fig.gca()
	circle_start = plt.Circle((133,800-122), radius=4, color='lime')
	circle_end = plt.Circle((686, 800-671), radius=4, color='red')
	ax.add_patch(circle_start)
	ax.add_patch(circle_end)
	for point in other_path_points:
		if not (point[0]==0 and point[1]==0) and not (point[0]==49 and point[1]==49):
			circle_temp = plt.Circle((133+point[0]*x_interval, 800-(122+point[1]*y_interval)), radius=4, color='blue')
			ax.add_patch(circle_temp)
	for point in final_path_points:
		if not (point[0]==0 and point[1]==0) and not (point[0]==49 and point[1]==49):
			circle_temp = plt.Circle((133+point[0]*x_interval, 800-(122+point[1]*y_interval)), radius=4, color='yellow')
			ax.add_patch(circle_temp)
	plt.show()


# iterates through the maze pickle and creates nodes for each entry
def getNodes():
	nodes = pickle.load(open("172maze2021.p", "rb"))
	for n in nodes:
		x, y = n
		children = []
		for i, child in enumerate(nodes[n]):	
			if child: children.append((
				x+(i%2)*(-1)**int(i/2),
				y+(i+1)%2*(-1)**int((i+1)/2)
			))
		
		nodes[n] = {
			"children": children,
			"visited": False,
			"parent": None
		}

	return nodes


# implements depth first search using list as a stack
def DFS(start, goal, nodes): 
	stack = [start]
	iterations = 0
	while len(stack) > 0 and goal not in stack:
		node = stack.pop()
		if not nodes[node]["visited"]:	
			nodes[node]["visited"] = True
			for c in nodes[node]["children"]:
				if not nodes[c]["visited"]:
					stack.append(c)
					nodes[c]["parent"] = node
		iterations += 1

	path = []
	node = goal
	while nodes[node]['parent'] != None:
		node = nodes[node]['parent']
		path.append(node)
	
	return path, iterations


# implements breath first search using list as a queue
def BFS(start, goal, nodes): 
	stack = [start]
	iterations = 0
	while len(stack) > 0 and goal not in stack:
		node = stack.pop(0)
		if not nodes[node]["visited"]:	
			nodes[node]["visited"] = True
			for c in nodes[node]["children"]:
				if not nodes[c]["visited"]:
					stack.append(c)
					nodes[c]["parent"] = node
		iterations += 1

	path = []
	node = goal
	while nodes[node]['parent'] != None:
		node = nodes[node]['parent']
		path.append(node)
	
	return path, iterations

nodes = getNodes()


# run DFS and plot the path
path, iterations = DFS(start, goal ,nodes)
print(iterations)
draw_path(path, [])