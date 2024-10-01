import serial
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# Set up the serial port
ser = serial.Serial('COM3', 9600)  
data = []  # List to hold values
labels = []  # List to hold labels
colors = ["#66c2a5","#fc8d62","#8da0cb"] # the colors for each bar

# Set up the plot
fig, ax = plt.subplots()
bar_container = ax.bar([], [])

ax.set_ylim(0, 5)  # Adjust y-axis limits for your data range
ax.set_xticks(range(1))  # Placeholder for x-ticks

def init():
    global bar_container
    bar_container = ax.bar([], [], color=colors)
    return bar_container,

def update(frame):
    global data, labels
    if ser.in_waiting:
        try:
            line = ser.readline().decode('utf-8').strip()
            label, value = line.split(': ')  # Split the labeled data
            value = int(value)
            print(f"Received: {label.strip()} = {value}")  # Print received data

            # Update lists
            if label not in labels:
                labels.append(label)
                data.append(value)
            else:
                index = labels.index(label)
                data[index] = 5 - value  # Update existing value

            # Update bar chart
            ax.clear()  # Clear previous bars
            thebars = ax.bar(labels, data, color = colors)  # Create new bar chart
            #Draw ticks
            for bar in thebars:
                y_value = bar.get_height()
                for i in range(1, y_value+1):
                    plt.hlines(i,bar.get_x(),bar.get_x()+bar.get_width(), color = "gray", linestyle = "--", linewidth =2)

            ax.set_ylim(0, 5)  # Keep the y-limit consistent
            ax.set_xticks(labels)  # Set x-ticks to labels
            ax.set_ylabel("Values")  # Label y-axis
            ax.set_title("Real-time Data Plot")  # Title for the plot

        except ValueError:
            pass  # Handle any conversion errors
    return bar_container,

# Create an animation
ani = animation.FuncAnimation(fig, update, init_func=init, blit=False, interval=100)

plt.show()
