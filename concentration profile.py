import numpy as np
import matplotlib.pyplot as plt

# Parameters
R = 0.02  # radius of the strawberry in meters (2 cm)
D = 2.5e-9  # water diffusivity in m²/s (you can adjust this)
C0 = 1.0  # initial concentration (100%)
n = 100  # number of radial points
dr = R / n # radial grid spacing
dt = 5  # time step in seconds
t_max = 3600 * 16  # 1 hour in seconds * the number of hours, total time drying

# Spatial grid
r = np.linspace(0, R, n + 1) # radial grid
C = np.ones_like(r) * C0 # initial concentration

# Time integration
n_steps = int(t_max / dt)  # total number of time steps

# Dictionary to save concentration profiles at specific hours
saved_profiles = {}
for hour in [0, 1, 3, 6, 9, 12]:
    saved_profiles[hour] = None  # initialize saved profiles

# Time stepping loop
for step in range(n_steps):
    C_new = np.copy(C)  # create a new concentration array for the current step
    # Update concentration using finite difference method
    for i in range(1, n):
        d2C_dr2 = (C[i + 1] - 2 * C[i] + C[i - 1]) / dr**2  # second derivative
        dC_dr = (C[i + 1] - C[i - 1]) / (2 * dr)  # first derivative
        C_new[i] = C[i] + D * dt * (d2C_dr2 + (2 / r[i]) * dC_dr)  # update concentration

    # Boundary conditions
    C_new[0] = C_new[1]  # symmetry at center
    C_new[-1] = 0.0  # surface is dry

    C = C_new  # update concentration for the next time step

    # Save concentration profiles at specified hours
    if ((step + 1) * dt) % 3600 == 0 and ((step + 1) * dt) // 3600 in saved_profiles:
        hour = ((step + 1) * dt) // 3600
        saved_profiles[hour] = np.copy(C_new)  # save the current concentration profile
        j = -1  # initialize node counter
        if hour == 1:  # print concentration values at 1 hour
            print(f"Concentration values at 3600s:")
            for i in [0, 25, 50, 75, 100]:
                j += 1
                print(f"Node {j} (r = {r[i]*1000:.1f} mm): {C_new[i]*100:.2f}%")

# Plot the final concentration profile
plt.figure(dpi=300)
for hour, profile in saved_profiles.items():
    if profile is not None:  # plot only saved profiles
        plt.plot(r * 1000, profile * 100, label=f'{hour} hour{"s" if hour > 1 else ""}')
plt.xlabel('Radius (mm)', fontsize=12, fontweight='bold')  # x-axis label
plt.ylabel('Ice Concentration (%)', fontsize=12, fontweight='bold')  # y-axis label
plt.legend()  # show legend
plt.grid(True)  # show grid
# plt.savefig('concentration_profile.png', dpi=300, bbox_inches='tight')  # save plot
plt.show()  # display plot

# Plot 2D cross-section of the sphere (center slice)
R_grid = np.linspace(-R, R, 2*n + 1)  # create a grid for the 2D plot
X, Y = np.meshgrid(R_grid, R_grid)  # create meshgrid for 2D plotting
radius = np.sqrt(X**2 + Y**2)  # calculate radius from center

# Create a 2D concentration field using radial symmetry
C_2D = np.interp(radius, r, C)  # interpolate 1D concentration to 2D
C_2D[radius > R] = np.nan  # Mask outside the sphere for plotting

# Plot the 2D concentration field
plt.figure(dpi=300)
plt.imshow(C_2D * 100, extent=[-R*1000, R*1000, -R*1000, R*1000], origin='lower', cmap='Blues', vmin=0, vmax=100)  # display concentration as image
plt.colorbar(label='Ice Concentration (%)')  # colorbar for concentration
plt.xlabel('x (mm)', fontsize=12, fontweight='bold')  # x-axis label
plt.ylabel('y (mm)', fontsize=12, fontweight='bold')  # y-axis label
plt.axis('equal')  # equal aspect ratio
plt.grid(False)  # disable grid

# Add center point marker and label
center_x = center_y = 0  # center coordinates
center_concentration = np.interp(0, r, C) * 100  # concentration at the center
plt.plot(center_x, center_y, 'ro')  # plot center point
plt.text(center_x + 1, center_y + 1, f'{center_concentration:.2f}%', color='red', fontsize=10)  # label center point

plt.savefig('concentration_profile_2D_16hrs.png', dpi=300, bbox_inches='tight')  # save 2D plot (commented out)

plt.show()  # display 2D plot