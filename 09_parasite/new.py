import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation
from numba import njit


FOOD = 50
SIZE = 30
P = 0.001
Q = 0.02
GENERATIONS = 500


@njit
def simulate(
    food,
    size,
    p,
    q,
    generations,
):

    whole_data_a = np.zeros(
        (generations, size, size),
        dtype=np.int32,
    )

    whole_data_b = np.zeros(
        (generations, size, size),
        dtype=np.int32,
    )

    population_a = np.full(
        (size, size),
        100,
        dtype=np.int32,
    )

    population_b = np.zeros(
        (size, size),
        dtype=np.int32,
    )

    mutation_max = int(1 / p)
    move_max = int(1 / q)

    for generation in range(generations):

        # Revised implementation
        # Reset at every generation
        next_a = np.zeros(
            (size, size),
            dtype=np.int32,
        )

        next_b = np.zeros(
            (size, size),
            dtype=np.int32,
        )

        # ------------------
        # Reproduction
        # ------------------

        for i in range(size):
            for j in range(size):

                if food >= population_a[i, j]:
                    next_a[i, j] = population_a[i, j] * 2
                else:
                    next_a[i, j] = food * 2

                if next_a[i, j] >= population_b[i, j]:

                    next_b[i, j] = (
                        population_b[i, j] * 2
                    )

                    next_a[i, j] -= population_b[i, j]

                else:

                    next_b[i, j] = (
                        next_a[i, j] * 2
                    )

                    next_a[i, j] = 0

                if np.random.randint(
                    0,
                    mutation_max + 1,
                ) == 0:

                    next_b[i, j] += 1

        # ------------------
        # Movement
        # ------------------

        for i in range(-1, size - 1):
            for j in range(-1, size - 1):

                if (
                    np.random.randint(
                        0,
                        move_max + 1,
                    )
                    < next_a[i, j]
                ):
                    next_a[i + 1, j] += 1
                    next_a[i, j] -= 1

                if (
                    np.random.randint(
                        0,
                        move_max + 1,
                    )
                    < next_a[i, j]
                ):
                    next_a[i - 1, j] += 1
                    next_a[i, j] -= 1

                if (
                    np.random.randint(
                        0,
                        move_max + 1,
                    )
                    < next_a[i, j]
                ):
                    next_a[i, j + 1] += 1
                    next_a[i, j] -= 1

                if (
                    np.random.randint(
                        0,
                        move_max + 1,
                    )
                    < next_a[i, j]
                ):
                    next_a[i, j - 1] += 1
                    next_a[i, j] -= 1

                if (
                    np.random.randint(
                        0,
                        move_max + 1,
                    )
                    < next_b[i, j]
                ):
                    next_b[i + 1, j] += 1
                    next_b[i, j] -= 1

                if (
                    np.random.randint(
                        0,
                        move_max + 1,
                    )
                    < next_b[i, j]
                ):
                    next_b[i - 1, j] += 1
                    next_b[i, j] -= 1

                if (
                    np.random.randint(
                        0,
                        move_max + 1,
                    )
                    < next_b[i, j]
                ):
                    next_b[i, j + 1] += 1
                    next_b[i, j] -= 1

                if (
                    np.random.randint(
                        0,
                        move_max + 1,
                    )
                    < next_b[i, j]
                ):
                    next_b[i, j - 1] += 1
                    next_b[i, j] -= 1

        whole_data_a[generation] = population_a
        whole_data_b[generation] = population_b

        population_a = next_a.copy()
        population_b = next_b.copy()

    return (
        whole_data_a,
        whole_data_b,
    )


whole_data_a, whole_data_b = simulate(
    FOOD,
    SIZE,
    P,
    Q,
    GENERATIONS,
)

fig = plt.figure(
    figsize=(6, 3),
    tight_layout=True,
)

ax1 = fig.add_subplot(1, 2, 1)
ax2 = fig.add_subplot(1, 2, 2)

images = []

for i in range(
    0,
    GENERATIONS,
    5,
):

    img1 = ax1.imshow(
        whole_data_a[i],
        interpolation="none",
        vmin=0,
        vmax=100,
        cmap="jet",
        extent=(0, SIZE, 0, SIZE),
    )

    img2 = ax2.imshow(
        whole_data_b[i],
        interpolation="none",
        vmin=0,
        vmax=100,
        cmap="jet",
        extent=(0, SIZE, 0, SIZE),
    )

    images.append(
        [img1, img2]
    )

fig.colorbar(
    img1,
    shrink=0.7,
)

fig.colorbar(
    img2,
    shrink=0.7,
)

ani = animation.ArtistAnimation(
    fig,
    images,
    interval=200,
)

plt.show()
