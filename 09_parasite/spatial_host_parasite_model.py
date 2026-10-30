import copy
import random
import matplotlib.pyplot as plt
from matplotlib import animation


def run_simulation(SIZE=30, P=0.010, Q=0.02, FOOD=50, GENERATIONS=500, graph_mode=True, manual_mode=False):
    
    mutation_threshold = int(1 / P)
    move_threshold = int(1 / Q)

    whole_data_a = []
    whole_data_b = []
    total_a_history = []
    total_b_history = []

    population_a = [[100 for _ in range(SIZE)] for _ in range(SIZE)]
    population_b = [[0 for _ in range(SIZE)] for _ in range(SIZE)]

    for generation in range(GENERATIONS):
        next_a = [[0 for _ in range(SIZE)] for _ in range(SIZE)]
        next_b = [[0 for _ in range(SIZE)] for _ in range(SIZE)]
        total_a = 0
        total_b = 0

        for i in range(SIZE):
            for j in range(SIZE):
                if FOOD >= population_a[i][j]:
                    next_a[i][j] = population_a[i][j] * 2
                else:
                    next_a[i][j] = FOOD * 2

                if next_a[i][j] >= population_b[i][j]:
                    next_b[i][j] = population_b[i][j] * 2
                    next_a[i][j] -= population_b[i][j]
                else:
                    next_b[i][j] = next_a[i][j] * 2
                    next_a[i][j] = 0

                if random.randint(0, mutation_threshold) == 0:
                    next_b[i][j] += 1

        for i in range(-1, SIZE - 1):
            for j in range(-1, SIZE - 1):
                if random.randint(0, move_threshold) < next_a[i][j]:
                    next_a[i + 1][j] += 1; next_a[i][j] -= 1
                if random.randint(0, move_threshold) < next_a[i][j]:
                    next_a[i - 1][j] += 1; next_a[i][j] -= 1
                if random.randint(0, move_threshold) < next_a[i][j]:
                    next_a[i][j + 1] += 1; next_a[i][j] -= 1
                if random.randint(0, move_threshold) < next_a[i][j]:
                    next_a[i][j - 1] += 1; next_a[i][j] -= 1

                if random.randint(0, move_threshold) < next_b[i][j]:
                    next_b[i + 1][j] += 1; next_b[i][j] -= 1
                if random.randint(0, move_threshold) < next_b[i][j]:
                    next_b[i - 1][j] += 1; next_b[i][j] -= 1
                if random.randint(0, move_threshold) < next_b[i][j]:
                    next_b[i][j + 1] += 1; next_b[i][j] -= 1
                if random.randint(0, move_threshold) < next_b[i][j]:
                    next_b[i][j - 1] += 1; next_b[i][j] -= 1

        for i in range(SIZE):
            for j in range(SIZE):
                total_a += next_a[i][j]
                total_b += next_b[i][j]

        total_a_history.append(total_a)
        total_b_history.append(total_b)

        if graph_mode and generation % 5 == 0:
            whole_data_a.append(copy.deepcopy(population_a))
            whole_data_b.append(copy.deepcopy(population_b))

        population_a = copy.deepcopy(next_a)
        population_b = copy.deepcopy(next_b)

    a_survived = total_a_history[-1] > 0
    b_survived = total_b_history[-1] > 0

    if graph_mode:
        fig = plt.figure(figsize=(10, 8), tight_layout=True)
        ax1 = plt.subplot2grid((2, 2), (0, 0))
        ax2 = plt.subplot2grid((2, 2), (0, 1))
        ax3 = plt.subplot2grid((2, 2), (1, 0), colspan=2)

        max_pop = max(max(total_a_history), max(total_b_history)) if total_a_history else 100

        if not manual_mode:
            # Play the animation automatically
            images = []
            for i in range(len(whole_data_a)):
                img1 = ax1.imshow(whole_data_a[i], interpolation="none", vmin=0, vmax=100, cmap="jet", extent=(0, SIZE, 0, SIZE))
                img2 = ax2.imshow(whole_data_b[i], interpolation="none", vmin=0, vmax=100, cmap="jet", extent=(0, SIZE, 0, SIZE))
                gen = i * 5
                line_a, = ax3.plot(range(gen+1), total_a_history[:gen+1], color='blue', label='Host (A)' if i==0 else "")
                line_b, = ax3.plot(range(gen+1), total_b_history[:gen+1], color='red', label='Parasite (B)' if i==0 else "")

                if i == 0:
                    ax3.set_xlim(0, GENERATIONS)
                    ax3.set_ylim(0, max_pop * 1.1)
                    ax3.legend()
                    ax1.set_title("Host (A)")
                    ax2.set_title("Parasite (B)")

                images.append([img1, img2, line_a, line_b])

            fig.colorbar(images[0][0], ax=ax1, shrink=0.7)
            fig.colorbar(images[0][1], ax=ax2, shrink=0.7)
            
            ani = animation.ArtistAnimation(fig, images, interval=200, repeat=False)
            plt.show()

        else:
            current_frame = [0]

            img1 = ax1.imshow(whole_data_a[0], interpolation="none", vmin=0, vmax=100, cmap="jet", extent=(0, SIZE, 0, SIZE))
            img2 = ax2.imshow(whole_data_b[0], interpolation="none", vmin=0, vmax=100, cmap="jet", extent=(0, SIZE, 0, SIZE))
            line_a, = ax3.plot(range(1), total_a_history[:1], color='blue', label='Host (A)')
            line_b, = ax3.plot(range(1), total_b_history[:1], color='red', label='Parasite (B)')

            ax3.set_xlim(0, GENERATIONS)
            ax3.set_ylim(0, max_pop * 1.1)
            ax3.legend()
            ax1.set_title("Host (A) [Click to advance]")
            ax2.set_title("Parasite (B)")

            fig.colorbar(img1, ax=ax1, shrink=0.7)
            fig.colorbar(img2, ax=ax2, shrink=0.7)

            def onclick(event):
                if current_frame[0] < len(whole_data_a) - 1:
                    current_frame[0] += 1
                    i = current_frame[0]
                    gen = i * 5
                    
                    img1.set_data(whole_data_a[i])
                    img2.set_data(whole_data_b[i])
                    line_a.set_data(range(gen+1), total_a_history[:gen+1])
                    line_b.set_data(range(gen+1), total_b_history[:gen+1])
                    
                    fig.canvas.draw_idle()

            fig.canvas.mpl_connect('button_press_event', onclick)
            plt.show()

    return a_survived, b_survived

if __name__ == "__main__":
    run_simulation(SIZE=30, graph_mode=True, manual_mode=False)
