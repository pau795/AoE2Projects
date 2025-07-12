import numpy as np
from AoE2ScenarioParser.objects.support.area import Area
from AoE2ScenarioParser.objects.support.tile import Tile
from AoE2ScenarioParser.scenarios.aoe2_de_scenario import AoE2DEScenario
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import seaborn as sns


class AreaOptimizer:

    def __init__(self, scenario: AoE2DEScenario, debug: bool = False):
        self.scenario = scenario
        self.map_manager = scenario.map_manager
        self.scenario.new.area()
        self.debug = debug

    def create_area(self, x1: int, y1: int, x2: int, y2: int) -> Area:
        area = self.scenario.new.area()
        area.x1 = int(x1)
        area.y1 = int(y1)
        area.x2 = int(x2)
        area.y2 = int(y2)
        return area

    def optimize_area(self, area_list: list[Area] = None, tile_list: list[Tile] = None) -> list[Area]:
        grid = np.zeros((self.map_manager.map_width, self.map_manager.map_height), dtype=bool)
        if tile_list:
            for tile in tile_list:
                grid[tile.x, tile.y] = True
        if area_list:
            for area in area_list:
                for tile in area.to_coords():
                    grid[tile.x, tile.y] = True

        new_areas = self.greedy_strip_merge(grid)
        if self.debug:
            self.show_differences(grid, new_areas)
        return new_areas

    def show_differences(self, grid: np.ndarray, new_areas: list[Area]):
        new_grid = np.zeros((self.map_manager.map_width, self.map_manager.map_height), dtype=bool)
        for area in new_areas:
            for tile in area.to_coords():
                new_grid[tile.x, tile.y] = True
        diff = grid != new_grid
        fig, ax = plt.subplots(1, 3, figsize=(9, 3))

        # original matrices
        sns.heatmap(grid, ax=ax[0], cbar=False, vmin=0, vmax=1, cmap="binary")
        ax[0].set_title("Matrix A")
        sns.heatmap(new_grid, ax=ax[1], cbar=False, vmin=0, vmax=1, cmap="binary")
        ax[1].set_title("Matrix B")

        # highlight differences: white = same, red = different

        cmap = mcolors.ListedColormap(["white", "red"])
        sns.heatmap(diff, ax=ax[2], cbar=False, vmin=0, vmax=1, cmap=cmap)
        ax[2].set_title("A ≠ B")

        for a in ax:
            a.set_xticks([])
            a.set_yticks([])

        plt.tight_layout()
        plt.show()

    def greedy_strip_merge(self, grid: np.ndarray) -> list[Area]:
        """
        Linear-time rectangle cover for large binary grids (≤250×250).

        Strategy
        --------
        1. Scan each row and split it into maximal “runs” of consecutive 1s: [x1, x2].
        2. Maintain an `active` dict mapping a run (x1, x2) to the rectangle
           that currently extends downward through successive rows.
        3. When the run re-appears in the next row we simply extend the rectangle’s
           bottom edge; if it disappears we close (emit) that rectangle.
        """

        if grid.dtype != np.bool_:
            grid = grid.astype(bool)

        rows, cols = grid.shape
        rectangles: list[Area] = []
        active: dict[tuple[int, int], tuple[int, int]] = {}
        #          run (x1,x2)     -> (y_top, y_bottom_so_far)

        for x in range(rows):
            row = grid[x]
            # -------- 1. find horizontal runs of 1s in this row --------
            # pad with 0 on both sides then look at rising edges
            padded = np.pad(row.astype(int), (1, 1))
            # indices where value changes 0->1
            starts = np.where((padded[1:-1] == 1) & (padded[:-2] == 0))[0]
            # indices where value changes 1->0
            ends = np.where((padded[1:-1] == 1) & (padded[2:] == 0))[0]

            new_active: dict[tuple[int, int], tuple[int, int]] = {}

            for y1, y2 in zip(starts, ends):
                run = (y1, y2)  # inclusive!
                if run in active:
                    # 2a. extend existing rect downward
                    x_top, _ = active[run]
                    new_active[run] = (x_top, x)  # keep same top, new bottom
                else:
                    # 2b. start a new rectangle
                    new_active[run] = (x, x)

            # -------- 3. any active runs NOT continued must be closed ------
            for run, (x_top, x_bot) in active.items():
                if run not in new_active:
                    y1, y2 = run
                    rectangles.append(self.create_area(x1=x_top, y1=y1, x2=x_bot, y2=y2))

            active = new_active

        # 4. close any rectangles that run to the last row
        for run, (x_top, x_bot) in active.items():
            y1, y2 = run
            rectangles.append(self.create_area(x1=x_top, y1=y1, x2=x_bot, y2=y2))

        return rectangles
