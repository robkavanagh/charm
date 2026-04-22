# This script plots the inferred 3D geometry for the magnetic field.

import numpy as np
import matplotlib.pyplot as plt
import json

rad_per_deg = np.pi / 180

color_lines = 'black'
color_B = 'xkcd:light red'
color_rot = 'xkcd:cerulean'
color_LOS = 'xkcd:light orange'

lw = 3
lw_thin = 2


###################################
# Parameters
###################################

# Camera
phi_cam = 45 * rad_per_deg
theta_cam = 90 * rad_per_deg

# Rotation phase
phi_rot = 35 * rad_per_deg

# Loop size
L = 3
theta_min = np.arcsin(L ** - 0.5)

# Get most likely geometric parameters
results = json.load(open('charm_runs/run1/info/results.json'))
cos_i = results['maximum_likelihood']['point'][results['paramnames'].index('cos_i')]
beta = results['maximum_likelihood']['point'][results['paramnames'].index('beta')]


###################################
# Vectors
###################################

# Repeated terms
sin_i = np.sin(np.arccos(cos_i))
sin_beta = np.sin(beta)
cos_beta = np.cos(beta)
sin_phi_rot = np.sin(phi_rot)
cos_phi_rot = np.cos(phi_rot)
sin_theta_cam = np.sin(theta_cam)
cos_theta_cam = np.cos(theta_cam)
sin_phi_cam = np.sin(phi_cam)
cos_phi_cam = np.cos(phi_cam)

# Camera position
x_cam, y_cam, z_cam = np.eye(3)

# Line of sight
n = sin_theta_cam * x_cam - cos_theta_cam * z_cam
x = cos_phi_cam * n - sin_phi_cam * y_cam
y = sin_phi_cam * n + cos_phi_cam * y_cam
z = cos_theta_cam * x_cam + sin_theta_cam * z_cam

# Rotation
n_rot = sin_i * x - cos_i * z
x_rot = sin_phi_rot * y + cos_phi_rot * n_rot
y_rot = cos_phi_rot * y - sin_phi_rot * n_rot
z_rot = cos_i * x + sin_i * z

# Magnetic
n_B = x_rot * cos_beta - z_rot * sin_beta
z_B = x_rot * sin_beta + z_rot * cos_beta


###################################
# Figure setup
###################################

fig_width = 6
fig_height = 4

xmax = 5.5
ymax = xmax * fig_height / fig_width

fig = plt.figure(figsize = (fig_width, fig_height))
ax = fig.subplots()
ax.set_aspect('equal')
ax.set_xlim(- xmax, xmax)
ax.set_ylim(- ymax, ymax)
ax.add_artist(plt.Circle((0, 0), radius = 1, ec = color_lines, fc = 'none', zorder = 0, lw = lw))

ax.set_aspect('equal')
ax.set_facecolor('none')
ax.axis('off')


###################################
# Lines of constant latitude
###################################

nphi = 500
phi = np.linspace(0, 2 * np.pi, nphi)

theta_line = np.array([30, 60, 90, 120, 150]) * rad_per_deg
ls = ['--', '--', '-', '--', '--']

for j, theta_line in enumerate(theta_line):

	x_line = np.sin(theta_line) * (np.cos(phi) * x_rot[0] + np.sin(phi) * y_rot[0]) + np.cos(theta_line) * z_rot[0]
	y_line = np.sin(theta_line) * (np.cos(phi) * x_rot[1] + np.sin(phi) * y_rot[1]) + np.cos(theta_line) * z_rot[1]
	z_line = np.sin(theta_line) * (np.cos(phi) * x_rot[2] + np.sin(phi) * y_rot[2]) + np.cos(theta_line) * z_rot[2]

	mask = x_line < 0
	y_line[mask] = np.nan
	z_line[mask] = np.nan

	ax.plot(y_line, z_line, color = color_lines, ls = ls[j], lw = lw, zorder = 0)


###################################
# Draw background field
###################################

ntheta = 500
theta = np.linspace(theta_min, np.pi - theta_min, ntheta)
sin_theta = np.sin(theta)
cos_theta = np.cos(theta)

nphi = 9
phi_B_arr = np.linspace(0, 2 * np.pi, nphi + 1)[:-1] + 0.2 * 2 * np.pi

for phi_B in phi_B_arr:

	x_B = np.sin(phi_B) * y_rot + np.cos(phi_B) * n_B

	r = L * sin_theta ** 2

	x_line = r * (sin_theta * x_B[0] + cos_theta * z_B[0])
	y_line = r * (sin_theta * x_B[1] + cos_theta * z_B[1])
	z_line = r * (sin_theta * x_B[2] + cos_theta * z_B[2])

	r_line = (x_line ** 2 + y_line ** 2 + z_line ** 2) ** 0.5
	c_line = (y_line ** 2 + z_line ** 2) ** 0.5

	mask = (r_line < 1) | ((x_line < 0) & (c_line < 1))
	y_line[mask] = np.nan
	z_line[mask] = np.nan

	ax.plot(y_line, z_line, color = color_lines, lw = lw_thin, zorder = 2)


###################################
# Precession path for magnetic axis
###################################

phi_pre = np.linspace(0, 2 * np.pi, 1000)
sin_phi_pre = np.sin(phi_pre)
cos_phi_pre = np.cos(phi_pre)

x_pre = (sin_phi_pre * y[0] + cos_phi_pre * n_rot[0]) * sin_beta + z_rot[0] * cos_beta
y_pre = (sin_phi_pre * y[1] + cos_phi_pre * n_rot[1]) * sin_beta + z_rot[1] * cos_beta
z_pre = (sin_phi_pre * y[2] + cos_phi_pre * n_rot[2]) * sin_beta + z_rot[2] * cos_beta

c_pre = (y_pre ** 2 + z_pre ** 2) ** 0.5

mask_pre = ((x_pre < 0) & (c_pre < 1))
y_pre[mask_pre] = np.nan
z_pre[mask_pre] = np.nan

ax.plot(y_pre, z_pre, color = color_B, lw = lw_thin, alpha = 0.8, zorder = 1, ls = '--')

###################################
# Plot vectors
###################################

def plot_vec(v, l, arrowprops):

	x0, y0, z0 = v
	x1, y1, z1 = v * l

	ax.annotate('', (y1, z1), (y0, z0), arrowprops = arrowprops)

arrowstyle = '->, head_length = 1, head_width = 0.5'

plot_vec(x, 3, dict(arrowstyle = arrowstyle, color = color_LOS, lw = lw, label = 'test'))
plot_vec(z_rot, 3, dict(arrowstyle = arrowstyle, color = color_rot, lw = lw))
plot_vec(z_B, 3, dict(arrowstyle = arrowstyle, color = color_B, lw = lw))

ax.plot([], [], color = color_LOS, lw = lw, label = 'Line of sight')
ax.plot([], [], color = color_rot, lw = lw, label = 'Rotation axis')
ax.plot([], [], color = color_B, lw = lw, label = 'Magnetic axis')
ax.plot([], [], color = color_B, lw = lw_thin, ls = '--', label = 'Precession path')

ax.legend(frameon = False, loc = 'lower left', bbox_to_anchor = (0.02, 0.02))

plt.subplots_adjust(left = 0, right = 1, bottom = 0, top = 1)
plt.show()