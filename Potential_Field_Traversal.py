import numpy as np
import matplotlib.pyplot as plt

initial_loc = np.array([0,0])		# robot starting location
final_loc = np.array([100,100])		# robot ending location goal
sigma = np.array([[50,0],[0,50]])
mu = np.array([[40, 30], [50, 80]])	# obstacle locations


# generates the potential field given obstical and goal locations
def f(x, y):
	goalGradient = ((final_loc[0]-x)**2 + (final_loc[1]-y)**2)/20000
	repulsorMagnitude = 10000*(1/(2*np.pi*np.linalg.det(sigma)))
	obstacleRepulsor1 = np.exp(-.5*(np.matmul(np.array([x-mu[0,0], y-mu[0,1]]),np.matmul(np.linalg.pinv(sigma), np.atleast_2d(np.array([x-mu[0,0], y-mu[0,1]])).T)))[0]) 
	obstacleRepulsor2 = np.exp(-.5*(np.matmul(np.array([x-mu[1,0], y-mu[1,1]]),np.matmul(np.linalg.pinv(sigma), np.array([x-mu[1,0], y-mu[1,1]])))))

	return goalGradient+repulsorMagnitude*(obstacleRepulsor1+obstacleRepulsor2)


# plots the potential field in 3d
def plot3D(x, y, z, descent=None):
	fig = plt.figure()
	ax = plt.axes(projection='3d')
	ax.contour3D(x, y, z, 25)
	
	if descent != None:
		ax.plot(descent[0], descent[1], descent[2], 'o-')
	
	ax.set_xlabel('x')
	ax.set_ylabel('y')
	ax.set_zlabel('z')
	ax.set_title('3D Contour')
	plt.show()


# plots the potential field and gradient descent in 2d
def plot2D(x, y, z, quiver=False, descent=None):
	fig, ax = plt.subplots(1, 1)
	
	cp = ax.contour(x, y, z, 10)
	fig.colorbar(cp)
	
	if quiver:
		dy, dx = np.gradient(-z)
		step = 5
		ax.quiver(
			x[::step], y[::step], 
			dx[::step, ::step], dy[::step, ::step],
			z[::step, ::step], scale = 1, headwidth = 5
		)
	
	if descent != None:
		ax.plot(descent[0], descent[1], 'o-')
	
	ax.set_xlabel('x')
	ax.set_ylabel('y')
	ax.set_title('Descent Quivers')
	plt.show()


# performs a descent on the gradient of z and stores the positions
def gradientDescent(initial_loc, z):
	x, y = initial_loc
	pos = [[x, y, z[x,y]]]
	dy, dx = np.gradient(z)
	alpha = pow(10,3)
	stepMin = pow(10,-4)
	momentum = 0.5
	step = [
		dx[int(pos[-1][1]), int(pos[-1][0])], 
		dy[int(pos[-1][1]), int(pos[-1][0])]
	]
		
	while np.linalg.norm(step) > stepMin:
		x = pos[-1][0] if pos[-1][0]<len(z[0]) else len(z[0])-1
		y = pos[-1][1] if pos[-1][1]<len(z[1]) else len(z[1])-1
		
		step = [
			step[0]*momentum + dx[int(y), int(x)]*(1-momentum), 
			step[1]*momentum + dy[int(y), int(x)]*(1-momentum)
		]

		x = pos[-1][0]-alpha*step[0]
		y = pos[-1][1]-alpha*step[1]
		pos.append([x, y, z[int(x),int(y)]])
	
	return list(zip(*pos))
	

# get the descent path and map 2d and 3d maps
x = np.linspace(0, 100, 100)
y = np.linspace(0, 100, 100)
z = f(x[:,None], y[None,:])
z = np.rot90(np.fliplr(z))

descent = gradientDescent(initial_loc, z)
plot2D(x, y, z, True, descent)
plot3D(x, y, z, descent)