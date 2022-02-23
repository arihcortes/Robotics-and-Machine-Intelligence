from math import radians
import numpy as np
import matplotlib.pyplot as plt


# uses the robots joints to plot the robots arms
def drawRobot(joints):
    eJoints = []

    for arm in joints:    
        plt.clf()
        x, y = list(zip(*arm))    
        plt.plot(x, y, 'o-', lw=3, ms=6)
        
        eJoints.append(arm[-1])
        x, y = list(zip(*eJoints))    
        plt.plot(x, y, 'o--', c='r', lw=1, ms=6)
        
        plt.axis('square')
        plt.pause(0.5)
        plt.draw()
    
    plt.show()    
        

# calculates joint positions using arm lengths and angles
def forwardKinematics(thetas, lengths):
    joints = [[0,0]]
    theta = 0
    
    for i in range(len(thetas)): 
        theta += thetas[i]
        joints.append([
            joints[-1][0] + lengths[i]*np.cos(theta),
            joints[-1][1] + lengths[i]*np.sin(theta)
        ])

    return joints


# calculates partial derivatives given current angles and lengths
def invJacobian(thetas, lengths):
    jacobian = []
    
    for i in range(len(thetas)):
        ddt = [0, 0]
        theta = 0

        for j in range(len(thetas), i, -1):
            theta = sum(thetas[:j])
            ddt[0] -= lengths[j-1]*np.sin(theta)
            ddt[1] += lengths[j-1]*np.cos(theta)
            
        jacobian.append(ddt)
    
    return np.linalg.pinv(list(zip(*jacobian)))
    

# calculates joint angles needed to touch target
def inverseKinematics(thetas, lengths, target):
    thetaMax = radians(15)
    tolerance = 1
    
    joints = [forwardKinematics(thetas, lengths)]
    error = [t-p for t, p in zip(target, joints[-1][-1])]
    
    while np.linalg.norm(error) > tolerance:
        step = invJacobian(thetas, lengths).dot(error)
        thetas += np.where(
            np.abs(step)>thetaMax, thetaMax*np.sign(step), step
        )
        
        joints.append(forwardKinematics(thetas, lengths))
        error = [t-p for t, p in zip(target, joints[-1][-1])]
    
    drawRobot(joints)    
    
    return joints


# calculate kinematics given initial conditions
thetas = [np.pi/3, 0, 0]
lengths = [10, 10, 10]
target = [6, 12]
    
inverseKinematics(thetas, lengths, target)