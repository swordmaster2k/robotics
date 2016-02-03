from threading import Thread

from framework.event.events import ScanResult
from framework.exception.exceptions import NoPathException


class Planner(Thread):
    """
    The Planner actually deals with moving the robot from A to B until it
    reaches the goal. It makes use of the map, robot, and a path planning
    algorithm to do this.

    It is implemented on its own thread.
    """

    def __init__(self, robot, map, algorithm, proxy):
        """
        Initialises the planner with a map and algorithm. It gets the
        robot from the map it is passed.

        :param map: current state space of the environment
        :param algorithm: path planning algorithm to use during run()
        :param proxy: communications connection to the robot
        :param output_file: debugging information file
        :param gnuplot_file: plot file for paths
        :return: a new planner
        """

        self.map = map
        self.robot = robot
        self.algorithm = algorithm

        self.proxy = proxy

        # Attach to notifiers.
        self.robot.listeners.append(self)
        self.map.listeners.append(self)

        self.finished = False
        self.last_scan = None

        Thread.__init__(self)

    def handle_event(self, event):
        """
        Handles specific event received from the system.

        :param event: generated system event from robot
        :return: none
        """
        if isinstance(event, ScanResult):
            self.last_scan = event

    def run(self):
        """
        The actions of the Planner using any algorithm are:

        1 . Plan
        2 . Check sensors to find obstacles.
        3 . Check the map for discrepancies.
        3a. If the map has changed, recompute the plan.
        4 . Check plan and initiate movement along shortest path.
        5 . Go to 2.

        Until we reach the goal.

        :return: none
        """

        try:
            '''
            Step 1: Plan.
            '''
            self.algorithm.plan()

            # Calculate our initial distance from the goal.
            x_difference = self.map.goal.x - self.robot.get_cell_x()
            y_difference = self.map.goal.y - self.robot.get_cell_y()

            if x_difference < 0:
                x_difference = -x_difference

            if y_difference < 0:
                y_difference = -y_difference

            # While we are not within 0.7 cells of the goal in both x and y.
            while not (0.5 >= x_difference >= -0.5 and 0.5 >= y_difference >= -0.5) and not self.finished:
                '''
                Step 2: Scan the immediate area for obstacles and free space.
                '''
                self.robot.ping()

                while self.last_scan is None:
                    continue

                # Just take 1 reading for now.
                affected_cells = []
                #self.map.ping_to_cells(round(float(self.last_scan.readings[0]) / self.map.cell_size, 2))
                self.last_scan = None

                '''
                Step 3: Update the map if necessary.
                '''
                if len(affected_cells) > 0:
                    updated_cells = self.map.update_map(affected_cells)
                    if len(updated_cells) > 0:
                        self.algorithm.update_occupancy_grid(updated_cells)

                        '''
                        Step 3a: Recompute the plan if necessary.
                        '''
                        self.algorithm.plan()

                '''
                Step 4: Pop the next point from the current path.
                '''
                if len(self.algorithm.path) == 0:  # Make sure there is a point.
                    break

                next_point = self.algorithm.pop_next_point()
                self.robot.go_to(next_point[0], next_point[1])

                # Wait for the robot to finish travelling.
                while self.robot.state != "Travelled":
                    continue

                self.robot.state = ""  # Reset the state.

                x_difference = self.map.goal.x - self.robot.get_cell_x()
                y_difference = self.map.goal.y - self.robot.get_cell_y()

                if x_difference < 0:
                    x_difference = +x_difference

                if y_difference < 0:
                    y_difference = +y_difference

            self.robot.halt()

        except NoPathException as ex:
            print(ex)
        except Exception as ex:
            print(ex)
        finally:
            if not self.finished:
                self.finished = True
